import os
import asyncio
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet

async def deep_audit():
    # The secrets we are hunting for
    seeds_to_check = ["AGENT_SEED", "AGENT_SEED_GAS", "MASTER_WALLET_SEED"]
    ledger = LedgerClient(NetworkConfig.fetch_mainnet())
    
    # Common "Mathematical Routes" (Derivation Paths)
    # 118 = Fetch.ai / 60 = Ethereum / 118 (index 1) = Second Account
    paths = ["m/44'/118'/0'/0/0", "m/44'/60'/0'/0/0", "m/44'/118'/1'/0/0"]
    
    print("--- 🛡️ ALPHA DEEP AUDIT STARTING ---")
    
    for seed_name in seeds_to_check:
        seed_value = os.getenv(seed_name, "").strip()
        if not seed_value: continue
            
        print(f"🔍 Probing {seed_name}...")
        
        for path in paths:
            try:
                # We try to derive the wallet using the specific path
                wallet = LocalWallet.from_mnemonic(seed_value, derivation_path=path)
                address = str(wallet.address())
                balance = ledger.query_bank_balance(address)
                
                print(f"   👉 Route {path}:")
                print(f"      📍 {address}")
                print(f"      💰 {balance / 10**18} FET")
                
                if (balance / 10**18) > 1:
                    print(f"🎯 BINGO! Found significant balance in {seed_name} using {path}!")
            except Exception:
                continue

    print("--- 🏁 DEEP AUDIT COMPLETE ---")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(deep_audit())
    
