import asyncio, bech32
from uagents.network import get_ledger, wait_for_tx_to_complete
from uagents.crypto import Identity

# --- 🛡️ THE LOCKED TRUTH ---
CORRECT_BANKER_ADDR = "fetch1epm9ukcjq6dujv7pgerqnnlzu4k5nxrxjaq07x"
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

FUEL_AMOUNT = 50000000000000000 # 0.05 FET
ledger = get_ledger()

def get_target_fetch_addr(seed):
    """Bypasses derivation issues by decoding the agent's default address."""
    ident = Identity.from_seed(seed, 0)
    hrp, data = bech32.bech32_decode(ident.address)
    return bech32.bech32_encode("fetch", data)

async def final_fuel_run():
    # 1. Initialize Signer
    banker_ident = Identity.from_seed(BANKER_SEED, 0)
    
    # 2. Check the SPECIFIC address you provided
    bal = ledger.query_bank_balance(CORRECT_BANKER_ADDR)
    print(f"🏦 Banker (Locked): {CORRECT_BANKER_ADDR}")
    print(f"💰 Balance: {float(bal)/10**18:.4f} FET")

    if int(bal) < (FUEL_AMOUNT * 19):
        print(f"❌ ABORT: {CORRECT_BANKER_ADDR} needs more FET.")
        return

    # 3. Fuel the fleet
    for seed in SUB_SEEDS:
        target_addr = get_target_fetch_addr(seed)
        try:
            print(f"⛽ Sending to {target_addr[:15]}...")
            # We sign with banker_ident, but the ledger knows it comes from the funded addr
            tx = ledger.send_tokens(target_addr, FUEL_AMOUNT, "afet", banker_ident)
            await wait_for_tx_to_complete(tx.tx_hash, ledger)
            print(f"✅ Success: {tx.tx_hash[:10]}")
            await asyncio.sleep(1)
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(final_fuel_run())
