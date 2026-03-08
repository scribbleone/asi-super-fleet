import os, shutil, asyncio
from uagents import Agent, Bureau, Context
from uagents.network import get_ledger, wait_for_tx_to_complete
from uagents.crypto import Identity

# --- ⚙️ CONFIGURATION ---
BANKER_NAME = "AlphaBeta-Oracle-1"
FUEL_AMOUNT = 50000000000000000  # 0.05 FET

def perform_safety_backup():
    if os.path.exists("main.py"):
        shutil.copy("main.py", "main.py.backup")
        print("🛡️ Safety backup created.")

SEEDS = [
    "alpha_prime_v26_secure_881", "alpha_nexus_v26_secure_102", "alpha_orbit_v26_secure_554",
    "alpha_pulse_v26_secure_923", "alpha_glory_v26_secure_317", "alpha_delta_v26_secure_441",
    "alpha_titan_v26_secure_609", "alpha_solar_v26_secure_228", "alpha_zenith_v26_secure_773",
    "alpha_matrix_v26_secure_415", "beta_prime_v26_secure_119", "beta_nexus_v26_secure_802",
    "beta_orbit_v26_secure_334", "beta_pulse_v26_secure_772", "beta_glory_v26_secure_515",
    "beta_delta_v26_secure_661", "beta_titan_v26_secure_209", "beta_solar_v26_secure_882",
    "beta_zenith_v26_secure_337", "beta_matrix_v26_secure_551"
]

bureau = Bureau(port=8000, endpoint=["http://127.0.0.1:8000/submit"])
ledger = get_ledger()
sub_agent_wallets = []

async def distribute_fuel(ctx: Context):
    print("--- 🏦 STARTING FUEL DISTRIBUTION ---")
    try:
        # 1. Identify Banker's current state
        banker_addr = str(ctx.address)
        banker_fetch = Identity.from_seed(SEEDS[0], 0).address
        bal = ledger.query_bank_balance(banker_fetch)
        print(f"💰 Banker Address: {banker_fetch} | Balance: {float(bal)/10**18:.4f} FET")

        if int(bal) < (FUEL_AMOUNT * 2):
            print("⚠️ Insufficient funds for distribution.")
            return

        # 2. Iterate and Fund
        for target in sub_agent_wallets:
            if target == banker_fetch: continue
            
            t_bal = ledger.query_bank_balance(target)
            if int(t_bal) < (FUEL_AMOUNT / 2):
                print(f"⛽ Funding {target[:15]}...")
                # The ctx.wallet is the signer. 'afet' is the denom.
                tx = ledger.send_tokens(target, FUEL_AMOUNT, "afet", ctx.wallet)
                await wait_for_tx_to_complete(tx.tx_hash, ledger)
                print(f"✅ Success! Tx: {tx.tx_hash[:8]}")
                await asyncio.sleep(2) # Prevent sequence errors
                
    except Exception as e:
        print(f"❌ Distribution Error: {e}")
    print("--- 🏦 DISTRIBUTION CYCLE ENDED ---")

# BUILD FLEET
for i, seed in enumerate(SEEDS):
    role = ["Oracle", "Notary", "Maker", "Broker"][min(i // 5, 3)]
    a_name = f"AlphaBeta-{role}-{i+1}"
    
    agent_obj = Agent(name=a_name, seed=seed)
    # Correctly map the fetch address (Index 0)
    f_addr = Identity.from_seed(seed, 0).address
    
    if a_name == BANKER_NAME:
        @agent_obj.on_event("startup")
        async def startup_fueling(ctx: Context):
            # Short wait to let the system stabilize
            await asyncio.sleep(3)
            await distribute_fuel(ctx)
            
        @agent_obj.on_interval(period=1800) # Every 30 mins
        async def regular_fueling(ctx: Context):
            await distribute_fuel(ctx)
    else:
        sub_agent_wallets.append(f_addr)

    bureau.add(agent_obj)

if __name__ == "__main__":
    perform_safety_backup()
    bureau.run()
