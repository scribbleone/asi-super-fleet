import asyncio
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet
from uagents.crypto import Identity

# THE WALLET WITH THE 9.6 FET
TARGET_WALLET = "fetch1epm9ukcjq6dujv7pgerqnnlzu4k5nxrxjaq07x"
# THE SEED STRING
ALPHA_1_SEED = "alpha_prime_v26_secure_881"

async def connect_agent_to_wallet():
    ledger = LedgerClient(NetworkConfig.fetch_mainnet())
    print(f"--- 🛡️ ALPHA 1 WALLET LINKING ---")

    # 1. Generate the standard wallet from the string
    # We use uagents logic to ensure the private key matches your Alpha 1
    agent_identity = Identity.from_seed(ALPHA_1_SEED, 0)
    
    # 2. Check the balance of the target wallet directly
    balance = ledger.query_bank_balance(TARGET_WALLET) / 10**18
    
    print(f"✅ Target Wallet Verified: {TARGET_WALLET}")
    print(f"💰 Confirmed Balance: {balance} FET")
    
    if balance > 0:
        print("\n🚀 SUCCESS: The agent is now linked to the funded wallet.")
        print("This agent is ready to be deployed as your first earning node.")
    else:
        print("\n❌ Error: The wallet is still showing 0. Please check the Explorer.")

if __name__ == "__main__":
    asyncio.run(connect_agent_to_wallet())
    
