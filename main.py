import os
from uagents import Agent, Context
from uagents.network import get_ledger
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# --- 🔒 THE COMMAND CENTER ---
HEX_KEY = os.environ.get("AGENT_1_KEY")
MY_HARD_WALLET = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# 1. THE NORD-PHONE MATH (Confirmed Match ✅)
key_bytes = bytes.fromhex(HEX_KEY)
wallet = LocalWallet(PrivateKey(key_bytes))

# 2. Set up the REAL Mainnet Ledger
ledger = get_ledger("mainnet")

# 3. Start the Agent
agent = Agent(
    name="alpha_1",
    seed=HEX_KEY, 
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

# 4. THE TOTAL OVERRIDE
# We force the wallet AND the ledger to use your hard-wallet settings
agent._wallet = wallet
agent._ledger = ledger

@agent.on_event("startup")
async def verify_identity(ctx: Context):
    ctx.logger.info("🛡️ TOTAL FLEET SYNC ACTIVE")
    ctx.logger.info(f"📍 WALLET: {agent.wallet.address()}")
    
    if str(agent.wallet.address()) == MY_HARD_WALLET:
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH PERMANENTLY LOCKED.")
        ctx.logger.info(f"Network: {agent.ledger.network_config.chain_id}")
        ctx.logger.info("Ready for 0.05 FET funding.")

if __name__ == "__main__":
    agent.run()
