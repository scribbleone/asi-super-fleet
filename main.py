import asyncio
import os
from uagents import Agent, Context
from uagents.crypto import Identity

# --- 🔒 THE 1:1 HARD-LOCK ---
HEX_KEY = os.environ.get("AGENT_1_KEY")

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# We use 'from_sk' (Secret Key). 
# This is a DIRECT link. No derivation, no math, no '50,000 ways'.
# It converts your HEX string directly into the Agent's soul.
agent_identity = Identity.from_sk(HEX_KEY)

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
    
    # This is the 'fetch1c6dj...' address from your phone
    expected = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"
    
    if agent.address == expected:
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH FOUND.")
        ctx.logger.info("The agent and your ASI Wallet are now the same person.")
    else:
        ctx.logger.info("❌ STILL A MISMATCH.")
        ctx.logger.info(f"Agent generated: {agent.address}")
        ctx.logger.info("This means the Hex Key in Secrets isn't the one for that wallet.")

if __name__ == "__main__":
    agent.run()
