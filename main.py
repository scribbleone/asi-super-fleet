import os
from uagents import Agent, Context
from uagents.crypto import Identity

# --- 🔒 THE COMMAND CENTER ---
HEX_KEY = os.environ.get("AGENT_1_KEY")
MY_HARD_WALLET = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# 1. Start the agent with a placeholder. 
# We use seed=None or a dummy string because we are about to override it.
agent = Agent(
    name="alpha_1",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

# 2. THE BRAIN SURGERY
# We force the identity to be derived directly from your Hex Key string.
# This is the 1:1 match that bypasses the library's derivation math.
agent._identity = Identity.from_string(HEX_KEY)
agent._address = agent._identity.address

@agent.on_event("startup")
async def verify_identity(ctx: Context):
    ctx.logger.info("🛡️ MANUAL IDENTITY LOCK ACTIVE")
    ctx.logger.info(f"📍 AGENT ADDRESS: {agent.address}")
    
    if agent.address == MY_HARD_WALLET:
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH!")
        ctx.logger.info("--- NETWORK CHECK ---")
        ctx.logger.info(f"The Almanac will now use {agent.address} for registration.")
    else:
        ctx.logger.info("❌ OVERRIDE FAILED.")
        ctx.logger.info(f"Agent is still: {agent.address}")

if __name__ == "__main__":
    agent.run()
