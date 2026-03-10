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

@agent1.on_message(model=StatusRequest)
async def handle_request(ctx: Context, sender: str, msg: StatusRequest):
    ctx.logger.info(f"💰 ALPHA_1: Payment received from {sender}!")
    balance = agent1.ledger.query_bank_balance(agent1.wallet.address())
    ctx.logger.info(f"📈 ALPHA_1: New Balance: {balance} afet")

# 2. SETUP AGENT 2 (The Payer)
agent2 = Agent(name="alpha_2", seed=KEY_2, port=8001, endpoint=["http://127.0.0.1:8001/submit"])
agent2._wallet = LocalWallet(PrivateKey(bytes.fromhex(KEY_2)))
agent2._ledger = get_ledger("mainnet")

@agent2.on_interval(period=60.0)
async def send_payment(ctx: Context):
    ctx.logger.info("💳 ALPHA_2: Sending 0.001 FET 'Service Fee' to Alpha 1...")
    # 'coins' is the correct keyword for sending afet
    await ctx.send(agent1.address, StatusRequest(message="Ping"), coins=1000000000000000)

if __name__ == "__main__":
    # We add the agents to the Bureau but keep their individual endpoints active
    bureau = Bureau(port=8000, endpoint=["http://127.0.0.1:8000/submit"])
    bureau.add(agent1)
    bureau.add(agent2)
    bureau.run()
