import os, shutil, asyncio
from uagents import Agent, Bureau, Context
from uagents.network import get_ledger, wait_for_tx_to_complete
from uagents.crypto import Identity

# --- ⚙️ CONFIGURATION ---
BANKER_NAME = "AlphaBeta-Oracle-1"
# 0.05 FET expressed in AttoFET
FUEL_AMOUNT = 50000000000000000 

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
    # Get Banker's actual balance first
    banker_bal = ledger.query_bank_balance(str(ctx.address))
    print(f"💰 Banker ({BANKER_NAME}) Balance: {float(banker_bal)/10**18:.4f} FET")
    
    if int(banker_bal) < (FUEL_AMOUNT * 20):
        print("⚠️ Banker has insufficient funds to fuel the whole fleet. Proceeding with caution.")

    for target_wallet in sub_agent_wallets:
        try:
            current_bal = ledger.query_bank_balance(target_wallet)
            if int(current_bal) < (FUEL_AMOUNT / 2):
                print(f"⛽ Fueling {target_wallet[:15]}...")
                # Explicitly using Mainnet denomination "afet"
                tx = ledger.send_tokens(target_wallet, FUEL_AMOUNT, "afet", ctx.wallet)
                await wait_for_tx_to_complete(tx.tx_hash, ledger)
                print(f"✅ Success.")
                await asyncio.sleep(1) # Network breathing room
        except Exception as e:
            print(f"❌ Failed to fuel {target_wallet[:15]}: {e}")

# BUILD FLEET
for i, seed in enumerate(SEEDS):
    role = ["Oracle", "Notary", "Maker", "Broker"][min(i // 5, 3)]
    a_name = f"AlphaBeta-{role}-{i+1}"
    
    # We ensure they are all explicitly targeting Mainnet
    agent_obj = Agent(name=a_name, seed=seed)
    
    # Deriving the fetch1 address for the banker's list
    f_addr = Identity.from_seed(seed, 0).address
    
    if a_name == BANKER_NAME:
        @agent_obj.on_event("startup")
        async def startup_fueling(ctx: Context):
            await distribute_fuel(ctx)
    else:
        sub_agent_wallets.append(f_addr)

    bureau.add(agent_obj)

if __name__ == "__main__":
    perform_safety_backup()
    bureau.run()
