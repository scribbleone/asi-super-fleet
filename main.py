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

async def find_funded_index(seed):
    """Scans indices for funds by forcing fetch1 address format."""
    print("🔍 Scanning seed indices for funds...")
    for i in range(10):
        ident = Identity.from_seed(seed, i)
        
        # This is the critical fix: manually deriving the fetch1 address
        # We use the agent's internal wallet logic to get the correct prefix
        temp_agent = Agent(seed=seed, index=i) if hasattr(Agent, 'index') else Agent(seed=seed)
        wallet_addr = str(temp_agent.wallet.address())
        
        # If it still starts with 'agent', we strip and re-prefix or use the raw address
        if wallet_addr.startswith("agent"):
            # The ledger needs the fetch1 version of the same public key
            from uagents.crypto import encode_bech32
            raw_address = ident.address_bytes
            wallet_addr = encode_bech32("fetch", raw_address)

        try:
            bal_raw = ledger.query_bank_balance(wallet_addr)
            bal = float(bal_raw) / 10**18
            print(f"  Index {i}: {wallet_addr} | {bal:.4f} FET")
            
            if bal > 0.1:
                print(f"⭐ SUCCESS! FOUND {bal:.4f} FET AT INDEX {i}")
                return i
        except Exception as e:
            print(f"  Index {i} ({wallet_addr[:10]}...): Ledger rejected request.")
            
    return 0

def register_handlers(target_agent, name, wallet_addr):
    @target_agent.on_event("startup")
    async def startup_audit(ctx: Context):
        try:
            bal_raw = ledger.query_bank_balance(wallet_addr)
            bal = float(bal_raw) / 10**18
            status = "✅ READY" if bal >= 0.05 else "❌ NO FUEL"
            print(f"[{status}] {name:20} | {bal:.4f} FET | {wallet_addr[:15]}...")
        except:
            pass

# 1. RUN THE SCANNER
loop = asyncio.get_event_loop()
funded_index = loop.run_until_complete(find_funded_index(SEEDS[0]))

# 2. BUILD FLEET
for i, seed in enumerate(SEEDS):
    role = ["Oracle", "Notary", "Maker", "Broker"][min(i // 5, 3)]
    a_name = f"AlphaBeta-{role}-{i+1}"
    
    agent_identity = Identity.from_seed(seed, funded_index)
    agent_obj = Agent(name=a_name, identity=agent_identity)
    
    # Use the encoded fetch address for our internal tracking/audits
    from uagents.crypto import encode_bech32
    w_addr = encode_bech32("fetch", agent_identity.address_bytes)
    
    register_handlers(agent_obj, a_name, w_addr)
    bureau.add(agent_obj)

if __name__ == "__main__":
    perform_safety_backup()
    bureau.run()
