import asyncio
import os
from uagents import Agent, Context
from uagents.crypto import Identity
from cosmpy.crypto.keypairs import PrivateKey

# --- 🔒 THE ABSOLUTE 1:1 LOCK ---
HEX_KEY = os.environ.get("AGENT_1_KEY")

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# We convert the HEX string into a PrivateKey object first.
# Then we tell Identity to use that specific key. 
# This bypasses the 'seed' derivation entirely.
priv_key = PrivateKey(bytes.fromhex(HEX_KEY))
agent_identity = Identity(priv_key)

agent = Agent(
    name="alpha_1",
    identity=agent_identity,
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

@agent.on_event("startup")
async def verify_identity(ctx: Context):
    ctx.logger.info("🛡️ 1:1 IDENTITY LOCK CHECK")
    ctx.logger.info(f"📍 AGENT ADDRESS: {agent.address}")
    
    # The address from your ASI Alliance Wallet
    expected = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"
    
    if agent.address == expected:
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH! The variations are dead.")
    else:
        ctx.logger.info("❌ MISMATCH STILL.")
        ctx.logger.info(f"The code produced: {agent.address}")
        ctx.logger.info("Double-check that the HEX_KEY in Secrets matches the one in your phone.")

if __name__ == "__main__":
    agent.run()
