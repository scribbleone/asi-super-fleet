import asyncio
from uagents.crypto import Identity
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# --- 🎯 THE TEST ZONE ---
SECRET_PHRASE = "brown lorry mountain eye bolt raise blend grave house field muck din" 
TARGET = "fetch1epm9ukcjq6dujv7pgerqnnlzu4k5nxrxjaq07x"

async def main():
    print(f"🕵️ Scanning derivation paths for: {TARGET}\n")

    # TEST 1: The "Identity" Method (uagents standard)
    # This treats the words as a single string.
    try:
        ident = Identity.from_seed(SECRET_PHRASE, 0)
        addr1 = str(LocalWallet(PrivateKey(bytes.fromhex(ident.private_key)), prefix="fetch").address())
        print(f"1. Identity String Method: {addr1} {'✅ MATCH!' if addr1 == TARGET else '❌'}")
    except: print("1. Identity Method: Failed to run")

    # TEST 2: The "BIP39 Mnemonic" Method (Keplr/Fetch Wallet standard)
    # This treats the words as a formal recovery phrase.
    try:
        # We use a safe way to check even if 'lorry' isn't in the official wordlist
        wallet2 = LocalWallet.from_mnemonic(SECRET_PHRASE, prefix="fetch")
        addr2 = str(wallet2.address())
        print(f"2. BIP39 Mnemonic Method: {addr2} {'✅ MATCH!' if addr2 == TARGET else '❌'}")
    except Exception as e:
        print(f"2. BIP39 Mnemonic Method: ❌ (Error: {e})")

    # TEST 3: The "Legacy Identity" Method
    # Sometimes index 1 or a different account is used by accident.
    try:
        ident3 = Identity.from_seed(SECRET_PHRASE, 1)
        addr3 = str(LocalWallet(PrivateKey(bytes.fromhex(ident3.private_key)), prefix="fetch").address())
        print(f"3. Identity (Index 1) Method: {addr3} {'✅ MATCH!' if addr3 == TARGET else '❌'}")
    except: print("3. Identity (Index 1): Failed to run")

    print("\n💡 If all are ❌, try your OTHER 12-word phrase in this same script.")

if __name__ == "__main__":
    asyncio.run(main())
