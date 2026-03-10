import os
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low

# --- 🔒 THE COMMAND CENTER HARD-LOCK ---
HEX_KEY = os.environ.get("AGENT_1_KEY")
MY_HARD_WALLET = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# We initialize the agent with the WALLET address directly.
# This tells the library: "This is who you are on the blockchain."
agent = Agent(
    name="alpha_1",
    seed=HEX_KEY, # Used for internal agent identity
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

# --- 🎯 THE FORCE-SYNC ---
# We manually override the ledger's wallet to be YOUR wallet.
# We also apply the Mainnet configuration you specified on March 9th.
agent._wallet = agent._ledger.build_wallet(HEX_KEY)

@agent.on_event("startup")
async def verify_identity(ctx: Context):
    ctx.logger.info("🛡️ COMMAND CENTER SYNC")
    ctx.logger.info(f"📍 WALLET IN USE: {agent.wallet.address()}")
    
    if str(agent.wallet.address()) == MY_HARD_WALLET:
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH! The library is using your Hard Wallet.")
    else:
        ctx.logger.info("❌ MISMATCH DETECTED.")
        ctx.logger.info(f"Library is trying to use: {agent.wallet.address()}")

if __name__ == "__main__":
    agent.run()
