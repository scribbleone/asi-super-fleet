import os
import asyncio
import time
# UPDATED IMPORTS FOR 2026 LIBRARIES
from fetchai import Ledger
from fetchai.crypto import Identity

async def audit_all_seeds():
    # The List of Secrets we are hunting for
    seeds_to_check = ["AGENT_SEED", "AGENT_SEED_GAS", "MASTER_WALLET_SEED"]
    
    # Setup the Ledger (Mainnet)
    ledger = Ledger() 
    start_time = time.time()
    
    print("--- 🛡️ ALPHA MULTI-AUDIT STARTING ---")
    
    for seed_name in seeds_to_check:
        seed_value = os.getenv(seed_name)
        
        if not seed_value:
            print(f"⚠️ {seed_name}: Not found in GitHub Secrets.")
            continue
            
        try:
            # Create the identity from the seed
            identity = Identity.from_seed(seed_value)
            address = identity.address
            # Query the balance
            balance = ledger.query_bank_balance(address)
            
            print(f"✅ FOUND {seed_name}")
            print(f"   📍 Address: {address}")
            print(f"   💰 Balance: {balance} FET")
        except Exception as e:
            print(f"❌ Error auditing {seed_name}: {str(e)}")

    print(f"--- 🏁 AUDIT COMPLETE (Took {int(time.time() - start_time)}s) ---")

if __name__ == "__main__":
    asyncio.run(asyncio.wait_for(audit_all_seeds(), timeout=120))
    
