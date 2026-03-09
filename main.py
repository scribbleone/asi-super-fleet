import asyncio
from uagents.network import wait_for_tx_to_complete
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet

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

FUEL_AMOUNT = 50000000000000000 # 0.05 FET

async def final_fuel_run():
    print(f"🔗 Accessing Standard Wallet for {FUNDED_ADDR}...")
    
    try:
        # Direct initialization - usually matches m/44'/118'/0'/0/0
        banker_wallet = LocalWallet.from_mnemonic(BANKER_SEED)
        derived_addr = str(banker_wallet.address())
        print(f"✨ Derived Address: {derived_addr}")

        if derived_addr != FUNDED_ADDR:
            print(f"⚠️ Mismatch! Derived {derived_addr} but need {FUNDED_ADDR}")
            print("Let's try deriving with the alternative prefix...")
            # Some versions of cosmpy might need an explicit prefix if 'fetch' isn't default
            banker_wallet = LocalWallet.from_mnemonic(BANKER_SEED, prefix="fetch")
            derived_addr = str(banker_wallet.address())
            print(f"✨ New Derived Address: {derived_addr}")
            
        if derived_addr != FUNDED_ADDR:
            print("🛑 Still no match. The seed might be deriving a different account index.")
            return

        bal = ledger.query_bank_balance(derived_addr)
        print(f"💰 Confirmed Balance: {float(bal)/10**18:.4f} FET")

        for seed in SUB_SEEDS:
            # Fund sub-agents using the same standard derivation
            target_wallet = LocalWallet.from_mnemonic(seed, prefix="fetch")
            target_addr = str(target_wallet.address())
            try:
                print(f"⛽ Sending 0.05 to {target_addr[:15]}...")
                tx = ledger.send_tokens(target_addr, FUEL_AMOUNT, "afet", banker_wallet)
                await wait_for_tx_to_complete(tx.tx_hash, ledger)
                print(f"✅ Success: {tx.tx_hash[:10]}")
                await asyncio.sleep(1) 
            except Exception as e:
                print(f"❌ Error during transfer: {e}")

    except Exception as e:
        print(f"❌ General Error: {e}")

if __name__ == "__main__":
    asyncio.run(final_fuel_run())
