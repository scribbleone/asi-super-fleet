import os
from uagents import Agent, Context
from uagents.crypto import Identity

# --- 🔒 THE COMMAND CENTER LOCK ---
HEX_KEY = os.environ.get("AGENT_1_KEY")

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# This is the "Kill Shot" for ghost wallets.
# Instead of a 'seed', we create the identity directly from your key.
# This forces the agent to BE the wallet you hold in your hand.
agent_identity = Identity.from_string(HEX_KEY)

agent = Agent(
    name="alpha_1",
    identity=agent_identity, # This overrides the library's math
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

@agent.on_event("startup")
async def verify_identity(ctx: Context):
    ctx.logger.info("🛡️ HARD-WALLET SYNC CHECK")
    ctx.logger.info(f"📍 AGENT ADDRESS: {agent.address}")
    
    # YOUR HARD WALLET ADDRESS
    expected = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"
    
    if agent.address == expected:
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH FOUND.")
        ctx.logger.info("The agent is now using your HARD WALLET.")
    else:
        ctx.logger.info("❌ STILL A MISMATCH.")
        ctx.logger.info(f"Agent is trying to be: {agent.address}")
        ctx.logger.info("If this fails, we will use the 'Ledger-Style' raw byte override.")

if __name__ == "__main__":
    agent.run()
