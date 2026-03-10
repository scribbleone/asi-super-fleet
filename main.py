import os
from uagents import Agent, Context
from uagents.crypto import Identity

# --- 🔒 THE COMMAND CENTER ---
HEX_KEY = os.environ.get("AGENT_1_KEY")
MY_HARD_WALLET = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# This is the "Secret Sauce." 
# We don't let the Agent generate its own seed. 
# We pass the HEX_KEY directly as the seed.
agent = Agent(
    name="alpha_1",
    seed=HEX_KEY, # This is where the 1:1 link happens
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

@agent.on_event("startup")
async def verify_identity(ctx: Context):
    ctx.logger.info("🛡️ FINAL IDENTITY VERIFICATION")
    # This prints the Fetch address associated with the agent's identity
    ctx.logger.info(f"📍 WALLET ADDRESS: {agent.wallet.address()}")
    
    if str(agent.wallet.address()) == MY_HARD_WALLET:
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH!")
    else:
        ctx.logger.info("❌ MISMATCH DETECTED.")
        ctx.logger.info(f"Library is pointing to: {agent.wallet.address()}")

if __name__ == "__main__":
    agent.run()
