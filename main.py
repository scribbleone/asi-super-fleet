import os, shutil, asyncio
from uagents import Agent, Bureau, Context
from uagents.crypto import Identity

# --- ⚙️ MASTER CONFIGURATION ---
MASTER_WALLET = "fetch1k6qg2lv5jpt3sdy66g5gn3f63m6e9wesdz99rm" 
BANKER_NAME = "AlphaBeta-Oracle-1"

def perform_safety_backup():
    if os.path.exists("main.py"):
        shutil.copy("main.py", "main.py.backup")
        print("🛡️ Safety backup created.")

# --- 🔑 THE 20 SEEDS ---
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

# CALCULATE ADDRESSES OFFLINE (No network calls here)
ALL_FETCH_ADDRS = []
for s in SEEDS:
    # We use the Identity class to get the address without hitting the blockchain
    ident = Identity.from_seed(s, 0)
    # The uagents lib provides the wallet address derived from the identity
    ALL_FETCH_ADDRS.append(ident.address)

def register_handlers(target_agent, name, my_addr):
    # Capture the wallet object directly from the agent
    agent_wallet = target_agent.wallet

    @target_agent.on_event("startup")
    async def startup_audit(ctx: Context):
        # Only check balance once per agent startup
        try:
            bal = float(ctx.ledger.query_bank_balance(my_addr)) / 10**18
            print(f"--- 🤖 {name} Online ---")
            print(f"💰 BAL: {bal:.4f} FET")

            if name == BANKER_NAME and bal > 1.0:
                print("⛽ Banker checking fuel levels...")
                for target in ALL_FETCH_ADDRS:
                    if target != my_addr:
                        # Only query ledger if banker has funds
                        t_bal = float(ctx.ledger.query_bank_balance(target)) / 10**18
                        if t_bal < 0.05:
                            print(f"💸 Fueling {target[:12]}...")
                            await ctx.ledger.send_tokens(agent_wallet, target, int(0.1 * 10**18), "FET")
        except Exception as e:
            print(f"⚠️ {name} Ledger Error: {e}")

    @target_agent.on_interval(period=3600.0)
    async def sweep(ctx: Context):
        try:
            bal = float(ctx.ledger.query_bank_balance(my_addr)) / 10**18
            if bal > 5.0:
                sweep_val = int((bal - 0.5) * 10**18)
                await ctx.ledger.send_tokens(agent_wallet, MASTER_WALLET, sweep_val, "FET")
                print(f"🚀 {name} SWEPT to Vault.")
        except:
            pass

# Create Fleet
for i, seed in enumerate(SEEDS):
    role = ["Oracle", "Notary", "Maker", "Broker"][min(i // 5, 3)]
    a_name = f"AlphaBeta-{role}-{i+1}"
    
    # Initialize the agent normally
    agent_obj = Agent(name=a_name, seed=seed)
    current_addr = str(agent_obj.wallet.address())
    
    register_handlers(agent_obj, a_name, current_addr)
    bureau.add(agent_obj)

if __name__ == "__main__":
    perform_safety_backup()
    bureau.run()
