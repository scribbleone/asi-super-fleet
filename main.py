import asyncio, shutil, os
from uagents.network import wait_for_tx_to_complete
from uagents.crypto import Identity
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# --- 🎯 THE LOCKED TRUTH ---
# We are going to try to derive the funded address using a different internal method
FUNDED_ADDR = "fetch1epm9ukcjq6dujv7pgerqnnlzu4k5nxrxjaq07x"
BANKER_SEED_STRING = "alpha_prime_v26_secure_881"

MAINNET_CONFIG = NetworkConfig(
    chain_id="fetchhub-4",
    url="grpc+https://grpc-fetchhub.fetch.ai:443",
    fee_minimum_gas_price=5000000000,
    fee_denomination="afet",
    staking_denomination="afet",
)
ledger = LedgerClient(MAINNET_CONFIG)

SUB_SEEDS = [
    "alpha_nexus_v26_secure_102", "alpha_orbit_v26_secure_554", "alpha_pulse_v26_secure_923", 
    "alpha_glory_v26_secure_317", "alpha_delta_v26_secure_441", "alpha_titan_v26_secure_609", 
    "alpha_solar_v26_secure_228", "alpha_zenith_v26_secure_773", "alpha_matrix_v26_secure_415", 
    "beta_prime_v26_secure_119", "beta_nexus_v26_secure_802", "beta_orbit_v26_secure_334", 
    "beta_pulse_v26_secure_772", "beta_glory_v26_secure_515", "beta_delta_v26_secure_661", 
    "beta_titan_v26_secure_209", "beta_solar_v26_secure_882", "beta_zenith_v26_secure_337", 
    "beta_matrix_v26_secure_551"
]

FUEL_AMOUNT = 50000000000000000 

async def final_fuel_run():
    print(f"🕵️ Analyzing Seed logic for {FUNDED_ADDR}...")

    # TEST A: Does a simple hash of the seed string work?
    # Some older implementations just sha256 the string to get the private key
    import hashlib
    h = hashlib.sha256(BANKER_SEED_STRING.encode()).digest()
    test_wallet = LocalWallet(PrivateKey(h), prefix="fetch")
    
    if str(test_wallet.address()) == FUNDED_ADDR:
        print("🎯 Found it! Seed was a direct SHA256 hash.")
        banker_wallet = test_wallet
    else:
        print(f"❌ SHA256 test failed. Derived: {test_wallet.address()}")
        # TEST B: Check if there's an index we missed or a legacy path
        print("Checking legacy derivation indices...")
        banker_wallet = None
        for i in range(100):
            # We use Identity's logic but try a different index range
            test_ident = Identity.from_seed(BANKER_SEED_STRING, i)
            test_wallet = LocalWallet(PrivateKey(bytes.fromhex(test_ident.private_key)), prefix="fetch")
            if str(test_wallet.address()) == FUNDED_ADDR:
                print(f"🎯 Found it! Index: {i}")
                banker_wallet = test_wallet
                break

    if not banker_wallet:
        print("🛑 RECOVERY FAILED. The seed string provided does not mathematically produce the funded address.")
        print("Check if there is a typo in 'alpha_prime_v26_secure_881'.")
        return

    # --- FLEET FUELING ---
    bal = ledger.query_bank_balance(str(banker_wallet.address()))
    print(f"💰 Balance: {float(bal)/10**18:.4f} FET")

    for seed in SUB_SEEDS:
        # Generate targets using standard index 0
        target_ident = Identity.from_seed(seed, 0)
        target_wallet = LocalWallet(PrivateKey(bytes.fromhex(target_ident.private_key)), prefix="fetch")
        target_addr = str(target_wallet.address())
        
        try:
            print(f"⛽ Sending 0.05 to {target_addr[:15]}...")
            tx = ledger.send_tokens(target_addr, FUEL_AMOUNT, "afet", banker_wallet)
            await wait_for_tx_to_complete(tx.tx_hash, ledger)
            print(f"✅ Success!")
        except Exception as e:
            print(f"⚠️ Transfer Error: {e}")

if __name__ == "__main__":
    asyncio.run(final_fuel_run())
