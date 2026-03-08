import os
import asyncio
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet

def clean_mobile_seed(raw_seed):
    # THE SCRIBBLE 2 SYNC BRIDGE logic to fix mobile distortion
    return " ".join(raw_seed.split()).lower()

async def wide_net_audit():
    seeds_to_check = ["AGENT_SEED", "AGENT_SEED_GAS", "MASTER_WALLET_SEED"]
    ledger = LedgerClient(NetworkConfig.fetch_mainnet())
    
    # We are checking 10 different "mathematical rooms"
    # Includes Fetch.ai (118) and Ethereum (60) styles across multiple account indexes
    paths = [
        "m/44'/118'/0'/0/0", "m/44'/118'/1'/0/0", "m/44'/118'/0'/0/1",
        "m/44'/60'/0'/0/0", "m/44'/60'/1'/0/0", "m/44'/60'/0'/0/1",
        "m/44'/118'/0'/1", "m/44'/118'/0'/0", "m/44'/60'/0'/1", "m/44'/60'/0'/0"
    ]
    
    print("--- 🛡️ ALPHA WIDE-NET AUDIT ---")
    
    for seed_name in seeds_to_check:
        raw_val = os.getenv(seed_name, "")
        if not raw_val: continue
            
        clean_seed = clean_mobile_seed(raw_val)
        print(f"🔍 Probing {seed_name} across 10 paths...")
        
        for path in paths:
            try:
                wallet = LocalWallet.from_mnemonic(clean_seed, derivation_path=path)
                address = str(wallet.address())
                balance_query = ledger.query_bank_balance(address)
                balance = balance_query / 10**18
                
                # We only print if there is ANY money found to keep the log clean
                if balance > 0:
                    print(f"   💰 FOUND: {balance} FET")
                    print(f"      📍 Path: {path}")
                    print(f"      🔗 Addr: {address}")
                    
                if balance > 5:
                    print(f"🎯 TARGET ACQUIRED: This is your 9.6 FET wallet!")
            except:
                continue

    print("--- 🏁 WIDE-NET COMPLETE ---")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wide_net_audit())
    
