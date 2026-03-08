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

# Pre-calculate all addresses so the Banker knows where to send FET
for seed in SEEDS:
    temp_agent = Agent(seed=seed)
    ALL_FETCH_ADDRESSES.append(str(temp_agent.wallet.address()))

# Create Fleet
for i, seed in enumerate(SEEDS):
    role = ["Oracle", "Notary", "Maker", "Broker"][min(i // 5, 3)]
    a_name = f"AlphaBeta-{role}-{i+1}"
    
    agent = Agent(name=a_name, seed=seed)
    current_addr = str(agent.wallet.address())

    # We use a closure to lock in the 'agent' object for each handler
    def make_handlers(a, name, my_addr):
        @a.on_event("startup")
        async def startup_audit(ctx: Context):
            bal = float(ctx.ledger.query_bank_balance(my_addr)) / 10**18
            print(f"--- 🤖 {name} Online ---")
            print(f"💰 BAL: {bal:.4f} FET")

            if name == BANKER_NAME and bal > 1.0:
                print("⛽ Banker checking fuel levels...")
                for target_addr in ALL_FETCH_ADDRESSES:
                    if target_addr != my_addr:
                        t_bal = float(ctx.ledger.query_bank_balance(target_addr)) / 10**18
                        if t_bal < 0.05:
                            print(f"💸 Fueling {target_addr[:12]}...")
                            await ctx.ledger.send_tokens(a.wallet, target_addr, int(0.1 * 10**18), "FET")

        @a.on_interval(period=3600.0)
        async def sweep(ctx: Context):
            bal = float(ctx.ledger.query_bank_balance(my_addr)) / 10**18
            if bal > 5.0:
                sweep_val = int((bal - 0.5) * 10**18)
                # Ensure we pass the actual wallet object, not a string
                await ctx.ledger.send_tokens(a.wallet, MASTER_WALLET, sweep_val, "FET")
                print(f"🚀 {name} SWEPT to Vault.")

    make_handlers(agent, a_name, current_addr)
    bureau.add(agent)

if __name__ == "__main__":
    perform_safety_backup()
    bureau.run()
    
