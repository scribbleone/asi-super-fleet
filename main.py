import asyncio, bech32
from uagents.network import wait_for_tx_to_complete
from uagents.crypto import Identity
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# --- 🎯 THE LOCKED TRUTH ---
FUNDED_ADDR = "fetch1epm9ukcjq6dujv7pgerqnnlzu4k5nxrxjaq07x"
BANKER_SEED = "alpha_prime_v26_secure_881"

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

def to_fetch_addr(agent_addr):
    hrp, data = bech32.bech32_decode(agent_addr)
    return bech32.bech32_encode("fetch", data)

async def final_fuel_run():
    print(f"🔎 Deep-searching paths for {FUNDED_ADDR}...")
    banker_wallet = None
    
    # We check indices 0-10 across common paths
    for i in range(11):
        # Path A: Standard uAgents path
        ident_a = Identity.from_seed(BANKER_SEED, i)
        if to_fetch_addr(ident_a.address) == FUNDED_ADDR:
            print(f"✅ Found! Path: Standard, Index: {i}")
            banker_wallet = LocalWallet(PrivateKey(bytes.fromhex(ident_a.private_key)))
            break

        # Path B: Alternative wallet path (checking if library allows)
        # Note: If this fails, we will try a manual cosmpy derivation in the next step
        
    if not banker_wallet:
        print("🛑 Still not found. Let's check the absolute default index 0 one last time.")
        ident_zero = Identity.from_seed(BANKER_SEED, 0)
        print(f"Index 0 actually derives: {to_fetch_addr(ident_zero.address)}")
        return

    bal = ledger.query_bank_balance(FUNDED_ADDR)
    print(f"💰 Confirmed Balance: {float(bal)/10**18:.4f} FET")

    for seed in SUB_SEEDS:
        target_addr = to_fetch_addr(Identity.from_seed(seed, 0).address)
        try:
            print(f"⛽ Sending 0.05 to {target_addr[:15]}...")
            tx = ledger.send_tokens(target_addr, FUEL_AMOUNT, "afet", banker_wallet)
            await wait_for_tx_to_complete(tx.tx_hash, ledger)
            print(f"✅ Success: {tx.tx_hash[:10]}")
            await asyncio.sleep(1) 
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(final_fuel_run())
