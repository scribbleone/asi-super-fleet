import os, shutil, asyncio
from uagents import Agent, Bureau, Context
from uagents.network import get_ledger, get_mainnet_prefix
from uagents.crypto import Identity, encode_bech32

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
ledger = get_ledger() # This defaults to Mainnet

async def find_funded_index(seed):
    print("🔍 Scanning Mainnet for the 9.6 FET...")
    # We will test a few different ways the wallet might be derived
    for i in range(5):
        ident = Identity.from_seed(seed, i)
        # Convert to the 'fetch1' format the ledger actually understands
        fetch_addr = encode_bech32("fetch", ident.address_bytes)
        
        try:
            bal_raw = ledger.query_bank_balance(fetch_addr)
            bal = float(bal_raw) / 10**18
            print(f"  [Index {i}] Address: {fetch_addr} | Bal: {bal:.4f} FET")
            
            if bal > 0.1:
                print(f"⭐ FOUND FUNDS AT INDEX {i}!")
                return i
        except Exception as e:
            print(f"  [Index {i}] Query failed: {e}")
    return 0

def register_handlers(target_agent, name, wallet_addr):
    @target_agent.on_event("startup")
    async def startup_audit(ctx: Context):
        try:
            bal_raw = ledger.query_bank_balance(wallet_addr)
            bal = float(bal_raw) / 10**18
            status = "✅ READY" if bal >= 0.01 else "❌ NO FUEL"
            print(f"[{status}] {name:20} | {bal:.4f} FET | {wallet_addr[:15]}...")
        except: pass

# 1. FIND THE MONEY
loop = asyncio.get_event_loop()
found_idx = loop.run_until_complete(find_funded_index(SEEDS[0]))

# 2. START THE FLEET
for i, seed in enumerate(SEEDS):
    role = ["Oracle", "Notary", "Maker", "Broker"][min(i // 5, 3)]
    a_name = f"AlphaBeta-{role}-{i+1}"
    
    # Correcting the initialization: use the seed and the correct index
    agent_obj = Agent(name=a_name, seed=seed) 
    # We manually override the identity if the index was not 0
    if found_idx != 0:
        new_ident = Identity.from_seed(seed, found_idx)
        agent_obj._identity = new_ident
        
    fetch_addr = encode_bech32("fetch", agent_obj.identity.address_bytes)
    register_handlers(agent_obj, a_name, fetch_addr)
    bureau.add(agent_obj)

if __name__ == "__main__":
    perform_safety_backup()
    bureau.run()
