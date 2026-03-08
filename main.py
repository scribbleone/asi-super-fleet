import os
import asyncio
# THE 2026 STANDARD FOR FETCH.AI AUDITS
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

async def audit_all_seeds():
    seeds_to_check = ["AGENT_SEED", "AGENT_SEED_GAS", "MASTER_WALLET_SEED"]
    
    # Connect to the official Fetch.ai Mainnet
    ledger = LedgerClient(NetworkConfig.fetchai_mainnet())
    
    print("--- 🛡️ ALPHA MULTI-AUDIT STARTING ---")
    
    for seed_name in seeds_to_check:
        seed_value = os.getenv(seed_name)
        
        if not seed_value:
            print(f"⚠️ {seed_name}: Not found in GitHub Secrets.")
            continue
            
        try:
            # Generate the wallet from your seed
            # Note: Fetch.ai SDK uses 32-byte hex or specific phrase formats
            private_key = PrivateKey(bytes.fromhex(seed_value) if len(seed_value) == 64 else seed_value.encode())
            wallet = LocalWallet(private_key)
            address = str(wallet.address())
            
            # The exact command to find your 9.6 FET
            balance = ledger.query_bank_balance(address)
            
            print(f"✅ FOUND {seed_name}")
            print(f"   📍 Address: {address}")
            print(f"   💰 Balance: {balance / 10**18} FET") 
        except Exception as e:
            print(f"❌ {seed_name} Check Failed: Ensure your Secret is a valid Seed Phrase or Hex.")

    print("--- 🏁 AUDIT COMPLETE ---")

if __name__ == "__main__":
    asyncio.run(audit_all_seeds())
    
