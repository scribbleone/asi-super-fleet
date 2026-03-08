import asyncio
from uagents.crypto import Identity
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.aerial.client import LedgerClient, NetworkConfig

# THE PARENT WALLET WE NEED
TARGET_WALLET = "fetch1epm9ukcjq6dujv7pgerqnnlzu4k5nxrxjaq07x"

# THE SEED STRING YOU BELIEVE OWNS IT
ALPHA_1_SEED = "alpha_prime_v26_secure_881"

async def link_audit():
    ledger = LedgerClient(NetworkConfig.fetch_mainnet())
    print(f"--- 🛡️ ALPHA PARENT-LINK AUDIT ---")
    
    # 1. Check Agent Identity (The 'agent1...' address)
    agent_id = Identity.from_seed(ALPHA_1_SEED, 0)
    print(f"🤖 Agent 1 ID: {agent_id.address}")
    
    # 2. Check if the seed string acts as a direct Wallet Private Key
    # We try different math 'routes' to see if this string creates the fetch1... address
    print(f"🔍 Searching for Parent Wallet: {TARGET_WALLET}...")
    
    try:
        # We test if the string itself is the secret to the fetch1 wallet
        wallet = LocalWallet.from_mnemonic(ALPHA_1_SEED)
        if str(wallet.address()) == TARGET_WALLET:
            print(f"🎯 MATCH FOUND! The string is the direct Seed Phrase.")
            return
    except:
        pass

    # 3. If no direct match, check for funds in the Agent ID itself
    try:
        bal = ledger.query_bank_balance(str(agent_id.address)) / 10**18
        print(f"💰 Agent 1 Balance: {bal} FET")
    except:
        print("💰 Agent 1 Balance: 0.0 FET")

    print("\n--- 🏁 AUDIT COMPLETE ---")
    print("If no match, the 9.6 FET is in a wallet created by a 12-word phrase,")
    print("not the 'alpha_prime...' string.")

if __name__ == "__main__":
    asyncio.run(link_audit())
    
