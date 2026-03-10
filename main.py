import os
from uagents import Agent, Context, Model, Bureau
from uagents.network import get_ledger
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# --- 🛰️ THE PROTOCOL ---
class StatusRequest(Model):
    message: str

# --- 🔒 KEYS & ADDRESSES ---
KEY_1 = os.getenv("AGENT_1_KEY")
KEY_2 = os.getenv("AGENT_2_KEY")

# 1. SETUP AGENT 1 (The Earner)
agent1 = Agent(name="alpha_1", seed=KEY_1, port=8000, endpoint=["http://127.0.0.1:8000/submit"])
agent1._wallet = LocalWallet(PrivateKey(bytes.fromhex(KEY_1)))
agent1._ledger = get_ledger("mainnet")

# 2. SETUP AGENT 2 (The Payer)
agent2 = Agent(name="alpha_2", seed=KEY_2, port=8001, endpoint=["http://127.0.0.1:8001/submit"])
agent2._wallet = LocalWallet(PrivateKey(bytes.fromhex(KEY_2)))
agent2._ledger = get_ledger("mainnet")

@agent2.on_interval(period=60.0)
async def send_payment(ctx: Context):
    ctx.logger.info("💳 ALPHA_2: Initiating direct Ledger transfer to Alpha 1...")
    try:
        # We send 0.001 FET directly using the ledger we know works
        # This creates a real on-chain transaction that your Nord phone will see
        amount = 1000000000000000 # 0.001 FET
        tx = agent2.ledger.send_tokens(agent1.wallet.address(), amount, "afet", agent2.wallet)
        tx.wait_to_complete()
        ctx.logger.info(f"✅ ALPHA_2: Transfer Successful! TX Hash: {tx.tx_hash}")
        
        # Now send the message separately
        await ctx.send(agent1.address, StatusRequest(message="Payment Sent"))
    except Exception as e:
        ctx.logger.info(f"❌ ALPHA_2: Transfer failed: {e}")

@agent1.on_message(model=StatusRequest)
async def handle_request(ctx: Context, sender: str, msg: StatusRequest):
    balance = agent1.ledger.query_bank_balance(agent1.wallet.address())
    ctx.logger.info(f"💰 ALPHA_1: Payment confirmed via Ledger. New Balance: {balance} afet")

if __name__ == "__main__":
    bureau = Bureau(port=8000, endpoint=["http://127.0.0.1:8000/submit"])
    bureau.add(agent1)
    bureau.add(agent2)
    bureau.run()
