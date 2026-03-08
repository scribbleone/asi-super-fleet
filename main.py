import asyncio
from uagents.network import get_ledger, wait_for_tx_to_complete
from uagents.crypto import Identity
from cosmpy.crypto.address import Address # The "Secret Sauce" for checksums

# --- ⚙️ FUNDING SETUP ---
BANKER_SEED = "alpha_prime_v26_secure_881"
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

def get_valid_fetch_address(seed):
    """Derives a valid fetch1 address with a correct checksum."""
    ident = Identity.from_seed(seed, 0)
    # Convert the raw public key bytes into a fetch1 address
    return str(Address(ident.public_key, prefix="fetch"))

async def manual_fuel_run():
    # 1. Initialize Banker
    banker_fetch_address = get_valid_fetch_address(BANKER_SEED)
    banker_identity = Identity.from_seed(BANKER_SEED, 0)
    
    print(f"🏦 Banker Validated Address: {banker_fetch_address}")
    
    try:
        banker_bal = ledger.query_bank_balance(banker_fetch_address)
        print(f"💰 Current Banker Balance: {float(banker_bal)/10**18:.4f} FET")
    except Exception as e:
        print(f"❌ Ledger Rejected Address again: {e}")
        return

    # 2. Loop through sub-agents
    for seed in SUB_SEEDS:
        target_fetch_address = get_valid_fetch_address(seed)
        
        try:
            print(f"⛽ Sending 0.05 FET to {target_fetch_address}...")
            tx = ledger.send_tokens(target_fetch_address, FUEL_AMOUNT, "afet", banker_identity)
            await wait_for_tx_to_complete(tx.tx_hash, ledger)
            print(f"✅ Success. Tx: {tx.tx_hash[:12]}")
            await asyncio.sleep(1.5) 
        except Exception as e:
            print(f"❌ Error with {target_fetch_address[:15]}: {e}")

    print("\n🏁 Mission Accomplished. Enjoy your break!")

if __name__ == "__main__":
    asyncio.run(manual_fuel_run())
