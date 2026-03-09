import asyncio
from uagents.crypto import Identity
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# --- 🎯 THE TARGET ---
FUNDED_ADDR = "fetch1epm9ukcjq6dujv7pgerqnnlzu4k5nxrxjaq07x"
# Try your primary 12-word phrase here
SEED_PHRASE = "brown lorry mountain eye bolt raise blend grave house field muck din" 

async def recover_agent_route():
    print(f"🕵️ Searching for route to {FUNDED_ADDR}...\n")

    # PATH A: The "Direct Mnemonic" Route (Standard Wallet)
    try:
        w_a = LocalWallet.from_mnemonic(SEED_PHRASE, prefix="fetch")
        addr_a = str(w_a.address())
        print(f"Path A (Standard Mnemonic): {addr_a}")
        if addr_a == FUNDED_ADDR: print("✅ MATCH FOUND IN PATH A!")
    except: pass

    # PATH B: The "Identity String" Route (Default uagents)
    try:
        ident_b = Identity.from_seed(SEED_PHRASE, 0)
        w_b = LocalWallet(PrivateKey(bytes.fromhex(ident_b.private_key)), prefix="fetch")
        addr_b = str(w_b.address())
        print(f"Path B (Identity String):   {addr_b}")
        if addr_b == FUNDED_ADDR: print("✅ MATCH FOUND IN PATH B!")
    except: pass

    # PATH C: The "Legacy Ledger" Route
    try:
        from cosmpy.crypto.address import Address
        ident_c = Identity.from_seed(SEED_PHRASE, 0)
        # This checks if the prefixing is causing the 'scramble'
        addr_c = Address(bytes.fromhex(ident_c.address), prefix="fetch")
        print(f"Path C (Legacy Prefix):     {addr_c}")
        if str(addr_c) == FUNDED_ADDR: print("✅ MATCH FOUND IN PATH C!")
    except: pass

if __name__ == "__main__":
    asyncio.run(recover_agent_route())
