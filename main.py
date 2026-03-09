import asyncio
import os
from uagents import Agent, Context
from uagents.crypto import Identity

# --- 🔒 THE ABSOLUTE 1:1 LOCK ---
HEX_KEY = os.environ.get("AGENT_1_KEY")

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# We use from_sk (Secret Key). 
# This converts your HEX string directly into the Agent's soul.
# It is a 1:1 mapping. No 'derivation paths' or 'indexes' allowed.
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
    
    # The address from your ASI Alliance Wallet
    expected = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"
    
    if agent.address == expected:
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH! The 50,000 variants are dead.")
    else:
        ctx.logger.info("❌ MISMATCH.")
        ctx.logger.info(f"Agent generated: {agent.address}")
        ctx.logger.info("This means the Hex Key in Secrets is not the one for that wallet.")

if __name__ == "__main__":
    agent.run()
