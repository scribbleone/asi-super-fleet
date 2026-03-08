import os
import asyncio
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet

# PASTE YOUR KNOWN 9.6 FET ADDRESS HERE
TARGET_ADDRESS = "fetch1epm9ukcjq6dujv7pgerqnnlzu4k5nxrxjaq07x" 

def clean_mobile_seed(raw_seed):
    return " ".join(raw_seed.split()).lower()

async def targeted_audit():
    seeds_to_check = ["AGENT_SEED", "AGENT_SEED_GAS"]
    ledger = LedgerClient(NetworkConfig.fetch_mainnet())
    
    print(f"--- 🎯 TARGETED AUDIT: HUNTING FOR {TARGET_ADDRESS} ---")
    
    for seed_name in seeds_to_check:
        raw_val = os.getenv(seed_name, "")
        if not raw_val: continue
            
        clean_seed = clean_mobile_seed(raw_val)
        print(f"🔍 Deep scanning {seed_name}...")
        
        # We are going to check the first 50 possible wallet indexes
        for i in range(50):
            # Checking both Fetch.ai (118) and Ethereum (60) derivation styles
            for coin_type in ["118", "60"]:
                path = f"m/44'/{coin_type}'/0'/0/{i}"
                try:
                    wallet = LocalWallet.from_mnemonic(clean_seed, derivation_path=path)
                    address = str(wallet.address())
                    
                    if address == TARGET_ADDRESS:
                        balance = ledger.query_bank_balance(address) / 10**18
                        print(f"🎯 MATCH FOUND!")
                        print(f"   📂 Secret: {seed_name}")
                        print(f"   🛣️ Path: {path}")
                        print(f"   💰 Balance: {balance} FET")
                        return # Stop once we find it
                except:
                    continue
                    
    print("--- 🏁 SCAN COMPLETE: NO MATCH FOUND ---")
    print("If no match, the seed in your Secrets may not be the one for that address.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(targeted_audit())
    
