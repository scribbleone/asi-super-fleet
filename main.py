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
ALL_AGENT_ADDRESSES = []

# First pass: Create agents and collect addresses
agents = []
for i, seed in enumerate(SEEDS):
    if i < 5: role = "Oracle"
    elif i < 10: role = "Notary"
    elif i < 15: role = "Maker"
    else: role = "Broker"
    
    name = f"AlphaBeta-{role}-{i+1}"
    a = Agent(name=name, seed=seed)
    agents.append(a)
    ALL_AGENT_ADDRESSES.append(str(a.wallet.address()))

for a in agents:
    @a.on_event("startup")
    async def startup_audit(ctx: Context):
        # Corrected access: ctx.agent.wallet
        my_addr = str(ctx.agent.wallet.address())
        bal = float(ctx.ledger.query_bank_balance(my_addr)) / 10**18
        print(f"--- 🤖 {ctx.agent.name} Online ---")
        print(f"💰 BAL: {bal:.4f} FET")

        # Banker logic to fuel the fleet
        if ctx.agent.name == BANKER_NAME and bal > 1.0:
            print("⛽ Banker checking fuel levels...")
            for addr in ALL_AGENT_ADDRESSES:
                if addr != my_addr:
                    t_bal = float(ctx.ledger.query_bank_balance(addr)) / 10**18
                    if t_bal < 0.05:
                        print(f"💸 Sending 0.1 FET gas to {addr[:10]}...")
                        await ctx.send_tokens(addr, int(0.1 * 10**18), "FET")

    @a.on_interval(period=3600.0)
    async def sweep_and_track(ctx: Context):
        my_addr = str(ctx.agent.wallet.address())
        bal = float(ctx.ledger.query_bank_balance(my_addr)) / 10**18
        
        if bal > 5.0:
            sweep_val = int((bal - 0.5) * 10**18)
            await ctx.send_tokens(MASTER_WALLET, sweep_val, "FET")
            print(f"🚀 {ctx.agent.name} SWEPT: {bal-0.5} FET sent to Vault.")
            # We can log this to a file in a later step once basic run works
            
    bureau.add(a)

if __name__ == "__main__":
    perform_safety_backup()
    bureau.run()
    
