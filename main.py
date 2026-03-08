import os
import asyncio
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet

async def audit_all_seeds():
    # The secrets we are hunting for
    seeds_to_check = ["AGENT_SEED", "AGENT_SEED_GAS", "MASTER_WALLET_SEED"]
    
    # Connect to Fetch.ai Mainnet
    ledger = LedgerClient(NetworkConfig.fetch_mainnet())
    
    print("--- 🛡️ ALPHA MULTI-AUDIT STARTING ---")
    
    for seed_name in seeds_to_check:
        seed_value = os.getenv(seed_name)
        
        if not seed_value or len(seed_value.strip()) < 5:
            print(f"⚠️ {seed_name}: Empty or not found.")
            continue
            
        try:
            # Create wallet from mnemonic seed phrase
            wallet = LocalWallet.from_mnemonic(seed_value)
            address = str(wallet.address())
            
            # Query the balance
            balance = ledger.query_bank_balance(address)
            
            print(f"✅ FOUND {seed_name}")
            print(f"   📍 Address: {address}")
            print(f"   💰 Balance: {balance / 10**18} FET")
            
        except Exception as e:
            # If it's not a mnemonic, try treating it as a direct Private Key
            try:
                from cosmpy.crypto.keypairs import PrivateKey
                priv_key = PrivateKey(bytes.fromhex(seed_value) if len(seed_value) == 64 else seed_value.encode())
                wallet = LocalWallet(priv_key)
                address = str(wallet.address())
                balance = ledger.query_bank_balance(address)
                print(f"✅ FOUND {seed_name} (Private Key)")
                print(f"   📍 Address: {address}")
                print(f"   💰 Balance: {balance / 10**18} FET")
            except:
                print(f"❌ {seed_name}: Could not decode seed/key format.")

    print("--- 🏁 AUDIT COMPLETE ---")

if __name__ == "__main__":
    # Standard 2026 async execution
    loop = asyncio.get_event_loop()
    loop.run_until_complete(audit_all_seeds())
            
