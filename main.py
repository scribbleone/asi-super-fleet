import asyncio
from uagents.network import wait_for_tx_to_complete
from uagents.crypto import Identity
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# --- 🎯 THE MASTER ACCESS ---
# Put your 12 words here exactly as they are written (e.g. "lorry apple...")
SECRET_PHRASE = "brown lorry mountain eye bolt raise blend grave house field muck din" 
FUNDED_ADDR = "fetch1epm9ukcjq6dujv7pgerqnnlzu4k5nxrxjaq07x"

# Fleet targets (Sub-agents)
SUB_SEEDS = [
    "alpha_nexus_v26_secure_102", "alpha_orbit_v26_secure_554", "alpha_pulse_v26_secure_923", 
    "alpha_glory_v26_secure_317", "alpha_delta_v26_secure_441", "alpha_titan_v26_secure_609", 
    "alpha_solar_v26_secure_228", "alpha_zenith_v26_secure_773", "alpha_matrix_v26_secure_415", 
    "beta_prime_v26_secure_119", "beta_nexus_v26_secure_802", "beta_orbit_v26_secure_334", 
    "beta_pulse_v26_secure_772", "beta_glory_v26_secure_515", "beta_delta_v26_secure_661", 
    "beta_titan_v26_secure_209", "beta_solar_v26_secure_882", "beta_zenith_v26_secure_337", 
    "beta_matrix_v26_secure_551"
]

MAINNET_CONFIG = NetworkConfig(
    chain_id="fetchhub-4",
    url="grpc+https://grpc-fetchhub.fetch.ai:443",
    fee_minimum_gas_price=5000000000,
    fee_denomination="afet",
    staking_denomination="afet",
)
ledger = LedgerClient(MAINNET_CONFIG)
FUEL_AMOUNT = 50000000000000000 # 0.05 FET

async def main():
    print("🎬 STARTING FLEET FUELING...")
    
    # 1. DERIVE BANKER
    # We use Identity.from_seed because "lorry" isn't a standard BIP39 word
    ident = Identity.from_seed(SECRET_PHRASE, 0)
    banker_wallet = LocalWallet(PrivateKey(bytes.fromhex(ident.private_key)), prefix="fetch")
    
    derived_addr = str(banker_wallet.address())
    print(f"🔎 Derived: {derived_addr}")
    
    if derived_addr != FUNDED_ADDR:
        print(f"❌ MISMATCH! Seed produced {derived_addr} instead of {FUNDED_ADDR}")
        return

    # 2. CHECK BALANCE
    bal = ledger.query_bank_balance(derived_addr)
    print(f"💰 Balance Found: {float(bal)/10**18:.4f} FET")

    # 3. FUELING LOOP
    for i, seed in enumerate(SUB_SEEDS):
        target_id = Identity.from_seed(seed, 0)
        target_wallet = LocalWallet(PrivateKey(bytes.fromhex(target_id.private_key)), prefix="fetch")
        target_addr = str(target_wallet.address())
        
        try:
            print(f"⛽ [{i+1}/20] Sending to {target_addr[:15]}...")
            tx = ledger.send_tokens(target_addr, FUEL_AMOUNT, "afet", banker_wallet)
            await wait_for_tx_to_complete(tx.tx_hash, ledger)
            print(f"✅ Confirmed: {tx.tx_hash[:10]}")
            await asyncio.sleep(1)
        except Exception as e:
            print(f"⚠️ Error: {e}")

    print("🏁 FINISHED.")

if __name__ == "__main__":
    asyncio.run(main())
