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

# OFFLINE WALLET ADDRESS CALCULATION
ALL_WALLETS = []
for s in SEEDS:
    ident = Identity.from_seed(s, 0)
    ALL_WALLETS.append(ident.address)

def register_handlers(target_agent, name, my_wallet_addr):
    agent_wallet_obj = target_agent.wallet

    @target_agent.on_event("startup")
    async def startup_audit(ctx: Context):
        try:
            bal_raw = ctx.ledger.query_bank_balance(my_wallet_addr)
            bal = float(bal_raw) / 10**18
            status = "✅ READY" if bal >= 0.05 else "❌ NO FUEL"
            
            # DASHBOARD DISPLAY
            print(f"[{status}] {name:20} | {bal:.4f} FET | {my_wallet_addr[:15]}...")

            if name == BANKER_NAME:
                if bal < 0.2:
                    print(f"🚨 ALERT: Banker {name} low on funds ({bal:.4f} FET)!")
                else:
                    print(f"⛽ Banker {name} online. Fueling fleet...")
                    for target_wallet in ALL_WALLETS:
                        if target_wallet != my_wallet_addr:
                            t_bal = float(ctx.ledger.query_bank_balance(target_wallet)) / 10**18
                            if t_bal < 0.05:
                                print(f"💸 Fueling {target_wallet[:15]}...")
                                # Send tokens to the fetch1 address
                                await ctx.ledger.send_tokens(agent_wallet_obj, target_wallet, int(0.1 * 10**18), "FET")
                                # Tiny sleep to prevent network congestion
                                await asyncio.sleep(2) 
                    print("✅ Fueling sequence complete.")
        except Exception as e:
            print(f"⚠️ {name} Ledger Error: {e}")

    @target_agent.on_interval(period=3600.0)
    async def sweep(ctx: Context):
        try:
            bal = float(ctx.ledger.query_bank_balance(my_wallet_addr)) / 10**18
            if bal > 5.0:
                sweep_val = int((bal - 0.5) * 10**18)
                await ctx.ledger.send_tokens(agent_wallet_obj, MASTER_WALLET, sweep_val, "FET")
                print(f"🚀 {name} SWEPT to Vault.")
        except:
            pass

# BUILD FLEET
for i, seed in enumerate(SEEDS):
    role = ["Oracle", "Notary", "Maker", "Broker"][min(i // 5, 3)]
    a_name = f"AlphaBeta-{role}-{i+1}"
    
    agent_obj = Agent(name=a_name, seed=seed)
    # Ensure we pass the wallet's fetch1 address
    wallet_addr = str(agent_obj.wallet.address())
    
    register_handlers(agent_obj, a_name, wallet_addr)
    bureau.add(agent_obj)

if __name__ == "__main__":
    perform_safety_backup()
    bureau.run()
