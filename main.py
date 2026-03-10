import os
from uagents import Agent, Context
from uagents.crypto import Identity

# --- 🔒 THE HARD-WALLET 1:1 LOCK ---
HEX_KEY = os.environ.get("AGENT_1_KEY")

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# 1. Create the agent with a placeholder seed
agent = Agent(
    name="alpha_1",
    seed="placeholder_seed", 
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

# 2. THE SURGERY: Force-swap the identity with your HEX_KEY
# This bypasses the constructor limitations.
agent._identity = Identity.from_seed(HEX_KEY, 0)
agent._address = agent._identity.address

@agent.on_event("startup")
async def verify_identity(ctx: Context):
    ctx.logger.info("🛡️ HARD-WALLET SYNC CHECK")
    ctx.logger.info(f"📍 AGENT ADDRESS: {agent.address}")
    
    # YOUR HARD WALLET ADDRESS
    expected = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"
    
    if agent.address == expected:
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH! Agent is using your Hard Wallet.")
    else:
        ctx.logger.info("❌ MISMATCH STILL DETECTED.")
        ctx.logger.info(f"Agent is at: {agent.address}")
        ctx.logger.info("This confirms the HEX_KEY and Address in your hand are not a pair.")

if __name__ == "__main__":
    agent.run()
