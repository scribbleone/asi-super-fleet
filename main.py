import os
from uagents import Agent, Context
# We import the specific Identity logic that handles raw Hex keys
from uagents_core.crypto.identity import Identity

# --- 🔒 THE HARD-WALLET 1:1 LOCK ---
HEX_KEY = os.environ.get("AGENT_1_KEY")

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# This is the 'Direct Link' method. 
# It takes your 64-character hex and treats it as the private key.
# No seeds, no derivation, no variations.
agent_identity = Identity.from_sk(HEX_KEY)

agent = Agent(
    name="alpha_1",
    identity=agent_identity,
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
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH! The variations are dead.")
    else:
        ctx.logger.info("❌ STILL A MISMATCH.")
        ctx.logger.info(f"Agent generated: {agent.address}")
        ctx.logger.info("This indicates the Hex Key in Secrets does not belong to that fetch address.")

if __name__ == "__main__":
    agent.run()
