import asyncio
from uagents.crypto import Identity
from cosmpy.aerial.client import LedgerClient, NetworkConfig

# THE TARGET WALLET
TARGET_ADDR = "fetch1epm9ukcjq6dujv7pgerqnnlzu4k5nxrxjaq07x"

# YOUR FLEET LIST
AGENT_SEEDS = {
    "Alpha 1": "alpha_prime_v26_secure_881",
    "Alpha 2": "alpha_nexus_v26_secure_102",
    "Alpha 3": "alpha_orbit_v26_secure_554",
    "Alpha 4": "alpha_pulse_v26_secure_923",
    "Alpha 5": "alpha_glory_v26_secure_317",
    "Alpha 6": "alpha_delta_v26_secure_441",
    "Alpha 7": "alpha_titan_v26_secure_609",
    "Alpha 8": "alpha_solar_v26_secure_228",
    "Alpha 9": "alpha_zenith_v26_secure_773",
    "Alpha 10": "alpha_matrix_v26_secure_415"
}

async def check_alpha_fleet():
    ledger = LedgerClient(NetworkConfig.fetch_mainnet())
    print(f"--- 🛡️ ALPHA FLEET AUDIT ---")
    print(f"HUNTING FOR: {TARGET_ADDR}\n")

    for name, seed_string in AGENT_SEEDS.items():
        # Generate the identity exactly how uagents does it
        agent_identity = Identity.from_seed(seed_string, 0)
        address = str(agent_identity.address)
        
        if address == TARGET_ADDR:
            print(f"🎯 MATCH FOUND: {name} is the owner!")
            balance = ledger.query_bank_balance(address) / 10**18
            print(f"💰 Balance: {balance} FET")
            return
        else:
            print(f"🔎 {name} generates: {address}")

    print("\n❌ Alpha 1 through 10 did not match that address.")
    print("If it's definitely Alpha 1, the seed string might be slightly different in your Replit.")

if __name__ == "__main__":
    asyncio.run(check_alpha_fleet())
    
