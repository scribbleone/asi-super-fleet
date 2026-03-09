import asyncio
import os
from uagents import Agent, Context
from uagents.crypto import Identity

# --- 🔒 THE ABSOLUTE 1:1 LOCK ---
HEX_KEY = os.environ.get("AGENT_1_KEY")

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# We use from_key and pass it the HEX. 
# In uagents 0.24.0, this is the 'back door' to 1:1 matching.
agent_identity = Identity.from_key(HEX_KEY)

agent = Agent(
    name="alpha_1",
    identity=agent_identity,
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

@agent.on_event("startup")
async def verify_identity(ctx: Context):
    ctx.logger.info("🛡️ 1:1 IDENTITY LOCK CHECK")
    ctx.logger.info(f"📍 AGENT ADDRESS: {agent.address}")
    
    # The address from your ASI Alliance Wallet
    expected = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"
    
    if agent.address == expected:
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH! The variations are dead.")
        ctx.logger.info("The agent and your phone are now looking at the same wallet.")
    else:
        ctx.logger.info("❌ MISMATCH.")
        ctx.logger.info(f"The code produced: {agent.address}")
        ctx.logger.info("This usually means the Secret Key in GitHub is missing a character or is the wrong one.")

if __name__ == "__main__":
    agent.run()
