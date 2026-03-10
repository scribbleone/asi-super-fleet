import os
from uagents import Agent, Context
from uagents.network import get_ledger
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# --- 🔒 THE COMMAND CENTER ---
HEX_KEY = os.environ.get("AGENT_1_KEY")
MY_HARD_WALLET = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"

key_bytes = bytes.fromhex(HEX_KEY)
wallet = LocalWallet(PrivateKey(key_bytes))
ledger = get_ledger("mainnet")

agent = Agent(
    name="alpha_1",
    seed=HEX_KEY,
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

# HIJACK
agent._ledger = ledger
agent._wallet = wallet

@agent.on_event("startup")
async def start_up(ctx: Context):
    ctx.logger.info(f"🚀 ALPHA_1 ONLINE. Wallet: {agent.wallet.address()}")
    ctx.logger.info(f"💰 STARTING BALANCE: {agent.ledger.query_bank_balance(agent.wallet.address())} afet")

# --- 🛰️ HEARTBEAT TASK ---
@agent.on_interval(period=30.0)
async def heartbeat(ctx: Context):
    ctx.logger.info("💓 HEARTBEAT: Checking network connection...")
    try:
        # We try to query the ledger to ensure the connection is live
        balance = agent.ledger.query_bank_balance(agent.wallet.address())
        ctx.logger.info(f"✅ CONNECTION LIVE. Current Balance: {balance} afet")
    except Exception as e:
        ctx.logger.info(f"❌ CONNECTION DROPPED: {e}")

if __name__ == "__main__":
    agent.run()
