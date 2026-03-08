import os, shutil, asyncio
from uagents import Agent, Bureau, Context
from uagents.network import get_ledger, wait_for_tx_to_complete
from uagents.crypto import Identity

# --- ⚙️ CONFIGURATION ---
BANKER_NAME = "AlphaBeta-Oracle-1"
FUEL_AMOUNT = 50000000000000000  # 0.05 FET in AttoFET (10^18)

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

# Global list of sub-agent fetch addresses
sub_agent_wallets = []

async def distribute_fuel(ctx: Context):
    """The Banker (Agent 1) iterates through the fleet and sends fuel."""
    print(f"💰 {BANKER_NAME} starting distribution audit...")
    
    for target_wallet in sub_agent_wallets:
        # Don't send fuel to yourself
        if target_wallet == str(ctx.ledger.address):
            continue
            
        try:
            balance = ledger.query_bank_balance(target_wallet)
            if balance < (FUEL_AMOUNT / 2):
                print(f"⛽ Sending fuel to {target_wallet}...")
                # The Banker uses its own wallet (ctx.ledger) to send the transaction
                tx = ledger.send_tokens(target_wallet, FUEL_AMOUNT, "atestfet", ctx.ledger)
                await wait_for_tx_to_complete(tx.tx_hash, ledger)
                print(f"✅ Fuel delivered to {target_wallet[:15]}...")
                # Small sleep to prevent sequence errors on the blockchain
                await asyncio.sleep(2) 
        except Exception as e:
            print(f"⚠️ Could not fuel {target_wallet[:10]}: {e}")

# BUILD FLEET
for i, seed in enumerate(SEEDS):
    role = ["Oracle", "Notary", "Maker", "Broker"][min(i // 5, 3)]
    a_name = f"AlphaBeta-{role}-{i+1}"
    
    # Standard initialization - Agent 1 will naturally have the funded address
    agent_obj = Agent(name=a_name, seed=seed)
    
    # Convert 'agent...' address to 'fetch...' address for the ledger
    fetch_addr = Identity.from_seed(seed, 0).address
    
    if a_name == BANKER_NAME:
        # Agent 1 handles the distribution
        @agent_obj.on_event("startup")
        async def startup_fueling(ctx: Context):
            await distribute_fuel(ctx)
    else:
        # All other agents are added to the recipient list
        sub_agent_wallets.append(fetch_addr)

    bureau.add(agent_obj)

if __name__ == "__main__":
    perform_safety_backup()
    bureau.run()
