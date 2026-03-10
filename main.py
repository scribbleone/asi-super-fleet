import os
from uagents import Agent, Context
from uagents.network import get_ledger
from uagents.registration import LedgerRegistrationPolicy
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# --- 🔒 THE COMMAND CENTER ---
HEX_KEY = os.environ.get("AGENT_1_KEY")
MY_HARD_WALLET = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"

# 1. NORD-PHONE WALLET & LEDGER
key_bytes = bytes.fromhex(HEX_KEY)
wallet = LocalWallet(PrivateKey(key_bytes))
ledger = get_ledger("mainnet")

# 2. INITIALIZE AGENT
agent = Agent(
    name="alpha_1",
    seed=HEX_KEY,
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

# 3. FORCE EVERYTHING TO YOUR WALLET
agent._ledger = ledger
agent._wallet = wallet

@agent.on_event("startup")
async def register_proxy(ctx: Context):
    ctx.logger.info("🛡️ FINAL HANDSHAKE INITIALIZED")
    ctx.logger.info(f"📍 WALLET: {agent.wallet.address()}")
    
    balance = agent.ledger.query_bank_balance(agent.wallet.address())
    ctx.logger.info(f"💰 CONFIRMED BALANCE: {balance} afet")

    if balance > 0:
        ctx.logger.info("🚀 ATTEMPTING SMART-CONTRACT REGISTRATION...")
        try:
            # We call the registration through the established ledger
            await agent.setup() 
            ctx.logger.info("✅ SUCCESS: Agent identity broadcast to Mainnet.")
        except Exception as e:
            ctx.logger.info(f"⚠️ Registration Note: {e}")
            ctx.logger.info("If you see 'already registered', we are good to go!")

if __name__ == "__main__":
    agent.run()
