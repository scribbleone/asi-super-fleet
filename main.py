import asyncio
import os
from uagents import Agent, Context
from uagents.crypto import Identity
from uagents_core.crypto.identity import EncodableIdentity

# --- 🔒 THE ABSOLUTE 1:1 LOCK ---
HEX_KEY = os.environ.get("AGENT_1_KEY")

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# We use the core 'from_seed' but with the index 0 and your HEX.
# In this specific library version, this is the most direct 1:1 path.
agent_identity = Identity.from_seed(HEX_KEY, 0)

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
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH! The 50,000 variants are dead.")
    else:
        ctx.logger.info("❌ MISMATCH.")
        ctx.logger.info(f"The code produced: {agent.address}")
        ctx.logger.info("This means the library is still deriving a new path.")
        ctx.logger.info("I have a backup 'Raw Byte' method if this fails.")

if __name__ == "__main__":
    agent.run()
