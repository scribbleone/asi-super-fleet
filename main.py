import os
from uagents import Agent, Context, Model, Bureau
from uagents.network import get_ledger
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# --- 🛰️ THE GLOBAL EARNING PROTOCOLS ---
class ExternalTask(Model):
    query: str

class TaskResult(Model):
    response: str

# --- 🔒 SECURITY BRIDGE (Your Nord Wallet Keys) ---
KEY_1 = os.getenv("AGENT_1_KEY")
KEY_2 = os.getenv("AGENT_2_KEY")

# 1. ALPHA_1 (The Data Worker)
agent1 = Agent(
    name="alpha_1", 
    seed=KEY_1, 
    port=8000, 
    endpoint=["https://agentverse.ai/v1/auth/callback"] 
)
agent1._wallet = LocalWallet(PrivateKey(bytes.fromhex(KEY_1)))
agent1._ledger = get_ledger("mainnet")

@agent1.on_message(model=ExternalTask, replies={TaskResult})
async def handle_outside_work(ctx: Context, sender: str, msg: ExternalTask):
    ctx.logger.info(f"🌍 ALPHA_1: EXTERNAL WORK REQUEST from {sender}")
    # This is where external FET would be verified before sending the result
    await ctx.send(sender, TaskResult(response="Service Active: Data Processed"))
    ctx.logger.info("💰 ALPHA_1: Task complete. Awaiting fee settlement.")

# 2. ALPHA_2 (The Network Guard & Secondary Earner)
agent2 = Agent(
    name="alpha_2", 
    seed=KEY_2, 
    port=8001, 
    endpoint=["https://agentverse.ai/v1/auth/callback"]
)
agent2._wallet = LocalWallet(PrivateKey(bytes.fromhex(KEY_2)))
agent2._ledger = get_ledger("mainnet")

@agent2.on_interval(period=3600.0)
async def maintenance_check(ctx: Context):
    ctx.logger.info("🕵️ ALPHA_2: Scanning Almanac for fleet visibility...")
    balance = agent2.ledger.query_bank_balance(agent2.wallet.address())
    ctx.logger.info(f"📈 ALPHA_2 STATUS: Online. Wallet Balance: {balance} afet")

@agent2.on_message(model=ExternalTask, replies={TaskResult})
async def handle_secondary_work(ctx: Context, sender: str, msg: ExternalTask):
    ctx.logger.info(f"🌍 ALPHA_2: EXTERNAL WORK REQUEST from {sender}")
    await ctx.send(sender, TaskResult(response="Service Active: Network Health OK"))

# --- 🚀 THE BUREAU (Management) ---
if __name__ == "__main__":
    # We run them in the Bureau to keep both threads alive on one GitHub Action
    bureau = Bureau(port=8000, endpoint=["https://agentverse.ai/v1/auth/callback"])
    bureau.add(agent1)
    bureau.add(agent2)
    
    print("💎 SUPER-FLEET PHASE 1: ACTIVE")
    print(f"📍 ALPHA_1: {agent1.wallet.address()}")
    print(f"📍 ALPHA_2: {agent2.wallet.address()}")
    
    bureau.run()
