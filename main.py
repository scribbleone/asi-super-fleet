import os
import shutil
import asyncio
from uagents import Agent, Bureau, Context

# --- 1. CONFIGURATION ---
MASTER_WALLET = "fetch1epm9ukcjq6dujv7pgerqnnlzu4k5nxrxjaq07x" # Your funded wallet
SWEEP_THRESHOLD = 5.0  # Payout whenever balance > 5 FET
MIN_RETAINED = 0.5     # Keep 0.5 FET for gas

def perform_safety_backup():
    if os.path.exists("main.py"):
        shutil.copy("main.py", "main.py.backup")
        print("🛡️ Safety backup created.")

# --- 2. THE FLEET ---
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

for i, seed in enumerate(SEEDS):
    name = f"Agent-{'Alpha' if i < 10 else 'Beta'}-{(i % 10) + 1}"
    agent = Agent(name=name, seed=seed)

    @agent.on_event("startup")
    async def startup_audit(ctx: Context):
        print(f"--- 🛡️ {ctx.name} AUDIT ---")
        print(f"DISCLAIMER: This agent is authorized to sweep earnings to {MASTER_WALLET}.")

    # --- SWEEP LOGIC (Every 1 hour) ---
    @agent.on_interval(period=3600.0)
    async def sweep_earnings(ctx: Context):
        balance = float(ctx.ledger.query_bank_balance(ctx.wallet.address())) / 10**18
        if balance > SWEEP_THRESHOLD:
            amount_to_send = balance - MIN_RETAINED
            ctx.logger.info(f"💰 Threshold reached! Sweeping {amount_to_send} FET to Master.")
            await ctx.send_tokens(MASTER_WALLET, int(amount_to_send * 10**18), "FET")

    bureau.add(agent)

if __name__ == "__main__":
    perform_safety_backup()
    bureau.run()
    
