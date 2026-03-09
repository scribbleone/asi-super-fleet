import asyncio
import os
from uagents import Agent, Context
from uagents.crypto import Identity

# --- 🔒 THE HARD-LOCK PROTOCOL ---
HEX_KEY = os.environ.get("AGENT_1_KEY")

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# We use 'from_seed' but pass the HEX string. 
# This ensures it uses the exact bytes of your Private Key.
agent_identity = Identity.from_seed(HEX_KEY, 0)

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
    
    # This is the address you imported to your ASI Wallet
    expected = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"
    
    if agent.address == expected:
        ctx.logger.info("✅ SUCCESS: The Agent is locked to your ASI Wallet!")
    else:
        ctx.logger.info(f"⚠️ MISMATCH: Agent is at {agent.address}")
        ctx.logger.info(f"Verify you used the Hex Key for {expected}")

if __name__ == "__main__":
    agent.run()
