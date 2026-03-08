import os, shutil, asyncio
from uagents import Agent, Bureau, Context

# --- ⚙️ MASTER CONFIGURATION ---
MASTER_WALLET = "fetch1k6qg2lv5jpt3sdy66g5gn3f63m6e9wesdz99rm" # Your Bank Vault
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

def add_agent_logic(agent, name, wallet_address):
    @agent.on_event("startup")
    async def startup_audit(ctx: Context):
        # Using the wallet_address (fetch1...) for ledger queries
        bal = float(ctx.ledger.query_bank_balance(wallet_address)) / 10**18
        print(f"--- 🤖 {name} Online ---")
        print(f"💰 WALLET: {wallet_address} | BAL: {bal:.4f} FET")

        if name == BANKER_NAME and bal > 1.0:
            print("⛽ Banker checking fuel levels...")
            for addr in ALL_FETCH_ADDRESSES:
                if addr != wallet_address:
                    t_bal = float(ctx.ledger.query_bank_balance(addr)) / 10**18
                    if t_bal < 0.05:
                        print(f"💸 Fueling {addr[:12]}...")
                        await ctx.send_tokens(addr, int(0.1 * 10**18), "FET")

    @agent.on_interval(period=3600.0)
    async def sweep(ctx: Context):
        bal = float(ctx.ledger.query_bank_balance(wallet_address)) / 10**18
        if bal > 5.0:
            sweep_val = int((bal - 0.5) * 10**18)
            await ctx.send_tokens(MASTER_WALLET, sweep_val, "FET")
            print(f"🚀 {name} SWEPT to Vault.")

# Setup
for i, seed in enumerate(SEEDS):
    role = ["Oracle", "Notary", "Maker", "Broker"][min(i // 5, 3)]
    name = f"AlphaBeta-{role}-{i+1}"
    a = Agent(name=name, seed=seed)
    
    # CRITICAL: We get the .wallet.address() which is 'fetch1...', NOT the .address which is 'agent1...'
    f_addr = str(a.wallet.address())
    ALL_FETCH_ADDRESSES.append(f_addr)
    
    add_agent_logic(a, name, f_addr)
    bureau.add(a)

if __name__ == "__main__":
    perform_safety_backup()
    bureau.run()
    
