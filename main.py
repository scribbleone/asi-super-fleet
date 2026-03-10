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

# 1. THE NORD-PHONE MATH (Confirmed ✅)
key_bytes = bytes.fromhex(HEX_KEY)
wallet = LocalWallet(PrivateKey(key_bytes))

# 2. START THE AGENT
agent = Agent(
    name="alpha_1",
    seed=HEX_KEY,
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

# 3. THE HIJACK
# We manually swap out the internal ledger and wallet 
# This forces the Registration logic to use your address.
agent._ledger = get_ledger("mainnet")
agent._wallet = wallet

@agent.on_event("startup")
async def verify_identity(ctx: Context):
    ctx.logger.info("🛡️ TOTAL HIJACK ACTIVE")
    ctx.logger.info(f"📍 WALLET ADDRESS: {agent.wallet.address()}")
    
    # Check balance directly on-chain
    balance = agent.ledger.query_bank_balance(agent.wallet.address())
    ctx.logger.info(f"💰 ON-CHAIN BALANCE: {balance} afet")

    if str(agent.wallet.address()) == MY_HARD_WALLET:
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH!")
        ctx.logger.info("--- ACTION PLAN ---")
        ctx.logger.info(f"If the WARNING below still says fetch1ey45,")
        ctx.logger.info("do NOT fund yet. We will disable Almanac auto-reg.")

if __name__ == "__main__":
    agent.run()
