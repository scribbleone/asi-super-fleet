# --- 🎯 THE MASTER ACCESS ---
# Put your 12 words here EXACTLY as they are written
SECRET_PHRASE = "just done free bush call angry hip juice pine sky salt cactus" 

FUNDED_ADDR = "fetch1epm9ukcjq6dujv7pgerqnnlzu4k5nxrxjaq07x"

# ... (keep the rest of the script the same, but update the wallet loader below)

async def run_fleet_fueling():
    # Change the banker_wallet line to this:
    ident = Identity.from_seed(SECRET_PHRASE, 0)
    banker_wallet = LocalWallet(PrivateKey(bytes.fromhex(ident.private_key)), prefix="fetch")
    
    current_addr = str(banker_wallet.address())
    print(f"✨ Derived Address: {current_addr}")
    
    # Rest of the code...
    
