import asyncio
import os
import shutil
from uagents.network import wait_for_tx_to_complete
from uagents.crypto import Identity
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# --- 🎯 THE MASTER ACCESS ---
# PASTE YOUR 12 WORDS BETWEEN THE QUOTES BELOW (Line 12)
# Example: "apple banana cherry..."
MNEMONIC_PHRASE = "brown lorry mountain eye bolt raise blend grave house field muck din" 

FUNDED_ADDR = "fetch1epm9ukcjq6dujv7pgerqnnlzu4k5nxrxjaq07x"

MAINNET_CONFIG = NetworkConfig(
    chain_id="fetchhub-4",
    url="grpc+https://grpc-fetchhub.fetch.ai:443",
    fee_minimum_gas_price=5000000000,
    fee_denomination="afet",
    staking_denomination="afet",
)
ledger = LedgerClient(MAINNET_CONFIG)

# The 20-Agent Fleet Seeds
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

async def run_fleet_fueling():
    print(f"🚀 Initializing Mnemonic Recovery for {FUNDED_ADDR}...")

    if not os.path.exists("main.py.bak"):
        shutil.copy("main.py", "main.py.bak")
        print("📁 Backup created.")

    try:
        # Load the banker wallet from the 12-word mnemonic
        # This uses the standard BIP44 path: m/44'/118'/0'/0/0
        banker_wallet = LocalWallet.from_mnemonic(MNEMONIC_PHRASE, prefix="fetch")
        current_addr = str(banker_wallet.address())
        
        print(f"✨ Wallet Address Derived: {current_addr}")

        if current_addr != FUNDED_ADDR:
            print(f"🛑 MISMATCH! Derived {current_addr}, but we need {FUNDED_ADDR}")
            print("Double-check your 12 words and their order.")
            return

        balance = ledger.query_bank_balance(current_addr)
        print(f"💰 Confirmed Balance: {float(balance)/10**18:.4f} FET")

        # Fueling logic
        for i, sub_seed in enumerate(SUB_SEEDS):
            # We keep sub-agents on the v26_secure seeds for now
            target_ident = Identity.from_seed(sub_seed, 0)
            target_priv = PrivateKey(bytes.fromhex(target_ident.private_key))
            target_wallet = LocalWallet(target_priv, prefix="fetch")
            target_addr = str(target_wallet.address())
            
            try:
                print(f"⛽ [{i+1}/20] Sending 0.05 FET to {target_addr[:20]}...")
                tx = ledger.send_tokens(target_addr, FUEL_AMOUNT, "afet", banker_wallet)
                await wait_for_tx_to_complete(tx.tx_hash, ledger)
                print(f"✅ Success: {tx.tx_hash[:12]}")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"⚠️ Error on agent {i+1}: {e}")

    except Exception as e:
        print(f"❌ Critical Error: {e}")

if __name__ == "__main__":
    asyncio.run(run_fleet_fueling())
