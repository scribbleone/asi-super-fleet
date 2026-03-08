import os, shutil, asyncio
from uagents import Agent, Bureau, Context
from uagents.network import get_ledger
from uagents.crypto import Identity

# --- ⚙️ CONFIGURATION ---
BANKER_NAME = "AlphaBeta-Oracle-1"

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

async def find_funded_identity(seed):
    """Scans indices 0-9 to find where the 9.6 FET is hiding."""
    print("🔍 Scanning seed indices for funds...")
    for i in range(10):
        # We use Agent(seed, index) to ensure we get the correct wallet derivation
        temp_agent = Agent(seed=seed, index=i)
        wallet_addr = str(temp_agent.wallet.address()) # This gets the 'fetch1...' address
        
        try:
            bal_raw = ledger.query_bank_balance(wallet_addr)
            bal = float(bal_raw) / 10**18
            print(f"  Index {i}: {wallet_addr[:15]}... | {bal:.4f} FET")
            
            if bal > 0.5:
                print(f"⭐ SUCCESS! FOUND FUNDS AT INDEX {i}")
                return i
        except Exception as e:
            print(f"  Index {i}: Error querying balance: {e}")
            
    return 0

def register_handlers(target_agent, name, wallet_addr):
    @target_agent.on_event("startup")
    async def startup_audit(ctx: Context):
        bal_raw = ledger.query_bank_balance(wallet_addr)
        bal = float(bal_raw) / 10**18
        status = "✅ READY" if bal >= 0.05 else "❌ NO FUEL"
        print(f"[{status}] {name:20} | {bal:.4f} FET | {wallet_addr[:15]}...")

# RUN THE SCANNER
loop = asyncio.get_event_loop()
funded_index = loop.run_until_complete(find_funded_identity(SEEDS[0]))

# BUILD FLEET USING THE CORRECT INDEX
for i, seed in enumerate(SEEDS):
    role = ["Oracle", "Notary", "Maker", "Broker"][min(i // 5, 3)]
    a_name = f"AlphaBeta-{role}-{i+1}"
    
    # Apply the funded index to ALL agents or just the Banker? 
    # Usually, if you funded one, they are all likely at that same index.
    agent_obj = Agent(name=a_name, seed=seed, index=funded_index)
    
    w_addr = str(agent_obj.wallet.address())
    register_handlers(agent_obj, a_name, w_addr)
    bureau.add(agent_obj)

if __name__ == "__main__":
    perform_safety_backup()
    bureau.run()
