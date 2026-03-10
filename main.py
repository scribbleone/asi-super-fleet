import os
from uagents import Agent, Context
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# --- 🔒 THE COMMAND CENTER ---
HEX_KEY = os.environ.get("AGENT_1_KEY")
MY_HARD_WALLET = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# 1. RAW CRYPTO: Create the exact wallet that matches your Nord phone
# We turn the HEX string into actual bytes, then a PrivateKey object
key_bytes = bytes.fromhex(HEX_KEY)
wallet = LocalWallet(PrivateKey(key_bytes))

# 2. Start the Agent with a dummy seed (we are going to overwrite its brain anyway)
agent = Agent(
    name="alpha_1",
    seed="override_placeholder",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

# 3. THE INJECTION: We manually replace the agent's wallet and address
# This forces the agent to use your 'fetch1c6dj...' for EVERYTHING
agent._wallet = wallet
agent._address = str(wallet.address())

@agent.on_event("startup")
async def verify_identity(ctx: Context):
    ctx.logger.info("🛡️ RAW ENGINE INJECTION ACTIVE")
    ctx.logger.info(f"📍 CURRENT WALLET: {agent.address}")
    
    if agent.address == MY_HARD_WALLET:
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH! The magician's trick has failed.")
        ctx.logger.info("The agent is now permanently locked to your wallet.")
    else:
        ctx.logger.info("❌ STILL MISMATCHED.")
        ctx.logger.info(f"The address is still showing as: {agent.address}")

if __name__ == "__main__":
    agent.run()
