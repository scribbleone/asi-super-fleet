import os
from uagents import Agent, Context
from uagents.network import get_ledger
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# --- 🔒 THE COMMAND CENTER ---
HEX_KEY = os.environ.get("AGENT_1_KEY")
MY_HARD_WALLET = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# 1. Create the wallet math to match your phone
key_bytes = bytes.fromhex(HEX_KEY)
wallet = LocalWallet(PrivateKey(key_bytes))

# 2. Initialize the Agent using your HEX_KEY as the SEED
# This is the "Front Door" way to sync the Almanac Registration
agent = Agent(
    name="alpha_1",
    seed=HEX_KEY, 
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

# 3. FORCE THE WALLET OVERRIDE
# Even with the seed, the library might try a different derivation path.
# This line ensures the wallet ALWAYS matches fetch1c6dj...
agent._wallet = wallet
agent._ledger = get_ledger("mainnet")

@agent.on_event("startup")
async def verify_identity(ctx: Context):
    ctx.logger.info("🛡️ DNA SYNC ACTIVE")
    ctx.logger.info(f"📍 WALLET: {agent.wallet.address()}")
    
    if str(agent.wallet.address()) == MY_HARD_WALLET:
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH!")
        ctx.logger.info("The Almanac should now be locked to your address.")

if __name__ == "__main__":
    agent.run()
