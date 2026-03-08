import os
import asyncio
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet

TARGET_ADDRESS = "fetch1epm9ukcjq6dujv7pgerqnnlzu4k5nxrxjaq07x"

def clean_mobile_seed(raw_seed):
    # THE SCRIBBLE 2 SYNC BRIDGE logic to fix mobile distortion
    return " ".join(raw_seed.split()).lower()

async def audit_hunt():
    # Adding the new AUDIT secret to our hunt list
    seeds_to_check = ["AGENT_SEED", "AGENT_SEED_GAS", "MASTER_WALLET_SEED", "AGENT_SEED_AUDIT"]
    ledger = LedgerClient(NetworkConfig.fetch_mainnet())
    
    print(f"--- 🛡️ ALPHA RECOVERY HUNT ---")
    print(f"TARGET: {TARGET_ADDRESS}")
    
    for seed_name in seeds_to_check:
        raw_val = os.getenv(seed_name, "")
        if not raw_val:
            continue
            
        clean_seed = clean_mobile_seed(raw_val)
        print(f"🔍 Probing {seed_name}...")
        
        # Check standard Fetch (118) and Ethereum (60) paths
        for path in ["m/44'/118'/0'/0/0", "m/44'/60'/0'/0/0"]:
            try:
                wallet = LocalWallet.from_mnemonic(clean_seed, derivation_path=path)
                address = str(wallet.address())
                
                if address == TARGET_ADDRESS:
                    balance = ledger.query_bank_balance(address) / 10**18
                    print(f"🎯 MATCH FOUND IN {seed_name}!")
                    print(f"   🛣️ Path: {path}")
                    print(f"   💰 Balance: {balance} FET")
                    return
            except:
                continue

    print("--- 🏁 HUNT COMPLETE: NO MATCH FOUND ---")
    print("If no match, the 9.6 FET seed is still not in your GitHub Secrets.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(audit_hunt())
    
