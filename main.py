import os, shutil, asyncio
from uagents import Agent, Bureau, Context

# --- ⚙️ MASTER CONFIGURATION ---
# YOUR REAL BANK VAULT ADDRESS
MASTER_WALLET = "fetch1k6qg2lv5jpt3sdy66g5gn3f63m6e9wesdz99rm"

# THE FUNDED ACCOUNT (Alpha 1)
BANKER_SEED = "alpha_prime_v26_secure_881"

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

# We need to pre-generate addresses to help the Banker find them
ALL_AGENT_ADDRESSES = []

for i, seed in enumerate(SEEDS):
    # Role Assignment
    if i < 5: role, job = "Oracle", "Price Feed"
    elif i < 10: role, job = "Notary", "Authentication"
    elif i < 15: role, job = "Maker", "Liquidity"
    else: role, job = "Broker", "Mediation"

    agent = Agent(name=f"AlphaBeta-{role}-{i+1}", seed=seed)
    ALL_AGENT_ADDRESSES.append(str(agent.wallet.address()))

    @agent.on_event("startup")
    async def startup_audit(ctx: Context):
        bal = float(ctx.ledger.query_bank_balance(ctx.wallet.address())) / 10**18
        print(f"--- 🤖 {ctx.agent.name} Online ---")
        print(f"💰 BAL: {bal:.4f} FET | 🏦 TARGET: {MASTER_WALLET}")

        # SPECIAL LOGIC FOR ALPHA 1 (The Banker)
        if ctx.agent.name == "AlphaBeta-Oracle-1":
            print("⛽ Banker detected. Checking fleet fuel levels...")
            for addr in ALL_AGENT_ADDRESSES:
                if addr != str(ctx.wallet.address()):
                    target_bal = float(ctx.ledger.query_bank_balance(addr)) / 10**18
                    if target_bal < 0.05: # If they have almost nothing
                        print(f"💸 Sending gas to {addr[:10]}...")
                        await ctx.send_tokens(addr, int(0.1 * 10**18), "FET")

    @agent.on_interval(period=3600.0)
    async def sweep(ctx: Context):
        bal = float(ctx.ledger.query_bank_balance(ctx.wallet.address())) / 10**18
        if bal > 5.0:
            sweep_val = int((bal - 0.5) * 10**18)
            await ctx.send_tokens(MASTER_WALLET, sweep_val, "FET")
            print(f"🚀 {ctx.agent.name} swept earnings to Vault.")

    bureau.add(agent)

if __name__ == "__main__":
    perform_safety_backup()
    bureau.run()
    
