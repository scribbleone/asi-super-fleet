import asyncio
import os
from uagents.crypto import Identity
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# --- 🎯 THE VAULT ACCESS ---
# This looks for a GitHub Secret. If it doesn't find one, it uses a fallback.
SECRET_FROM_GITHUB = os.environ.get("AGENT_SEED", "NOT_FOUND")
TARGET_ADDR = "fetch1epm9ukcjq6dujv7pgerqnnlzu4k5nxrxjaq07x"

async def main():
    print(f"📡 Attempting to pull key from GitHub Secrets...")
    
    if SECRET_FROM_GITHUB == "NOT_FOUND":
        print("❌ ERROR: No secret found in the environment.")
        print("Make sure you added 'AGENT_SEED' to your GitHub Secrets AND the YAML file.")
        return

    # Try to turn that secret into our funded address
    ident = Identity.from_seed(SECRET_FROM_GITHUB, 0)
    banker_wallet = LocalWallet(PrivateKey(bytes.fromhex(ident.private_key)), prefix="fetch")
    
    derived = str(banker_wallet.address())
    print(f"🔎 Derived from Secret: {derived}")
    
    if derived == TARGET_ADDR:
        print("✅ SUCCESS! The secret matches the funded wallet.")
    else:
        print("❌ MISMATCH. The secret held a different key.")

if __name__ == "__main__":
    asyncio.run(main())
