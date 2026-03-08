import os
import asyncio
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet

def clean_mobile_seed(raw_seed):
    # THE SCRIBBLE 2 SYNC BRIDGE LOGIC
    # Removes mobile browser distortion and hidden characters
    return " ".join(raw_seed.split()).lower()

async def deep_audit():
    seeds_to_check = ["AGENT_SEED", "AGENT_SEED_GAS", "MASTER_WALLET_SEED"]
    ledger = LedgerClient(NetworkConfig.fetch_mainnet())
    
    # We will try the two most likely mathematical routes for your wallet
    paths = ["m/44'/118'/0'/0/0", "m/44'/60'/0'/0/0"]
    
    print("--- 🛡️ ALPHA DEEP AUDIT: SCRIBBLE SYNC ---")
    
    for seed_name in seeds_to_check:
        raw_val = os.getenv(seed_name, "")
        if not raw_val:
            print(f"⚠️ {seed_name}: Secret is empty in GitHub.")
            continue
            
        # Apply the Scribble 2 Bridge cleaning
        clean_seed = clean_mobile_seed(raw_val)
        print(f"🔍 Probing {seed_name} (Cleaned)...")
        
        for path in paths:
            try:
                # Standard BIP39 math (Matches ASI Alliance App)
                wallet = LocalWallet.from_mnemonic(clean_seed, derivation_path=path)
                address = str(wallet.address())
                balance = ledger.query_bank_balance(address)
                
                print(f"   👉 Path {path}:")
                print(f"      📍 {address}")
                print(f"      💰 {balance / 10**18} FET")
                
                if (balance / 10**18) > 1:
                    print(f"🎯 BINGO! Found your funds in {seed_name}!")
            except Exception as e:
                continue

    print("--- 🏁 DEEP AUDIT COMPLETE ---")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(deep_audit())
    
