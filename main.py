import asyncio
from uagents import Model
from uagents.crypto import Identity

# THE FULL FLEET LIST
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
    "Alpha 10": "alpha_matrix_v26_secure_415",
    "Beta 1": "beta_prime_v26_secure_119",
    "Beta 2": "beta_nexus_v26_secure_802",
    "Beta 3": "beta_orbit_v26_secure_334",
    "Beta 4": "beta_pulse_v26_secure_772",
    "Beta 5": "beta_glory_v26_secure_515",
    "Beta 6": "beta_delta_v26_secure_661",
    "Beta 7": "beta_titan_v26_secure_209",
    "Beta 8": "beta_solar_v26_secure_882",
    "Beta 9": "beta_zenith_v26_secure_337",
    "Beta 10": "beta_matrix_v26_secure_551"
}

TARGET_ADDR = "fetch1epm9ukcjq6dujv7pgerqnnlzu4k5nxrxjaq07x"

async def audit_fleet():
    print(f"--- 🛡️ FLEET AUDIT: 20 AGENTS ---")
    print(f"Targeting: {TARGET_ADDR}\n")
    
    found_any = False
    for name, seed in AGENT_SEEDS.items():
        # This replicates how uagents creates an identity from a string
        agent_identity = Identity.from_seed(seed, 0)
        address = agent_identity.address
        
        # Check if this matches our 9.6 FET wallet
        if str(address) == TARGET_ADDR:
            print(f"🎯 MATCH FOUND!")
            print(f"   🤖 Agent: {name}")
            print(f"   🔑 Seed String: {seed}")
            found_any = True
        else:
            # Optional: Print the address so you can see what it's generating
            print(f"🔎 {name}: {address}")

    if not found_any:
        print("\n❌ None of these 20 seeds match the 9.6 FET address.")
        print("This means the 9.6 FET wallet was likely made with a standard 12-word phrase, not these 'alpha_' strings.")

if __name__ == "__main__":
    asyncio.run(audit_fleet())
    
