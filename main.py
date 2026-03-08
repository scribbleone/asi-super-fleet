import os, shutil, asyncio
from uagents import Agent, Bureau, Context

# --- ⚙️ CONFIGURATION & BACKUP ---
MASTER_WALLET = "fetch1epm9ukcjq6dujv7pgerqnnlzu4k5nxrxjaq07x"
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

for i, seed in enumerate(SEEDS):
    # Assignment Logic based on your original lucrative roles
    if i < 5: role, job = "Oracle", "Price Feed Service"
    elif i < 10: role, job = "Notary", "Data Authentication"
    elif i < 15: role, job = "Maker", "Liquidity Provision"
    else: role, job = "Broker", "Service Mediation"

    agent = Agent(name=f"AlphaBeta-{role}-{i+1}", seed=seed)

    @agent.on_event("startup")
    async def audit(ctx: Context):
        print(f"--- 🛡️ {ctx.name} Startup ---")
        print(f"ROLE: {job} | WALLET: {ctx.wallet.address()}")
        print(f"DISCLAIMER: This agent is authorized to sweep to {MASTER_WALLET}.")

    @agent.on_interval(period=300.0) # Internal check every 5 mins
    async def task(ctx: Context):
        # Automated Sweep Logic: Keep 0.5 FET, send rest to Master
        bal = float(ctx.ledger.query_bank_balance(ctx.wallet.address())) / 10**18
        if bal > 5.0:
            await ctx.send_tokens(MASTER_WALLET, int((bal-0.5) * 10**18), "FET")
            ctx.logger.info(f"💰 {ctx.name} swept earnings to Master Wallet.")

    bureau.add(agent)

if __name__ == "__main__":
    perform_safety_backup()
    bureau.run()
                                  
