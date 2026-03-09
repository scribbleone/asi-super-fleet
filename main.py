import asyncio
import os
import shutil
from uagents.network import wait_for_tx_to_complete
from uagents.crypto import Identity
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# --- 🎯 THE LOCKED TRUTH ---
FUNDED_ADDR = "fetch1epm9ukcjq6dujv7pgerqnnlzu4k5nxrxjaq07x"
BANKER_SEED = "alpha_prime_v26_secure_881"

# Mainnet Configuration for Fetch.ai
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

def get_standard_fetch_wallet(seed_string, index=0):
    """
    Forces the Identity to output a private key, then wraps it 
    into a standard 'fetch' prefix wallet to avoid Bech32m errors.
    """
    ident = Identity.from_seed(seed_string, index)
    priv_key = PrivateKey(bytes.fromhex(ident.private_key))
    return LocalWallet(priv_key, prefix="fetch")

async def run_fleet_fueling():
    print(f"🚀 Starting Fleet Fueling from {FUNDED_ADDR}...")

    # 1. Create a backup of main.py as requested
    if not os.path.exists("main.py.bak"):
        shutil.copy("main.py", "main.py.bak")
        print("📁 Backup created: main.py.bak")

    # 2. Initialize the Banker Wallet
    # We use index 0 because that's the standard for single-agent funding
    banker_wallet = get_standard_fetch_wallet(BANKER_SEED, 0)
    current_addr = str(banker_wallet.address())
    
    print(f"🔎 Checking derived address: {current_addr}")

    # 3. Validation Check
    if current_addr != FUNDED_ADDR:
        print(f"❌ ERROR: Derived address {current_addr} does not match funded address {FUNDED_ADDR}")
        print("Checking if you used a different index...")
        # Emergency scan of first 5 indices
        for i in range(1, 6):
            alt_wallet = get_standard_fetch_wallet(BANKER_SEED, i)
            if str(alt_wallet.address()) == FUNDED_ADDR:
                print(f"✅ Found match at Index {i}!")
                banker_wallet = alt_wallet
                break
        else:
            return

    # 4. Check Balance on Mainnet
    balance = ledger.query_bank_balance(str(banker_wallet.address()))
    print(f"💰 Confirmed Banker Balance: {float(balance)/10**18:.4f} FET")

    # 5. Fuel the Fleet
    for i, sub_seed in enumerate(SUB_SEEDS):
        target_wallet = get_standard_fetch_wallet(sub_seed, 0)
        target_addr = str(target_wallet.address())
        
        try:
            print(f"⛽ [{i+1}/20] Sending 0.05 FET to {target_addr[:20]}...")
            tx = ledger.send_tokens(target_addr, FUEL_AMOUNT, "afet", banker_wallet)
            
            # Wait for block confirmation
            await wait_for_tx_to_complete(tx.tx_hash, ledger)
            print(f"✅ Transaction Confirmed: {tx.tx_hash[:12]}")
            
            # Small delay to prevent sequence errors on the blockchain
            await asyncio.sleep(1)
            
        except Exception as e:
            print(f"⚠️ Failed to fuel agent {i+1}: {e}")

    print("\n🏁 Fleet Fueling Sequence Complete.")

if __name__ == "__main__":
    asyncio.run(run_fleet_fueling())
