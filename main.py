import os
from uagents import Agent, Context
from uagents.crypto import Identity
from cosmpy.crypto.keypairs import PrivateKey

# --- 🔒 THE COMMAND CENTER LOCK ---
HEX_KEY = os.environ.get("AGENT_1_KEY")

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# 1. Convert HEX to RAW BYTES (The real secret)
key_bytes = bytes.fromhex(HEX_KEY)

# 2. Create a PrivateKey object (The 'Hard Wallet' logic)
# This is the exact same math Keplr/ASI Wallet uses.
priv_key = PrivateKey(key_bytes)

# 3. Force-feed this identity to the Agent
# This is the 'Manual Override'
agent_identity = Identity(priv_key)

agent = Agent(
    name="alpha_1",
    identity=agent_identity,
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

@agent.on_event("startup")
async def verify_identity(ctx: Context):
    ctx.logger.info("🛡️ HARD-WALLET 1:1 SYNC")
    ctx.logger.info(f"📍 AGENT ADDRESS: {agent.address}")
    
    # YOUR HARD WALLET ADDRESS
    expected = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"
    
    if agent.address == expected:
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH! No more ghost wallets.")
    else:
        ctx.logger.info("❌ MISMATCH.")
        ctx.logger.info(f"Agent is at: {agent.address}")
        ctx.logger.info("If they don't match, we will use the 'Address Override' trick.")

if __name__ == "__main__":
    agent.run()
