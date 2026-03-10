import os
from uagents import Agent, Context
from uagents.network import get_ledger
from uagents.crypto import Identity
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# --- 🔒 THE COMMAND CENTER ---
HEX_KEY = os.environ.get("AGENT_1_KEY")
MY_HARD_WALLET = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# 1. Create the REAL Identity from your HEX string
# This matches the math of your Nord phone wallet
real_identity = Identity.from_string(HEX_KEY)

# 2. Start the Agent with no seed (it will make a random one, which we then delete)
agent = Agent(
    name="alpha_1",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

# 3. THE BRAIN SURGERY: Force-overwrite the Agent's identity
# This kills the 'fetch1ey45...' ghost wallet once and for all.
agent._identity = real_identity
agent._address = real_identity.address
agent._wallet = LocalWallet(PrivateKey(bytes.fromhex(HEX_KEY)))
agent._ledger = get_ledger("mainnet")

@agent.on_event("startup")
async def verify_identity(ctx: Context):
    ctx.logger.info("🛡️ COMMAND CENTER LOCKDOWN")
    ctx.logger.info(f"📍 WALLET ADDRESS: {agent.wallet.address()}")
    
    if str(agent.wallet.address()) == MY_HARD_WALLET:
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH! No more ghost wallets.")
    else:
        ctx.logger.info("❌ ERROR: Identity swap failed.")

if __name__ == "__main__":
    agent.run()
