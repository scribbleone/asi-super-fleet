import asyncio
import os
from uagents import Agent, Context
from uagents.crypto import Identity

# --- 🔒 THE ABSOLUTE 1:1 LOCK ---
HEX_KEY = os.environ.get("AGENT_1_KEY")

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# We use from_seed because the library refuses everything else.
# By passing the HEX_KEY and the index 0, we are telling the library:
# "Do not derive a path. Use this specific hex as the starting point."
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
    
    # This MUST match what you see in your ASI Alliance Wallet
    expected = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"
    
    if agent.address == expected:
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH FOUND.")
    else:
        ctx.logger.info("❌ MISMATCH DETECTED.")
        ctx.logger.info(f"The Agent created: {agent.address}")
        ctx.logger.info("ACTION REQUIRED: If this address is different, copy it.")
        ctx.logger.info("We will then adjust how the Key is read.")

if __name__ == "__main__":
    agent.run()
