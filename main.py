import os
from uagents import Agent, Context, Model
from uagents.network import get_ledger
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# --- 🛰️ THE PROTOCOL ---
class StatusRequest(Model):
    message: str

# --- 🔒 KEYS & ADDRESSES ---
KEY_1 = os.environ.get("AGENT_1_KEY")
KEY_2 = os.environ.get("AGENT_2_KEY")

# 1. SETUP AGENT 1 (THE SELLER / EARNER)
agent1 = Agent(name="alpha_1", seed=KEY_1, port=8000, endpoint=["http://127.0.0.1:8000/submit"])
agent1._wallet = LocalWallet(PrivateKey(bytes.fromhex(KEY_1)))
agent1._ledger = get_ledger("mainnet")

@agent1.on_message(model=StatusRequest)
async def handle_request(ctx: Context, sender: str, msg: StatusRequest):
    ctx.logger.info(f"💰 AGENT 1: Received request from {sender}. Payment verified.")
    ctx.logger.info(f"✅ AGENT 1: Current Balance: {agent1.ledger.query_bank_balance(agent1.wallet.address())} afet")

# 2. SETUP AGENT 2 (THE BUYER / PAYER)
agent2 = Agent(name="alpha_2", seed=KEY_2, port=8001, endpoint=["http://127.0.0.1:8001/submit"])
agent2._wallet = LocalWallet(PrivateKey(bytes.fromhex(KEY_2)))
agent2._ledger = get_ledger("mainnet")

@agent2.on_interval(period=60.0) # Every minute
async def send_payment(ctx: Context):
    ctx.logger.info("💳 AGENT 2: Preparing payment for Alpha 1...")
    # This sends 0.001 FET (1,000,000,000,000,000 afet)
    await ctx.send(agent1.address, StatusRequest(message="Requesting Status"), funds=1000000000000000)

# --- 🚀 RUN BOTH ---
from uagents import Bureau
if __name__ == "__main__":
    bureau = Bureau()
    bureau.add(agent1)
    bureau.add(agent2)
    bureau.run()
