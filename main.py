import asyncio, shutil, os
from uagents.network import wait_for_tx_to_complete
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# --- 🎯 THE LOCKED TRUTH ---
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

FUEL_AMOUNT = 50000000000000000 # 0.05 FET

def get_wallet_from_seed(seed_str):
    # This mimics the exact way standard Fetch wallets derive from a seed string
    from uagents.crypto import Identity
    ident = Identity.from_seed(seed_str, 0)
    return LocalWallet(PrivateKey(bytes.fromhex(ident.private_key)), prefix="fetch")

async def final_fuel_run():
    print(f"🛰️ Executing brute-force recovery for {FUNDED_ADDR}...")
    
    # Backup current file before we proceed
    if not os.path.exists("main.py.bak"):
        shutil.copy("main.py", "main.py.bak")
        print("📁 Created main.py.bak")

    # We need to find why the Identity.from_seed is giving us 'fetch1d2c'
    # It's possible the funded address was created at a different index or path
    # Let's check indices 0-50 across standard uagents logic
    from uagents.crypto import Identity
    
    banker_wallet = None
    for i in range(51):
        test_ident = Identity.from_seed(BANKER_SEED_STRING, i)
        test_wallet = LocalWallet(PrivateKey(bytes.fromhex(test_ident.private_key)), prefix="fetch")
        if str(test_wallet.address()) == FUNDED_ADDR:
            print(f"🎯 MATCH FOUND! Index: {i}")
            banker_wallet = test_wallet
            break
    
    if not banker_wallet:
        print("❌ CRITICAL: Could not derive ...jaq07x from this seed at any index (0-50).")
        print(f"Common derivation at index 0 is: {str(get_wallet_from_seed(BANKER_SEED_STRING).address())}")
        return

    bal = ledger.query_bank_balance(str(banker_wallet.address()))
    print(f"💰 Mainnet Balance: {float(bal)/10**18:.4f} FET")

    for seed in SUB_SEEDS:
        target_wallet = get_wallet_from_seed(seed)
        target_addr = str(target_wallet.address())
        try:
            print(f"⛽ Fueling {target_addr[:15]}...")
            tx = ledger.send_tokens(target_addr, FUEL_AMOUNT, "afet", banker_wallet)
            await wait_for_tx_to_complete(tx.tx_hash, ledger)
            print(f"✅ TX: {tx.tx_hash[:10]}")
        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    asyncio.run(final_fuel_run())
