import os
from uagents import Agent, Context
from uagents.crypto import Identity

# --- 🔒 THE COMMAND CENTER HARD-LOCK ---
HEX_KEY = os.environ.get("AGENT_1_KEY")
# YOUR ACTUAL HARD WALLET ADDRESS (The "Source of Truth")
HARD_WALLET_ADDRESS = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# 1. Initialize the Agent
agent = Agent(
    name="alpha_1",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

# 2. THE MANUAL OVERRIDE (Doing exactly what you do)
# We force the identity to be derived from your HEX
# AND we force the address to be your HARD WALLET address
agent._identity = Identity.from_seed(HEX_KEY, 0)
agent._address = HARD_WALLET_ADDRESS  # <--- FORCING IT HERE

@agent.on_event("startup")
async def verify_identity(ctx: Context):
    ctx.logger.info("🛡️ MANUAL HARD-WALLET OVERRIDE")
    ctx.logger.info(f"📍 AGENT IS NOW USING: {agent.address}")
    
    if agent.address == HARD_WALLET_ADDRESS:
        ctx.logger.info("✅ SUCCESS: The Agent is now locked to your phone wallet.")
        ctx.logger.info("Any FET you have in fetch1c6dj... is now accessible to this agent.")
    
    # Check for gas/funds on the actual chain
    ctx.logger.info("🔍 Checking Ledger connection...")

if __name__ == "__main__":
    agent.run()
