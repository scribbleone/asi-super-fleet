import os
import asyncio
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet

TARGET_ADDRESS = "fetch1epm9ukcjq6dujv7pgerqnnlzu4k5nxrxjaq07x"

def clean_mobile_seed(raw_seed):
    # THE SCRIBBLE 2 SYNC BRIDGE logic
    return " ".join(raw_seed.split()).lower()

async def final_audit():
    seeds_to_check = ["AGENT_SEED", "AGENT_SEED_GAS", "MASTER_WALLET_SEED"]
    ledger = LedgerClient(NetworkConfig.fetch_mainnet())
    
    print(f"--- 🛡️ ALPHA FINAL VERIFICATION ---")
    print(f"HUNTING FOR: {TARGET_ADDRESS}")
    
    for seed_name in seeds_to_check:
        raw_val = os.getenv(seed_name, "")
        if not raw_val: continue
            
        clean_seed = clean_mobile_seed(raw_val)
        words = clean_seed.split()
        
        # Verify the seed is valid (usually 12 or 24 words)
        if len(words) < 12:
            print(f"❌ {seed_name}: Only {len(words)} words found. Incomplete seed.")
            continue

        # Safety Check: Show first 3 words to verify it's the right phrase
        print(f"🔍 {seed_name} starts with: '{words[0]} {words[1]} {words[2]}...'")
        
        # Check standard Fetch and Ethereum paths
        for path in ["m/44'/118'/0'/0/0", "m/44'/60'/0'/0/0"]:
            try:
                wallet = LocalWallet.from_mnemonic(clean_seed, derivation_path=path)
                address = str(wallet.address())
                if address == TARGET_ADDRESS:
                    balance = ledger.query_bank_balance(address) / 10**18
                    print(f"🎯 MATCH FOUND at {path}!")
                    print(f"💰 Balance: {balance} FET")
                    return
            except Exception:
                continue
                
    print("--- 🏁 VERIFICATION COMPLETE ---")
    print("If you don't see a match, the seed in GitHub is not for the 9.6 FET wallet.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(final_audit())
    
