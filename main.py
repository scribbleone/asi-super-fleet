import asyncio
import os
from uagents import Agent, Context
from uagents.crypto import Identity

# --- 🔒 THE HARD-LOCK PROTOCOL ---
# We pull the HEX KEY from GitHub Secrets so it stays private.
HEX_KEY = os.environ.get("AGENT_1_KEY")

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# This creates the 'Soul' of the agent directly from your Hex Key.
# It bypasses all seed-phrase math.
agent_identity = Identity.from_key(bytes.fromhex(HEX_KEY))

# Initialize the agent with your fixed identity
agent = Agent(
    name="alpha_1",
    identity=agent_identity,
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

@agent.on_event("startup")
async def verify_identity(ctx: Context):
    ctx.logger.info("🛡️ HARD-LOCK TEST INITIATED")
    ctx.logger.info(f"📍 ACTIVE WALLET: {agent.address}")
    
    expected = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"
    if agent.address == expected:
        ctx.logger.info("✅ SUCCESS: The Agent is locked to your ASI Wallet!")
    else:
        ctx.logger.info(f"❌ MISMATCH: Agent is at {agent.address}")

if __name__ == "__main__":
    agent.run()
    
