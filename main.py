import asyncio
import os
from uagents import Agent, Context

# --- 🔒 THE DIRECT SEED LOCK ---
HEX_KEY = os.environ.get("AGENT_1_KEY")

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# We pass the HEX_KEY directly as the seed. 
# This is the 'Front Door' the library is forcing us to use.
agent = Agent(
    name="alpha_1",
    seed=HEX_KEY,
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

@agent.on_event("startup")
async def verify_identity(ctx: Context):
    ctx.logger.info("🛡️ IDENTITY LOCK CHECK")
    ctx.logger.info(f"📍 AGENT ADDRESS: {agent.address}")
    
    # The address you have in your ASI Alliance Wallet
    expected = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"
    
    if agent.address == expected:
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH FOUND!")
    else:
        ctx.logger.info("❌ MISMATCH DETECTED.")
        ctx.logger.info(f"The Agent created: {agent.address}")
        ctx.logger.info("--- ACTION ---")
        ctx.logger.info("If they don't match, we will simply import the 'Agent created' address into your phone.")

if __name__ == "__main__":
    agent.run()
