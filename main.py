import os, shutil, asyncio
from uagents import Agent, Bureau, Context

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
ALL_FETCH_ADDRESSES = []

def add_agent_logic(agent_obj):
    name = agent_obj.name
    wallet_addr = str(agent_obj.wallet.address())

    @agent_obj.on_event("startup")
    async def startup_audit(ctx: Context):
        bal = float(ctx.ledger.query_bank_balance(wallet_addr)) / 10**18
        print(f"--- 🤖 {name} Online ---")
        print(f"💰 BAL: {bal:.4f} FET")

        # Alpha 1 handles fueling
        if name == BANKER_NAME and bal > 1.0:
            print("⛽ Banker checking fuel levels...")
            for addr in ALL_FETCH_ADDRESSES:
                if addr != wallet_addr:
                    t_bal = float(ctx.ledger.query_bank_balance(addr)) / 10**18
                    if t_bal < 0.05:
                        print(f"💸 Fueling {addr[:12]}...")
                        # Pass the wallet object directly from the agent
                        await ctx.ledger.send_tokens(agent_obj.wallet, addr, int(0.1 * 10**18), "FET")

    @agent_obj.on_interval(period=3600.0)
    async def sweep(ctx: Context):
        bal = float(ctx.ledger.query_bank_balance(wallet_addr)) / 10**18
        if bal > 5.0:
            sweep_val = int((bal - 0.5) * 10**18)
            await ctx.ledger.send_tokens(agent_obj.wallet, MASTER_WALLET, sweep_val, "FET")
            print(f"🚀 {name} SWEPT to Vault.")

# Build Fleet
for i, seed in enumerate(SEEDS):
    role = ["Oracle", "Notary", "Maker", "Broker"][min(i // 5, 3)]
    a_name = f"AlphaBeta-{role}-{i+1}"
    
    agent = Agent(name=a_name, seed=seed)
    ALL_FETCH_ADDRESSES.append(str(agent.wallet.address()))
    
    add_agent_logic(agent)
    bureau.add(agent)

if __name__ == "__main__":
    perform_safety_backup()
    bureau.run()
    
