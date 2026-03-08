import os, shutil, asyncio
from uagents import Agent, Bureau, Context
from uagents.network import get_ledger

# --- ⚙️ CONFIGURATION ---
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
ledger = get_ledger()

def register_handlers(target_agent, name, wallet_addr):
    @target_agent.on_event("startup")
    async def startup_audit(ctx: Context):
        try:
            # Atomic balance check
            bal_raw = ledger.query_bank_balance(wallet_addr)
            bal = float(bal_raw) / 10**18
            status = "✅ READY" if bal >= 0.05 else "❌ NO FUEL"
            
            print(f"[{status}] {name:20} | {bal:.4f} FET | {wallet_addr[:15]}...")

            if name == BANKER_NAME and bal > 0.5:
                print(f"⛽ {name} initiating direct-ledger fueling...")
                # We build the list of targets inside the banker only
                for s_seed in SEEDS:
                    t_agent = Agent(seed=s_seed)
                    t_wallet = str(t_agent.wallet.address())
                    
                    if t_wallet != wallet_addr:
                        t_bal = float(ledger.query_bank_balance(t_wallet)) / 10**18
                        if t_bal < 0.05:
                            print(f"💸 Sending 0.1 FET to {t_wallet[:15]}...")
                            try:
                                # This is the most direct way to sign and send tokens
                                await ledger.send_tokens(target_agent.wallet, t_wallet, int(0.1 * 10**18), "FET")
                                await asyncio.sleep(3) # Heavy sleep to ensure sequence confirmation
                            except Exception as inner_e:
                                print(f"❌ Transfer Failed: {inner_e}")
        except Exception as e:
            print(f"⚠️ {name} System Error: {e}")

# BUILD FLEET
for i, seed in enumerate(SEEDS):
    role = ["Oracle", "Notary", "Maker", "Broker"][min(i // 5, 3)]
    a_name = f"AlphaBeta-{role}-{i+1}"
    
    agent_obj = Agent(name=a_name, seed=seed)
    w_addr = str(agent_obj.wallet.address())
    
    register_handlers(agent_obj, a_name, w_addr)
    bureau.add(agent_obj)

if __name__ == "__main__":
    perform_safety_backup()
    bureau.run()
