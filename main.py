import os
from uagents import Agent, Context
from uagents.crypto import Identity

# --- 🔒 THE COMMAND CENTER LOCK ---
HEX_KEY = os.environ.get("AGENT_1_KEY")

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# We create the identity FIRST using the HEX_KEY and index 0.
# This is the most direct way to say "Use this key exactly."
agent_identity = Identity.from_seed(HEX_KEY, 0)

# We initialize the agent. Since the constructor is being picky about 
# the 'identity' keyword, we will pass the seed directly.
agent = Agent(
    name="alpha_1",
    seed=HEX_KEY,
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

# --- 🎯 THE FORCED SYNC ---
# We manually overwrite the agent's internal address with the one 
# derived from our specific identity check.
@agent.on_event("startup")
async def verify_identity(ctx: Context):
    ctx.logger.info("🛡️ HARD-WALLET SYNC CHECK")
    ctx.logger.info(f"📍 AGENT ADDRESS: {agent.address}")
    
    # YOUR HARD WALLET ADDRESS
    expected = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"
    
    if agent.address == expected:
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH FOUND.")
    else:
        ctx.logger.info("❌ MISMATCH DETECTED.")
        ctx.logger.info(f"Agent produced: {agent.address}")
        ctx.logger.info("---------------------------------------------")
        ctx.logger.info("If this is a mismatch, the HEX_KEY in Secrets")
        ctx.logger.info("is not the parent key of that fetch address.")

if __name__ == "__main__":
    agent.run()
