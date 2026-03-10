import os
from uagents import Agent, Context
from uagents.network import get_ledger
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# --- 🔒 THE COMMAND CENTER ---
HEX_KEY = os.environ.get("AGENT_1_KEY")
MY_HARD_WALLET = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"

# 1. NORD-PHONE WALLET & LEDGER SETUP
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

# 3. THE HIJACK: Force the agent to use YOUR wallet for signing
agent._ledger = ledger
agent._wallet = wallet

@agent.on_event("startup")
async def final_push(ctx: Context):
    ctx.logger.info("🛡️ FINAL HANDSHAKE ATTEMPT")
    ctx.logger.info(f"📍 WALLET: {agent.wallet.address()}")
    
    # Verify the 0.1 FET is still there
    balance = agent.ledger.query_bank_balance(agent.wallet.address())
    ctx.logger.info(f"💰 ON-CHAIN BALANCE: {balance} afet")

    if balance > 0:
        ctx.logger.info("🚀 FUNDING DETECTED. Triggering registration...")
        try:
            # We use the internal setup to push the registration to the Almanac
            await agent.setup()
            ctx.logger.info("✅ SUCCESS: Agent is now active on Mainnet.")
        except Exception as e:
            ctx.logger.info(f"📝 NOTE: {e}")
            ctx.logger.info("If the log shows 'Already registered', you have won.")

if __name__ == "__main__":
    agent.run()
