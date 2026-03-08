import os
import asyncio
import time
from fetchai.ledger.api import LedgerApi
from fetchai.ledger.crypto import Entity

async def audit_all_seeds():
    # 1. The List of Secrets we are hunting for
    seeds_to_check = ["AGENT_SEED", "AGENT_SEED_GAS", "MASTER_WALLET_SEED"]
    
    # 2. Setup the Ledger (Mainnet)
    ledger = LedgerApi('mainnet.fetch.ai', 443)
    start_time = time.time()
    
    print("--- 🛡️ ALPHA MULTI-AUDIT STARTING ---")
    
    for seed_name in seeds_to_check:
        seed_value = os.getenv(seed_name)
        
        if not seed_value:
            print(f"⚠️ {seed_name}: Not found in GitHub Secrets.")
            continue
            
        try:
            # Create the entity from the seed
            entity = Entity.from_seed(seed_value)
            address = str(entity.address)
            balance = ledger.query_funds(entity)
            
            print(f"✅ FOUND {seed_name}")
            print(f"   📍 Address: {address}")
            print(f"   💰 Balance: {balance / 10**18} FET") # Converting from 'atto' to FET
        except Exception as e:
            print(f"❌ Error auditing {seed_name}: {str(e)}")

    print(f"--- 🏁 AUDIT COMPLETE (Took {int(time.time() - start_time)}s) ---")
    print("Shutting down to save GitHub minutes...")

if __name__ == "__main__":
    # Run the audit with a 120-second hard timeout
    try:
        asyncio.run(asyncio.wait_for(audit_all_seeds(), timeout=120))
    except asyncio.TimeoutError:
        print("⏰ Timeout reached. Closing agent.")
        
