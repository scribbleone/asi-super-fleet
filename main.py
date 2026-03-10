import os
from uagents import Agent, Context
from uagents.crypto import Identity

# --- 🔒 THE ABSOLUTE 1:1 HARD-LOCK ---
HEX_KEY = os.environ.get("AGENT_1_KEY")

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# This is the "No-Math" override. 
# We tell the Agent: "Forget everything you know about seeds. 
# This string IS your private key."
agent_identity = Identity.from_string(HEX_KEY)

agent = Agent(
    name="alpha_1",
    identity=agent_identity,
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

@agent.on_event("startup")
async def verify_identity(ctx: Context):
    ctx.logger.info("🛡️ COMMAND CENTER SYNC CHECK")
    ctx.logger.info(f"📍 AGENT ADDRESS: {agent.address}")
    
    # YOUR HARD WALLET ADDRESS
    expected = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"
    
    if agent.address == expected:
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH! The ghost wallets are gone.")
    else:
        ctx.logger.info("❌ MISMATCH DETECTED.")
        ctx.logger.info(f"Agent is running as: {agent.address}")
        ctx.logger.info("Check: Is the Hex Key in GitHub definitely for fetch1c6dj...?")

if __name__ == "__main__":
    agent.run()
