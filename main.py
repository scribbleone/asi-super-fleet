import os
from uagents import Agent, Context
from uagents.crypto import Identity

# --- 🔒 THE COMMAND CENTER ---
HEX_KEY = os.environ.get("AGENT_1_KEY")
MY_HARD_WALLET = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# 1. We create the Identity object FIRST.
# Identity.from_string(HEX_KEY) is the literal interpretation.
# This is the "soul" that matches your phone's address.
agent_identity = Identity.from_string(HEX_KEY)

# 2. Initialize Agent with the FORCED identity.
# By passing 'identity=agent_identity', we stop the library from 
# inventing its own 'fetch1ey45...' address for the Almanac.
agent = Agent(
    name="alpha_1",
    identity=agent_identity,
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

@agent.on_event("startup")
async def verify_identity(ctx: Context):
    ctx.logger.info("🛡️ TOTAL LOCKDOWN ACTIVE")
    ctx.logger.info(f"📍 WALLET IN USE: {agent.address}")
    
    if agent.address == MY_HARD_WALLET:
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH FOUND.")
        ctx.logger.info("--- ACTION REQUIRED ---")
        ctx.logger.info(f"You can now safely send FET to {agent.address}")
    else:
        ctx.logger.info("❌ MISMATCH DETECTED.")
        ctx.logger.info(f"Agent is still trying to be: {agent.address}")

if __name__ == "__main__":
    agent.run()
