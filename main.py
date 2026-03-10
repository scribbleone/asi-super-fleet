import os
from uagents import Agent, Context
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# --- 🔒 THE COMMAND CENTER ---
HEX_KEY = os.environ.get("AGENT_1_KEY")
MY_HARD_WALLET = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# 1. THE NORD-PHONE MATH: Convert Hex to the exact PrivateKey object
# This ensures we are using the raw 'Identity' without the library's flavor.
key_bytes = bytes.fromhex(HEX_KEY)
priv_key = PrivateKey(key_bytes)
my_wallet = LocalWallet(priv_key)

# 2. Start the Agent
agent = Agent(
    name="alpha_1",
    seed=HEX_KEY, 
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

# 3. THE HARD-WIRE: Replace the agent's internal wallet with our Nord-math wallet
# We use agent.wallet (the property) to force it to look at our LocalWallet
agent._wallet = my_wallet

@agent.on_event("startup")
async def verify_identity(ctx: Context):
    ctx.logger.info("🛡️ NORD-WALLET SYNC ACTIVE")
    # We ask the WALLET directly for its address, not the Agent.
    actual_addr = str(agent.wallet.address())
    ctx.logger.info(f"📍 WALLET IN USE: {actual_addr}")
    
    if actual_addr == MY_HARD_WALLET:
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH! The magician is out of tricks.")
        ctx.logger.info(f"You can now safely fund {actual_addr}")
    else:
        ctx.logger.info("❌ STILL DRIFTING.")
        ctx.logger.info(f"Math produced: {actual_addr}")

if __name__ == "__main__":
    agent.run()
