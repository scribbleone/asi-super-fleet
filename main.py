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

# 1. Force the Identity to be derived 1:1 from your HEX
# We use from_string to ensure no extra derivation math is added
forced_identity = Identity.from_string(HEX_KEY)

# 2. Setup the Nord-Phone Wallet math
key_bytes = bytes.fromhex(HEX_KEY)
wallet = LocalWallet(PrivateKey(key_bytes))

# 3. Initialize Agent with the FORCED identity
# By passing 'identity', the Almanac registration is forced to use your key
agent = Agent(
    name="alpha_1",
    identity=forced_identity,
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

# 4. Final Ledger & Wallet Bridge
agent._wallet = wallet
agent._ledger = get_ledger("mainnet")

@agent.on_event("startup")
async def verify_identity(ctx: Context):
    ctx.logger.info("🛡️ TOTAL GLOBAL LOCKDOWN")
    ctx.logger.info(f"📍 WALLET: {agent.wallet.address()}")
    ctx.logger.info(f"📍 REGISTRATION ADDR: {agent.address}")
    
    if str(agent.wallet.address()) == MY_HARD_WALLET:
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH PERMANENTLY LOCKED.")
    else:
        ctx.logger.info("❌ WARNING: ADDRESS DRIFT DETECTED.")

if __name__ == "__main__":
    agent.run()
