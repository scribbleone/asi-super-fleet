import asyncio, bech32
from uagents.network import get_ledger, wait_for_tx_to_complete
from uagents.crypto import Identity
from cosmpy.aerial.client import LedgerClient, NetworkConfig

# --- 🎯 THE RIGID CONFIG ---
FUNDED_ADDR = "fetch1epm9ukcjq6dujv7pgerqnnlzu4k5nxrxjaq07x"
BANKER_SEED = "alpha_prime_v26_secure_881"

# Manually defining the Mainnet parameters we found earlier
MAINNET_CONFIG = NetworkConfig(
    chain_id="fetchhub-4",
    url="grpc+https://grpc-fetchhub.fetch.ai:443",
    fee_minimum_gas_price=5000000000,
    fee_denomination="afet",
    staking_denomination="afet",
)

# Use the manual client instead of the generic get_ledger()
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

def get_fetch_address(seed):
    ident = Identity.from_seed(seed, 0)
    hrp, data = bech32.bech32_decode(ident.address)
    return bech32.bech32_encode("fetch", data)

async def final_fuel_run():
    # Signer must match the derivation that leads to jaq07x
    # Based on our "digging", we confirmed this seed + index 0 = jaq07x
    banker_ident = Identity.from_seed(BANKER_SEED, 0)
    
    print(f"📡 Querying Fetch Mainnet (fetchhub-4)...")
    try:
        bal = ledger.query_bank_balance(FUNDED_ADDR)
        print(f"🏦 Banker: {FUNDED_ADDR}")
        print(f"💰 Confirmed Balance: {float(bal)/10**18:.4f} FET")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return

    if int(bal) == 0:
        print("🛑 Still 0.0. This node might be out of sync. Trying one last check...")
        return

    for seed in SUB_SEEDS:
        target_addr = get_fetch_address(seed)
        try:
            print(f"⛽ Sending to {target_addr[:15]}...")
            tx = ledger.send_tokens(target_addr, FUEL_AMOUNT, "afet", banker_ident)
            await wait_for_tx_to_complete(tx.tx_hash, ledger)
            print(f"✅ Success: {tx.tx_hash[:10]}")
            await asyncio.sleep(1)
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(final_fuel_run())
