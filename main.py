import asyncio
from uagents.network import get_ledger, wait_for_tx_to_complete
from uagents.crypto import Identity

# --- ⚙️ FUNDING SETUP ---
# Your Banker Seed (Oracle-1)
BANKER_SEED = "alpha_prime_v26_secure_881"
# The other 19 seeds to fund
SUB_SEEDS = [
    "alpha_nexus_v26_secure_102", "alpha_orbit_v26_secure_554", "alpha_pulse_v26_secure_923", 
    "alpha_glory_v26_secure_317", "alpha_delta_v26_secure_441", "alpha_titan_v26_secure_609", 
    "alpha_solar_v26_secure_228", "alpha_zenith_v26_secure_773", "alpha_matrix_v26_secure_415", 
    "beta_prime_v26_secure_119", "beta_nexus_v26_secure_802", "beta_orbit_v26_secure_334", 
    "beta_pulse_v26_secure_772", "beta_glory_v26_secure_515", "beta_delta_v26_secure_661", 
    "beta_titan_v26_secure_209", "beta_solar_v26_secure_882", "beta_zenith_v26_secure_337", 
    "beta_matrix_v26_secure_551"
]

FUEL_AMOUNT = 50000000000000000  # 0.05 FET
ledger = get_ledger()

async def manual_fuel_run():
    # 1. Initialize Banker
    banker_identity = Identity.from_seed(BANKER_SEED, 0)
    print(f"🏦 Banker initialized: {banker_identity.address}")
    
    banker_bal = ledger.query_bank_balance(banker_identity.address)
    print(f"💰 Current Banker Balance: {float(banker_bal)/10**18:.4f} FET")

    # 2. Loop through sub-agents
    for seed in SUB_SEEDS:
        target_addr = Identity.from_seed(seed, 0).address
        
        try:
            print(f"⛽ Sending to {target_addr[:15]}...")
            # Direct ledger transfer
            tx = ledger.send_tokens(target_addr, FUEL_AMOUNT, "afet", banker_identity)
            await wait_for_tx_to_complete(tx.tx_hash, ledger)
            print(f"✅ Success. Tx: {tx.tx_hash[:10]}")
            await asyncio.sleep(1) # Small gap
        except Exception as e:
            print(f"❌ Error with {target_addr[:10]}: {e}")

    print("\n🏁 All transfers attempted. You can now go back to your main Bureau script!")

if __name__ == "__main__":
    asyncio.run(manual_fuel_run())
