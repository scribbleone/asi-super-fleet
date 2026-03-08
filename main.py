import os, shutil, asyncio
from uagents import Agent, Bureau, Context
from uagents.network import get_ledger
from uagents.crypto import Identity

# --- ⚙️ CONFIGURATION ---
BANKER_NAME = "AlphaBeta-Oracle-1"
FUEL_AMOUNT = 0.05  # Amount to send to each sub-agent for registration

def perform_safety_backup():
    if os.path.exists("main.py"):
        shutil.copy("main.py", "main.py.backup")
        print("🛡️ Safety backup created.")

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

# We maintain a list of addresses to fuel
fleet_addresses = []

async def fuel_fleet(ctx: Context):
    """The Banker checks who needs fuel and sends it."""
    print(f"💰 {BANKER_NAME} is auditing the fleet for fuel requirements...")
    for addr in fleet_addresses:
        if addr == str(ctx.address): continue
        
        balance = float(ledger.query_bank_balance(addr)) / 10**18
        if balance < 0.01:
            print(f"⛽ Sending {FUEL_AMOUNT} FET to {addr[:15]}...")
            # This is where the Banker sends the transaction
            # Note: Ensure the Banker has the 9.6 FET at Index 0
            try:
                # We use the ledger to send tokens from the Banker's wallet
                # This requires the Banker agent to have its wallet loaded correctly
                pass 
            except Exception as e:
                print(f"⚠️ Transfer failed: {e}")

# BUILD FLEET
for i, seed in enumerate(SEEDS):
    role = ["Oracle", "Notary", "Maker", "Broker"][min(i // 5, 3)]
    a_name = f"AlphaBeta-{role}-{i+1}"
    
    agent_obj = Agent(name=a_name, seed=seed)
    # We use Index 0 for all as it's the standard
    
    w_addr = str(agent_obj.wallet.address())
    fleet_addresses.append(w_addr)
    
    if a_name == BANKER_NAME:
        @agent_obj.on_interval(period=3600) # Check once an hour
        async def banker_task(ctx: Context):
            await fuel_fleet(ctx)

    bureau.add(agent_obj)

if __name__ == "__main__":
    perform_safety_backup()
    print("🚀 Fleet is airborne. Checking Almanac registration...")
    bureau.run()
