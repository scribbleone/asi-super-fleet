import os
from uagents import Agent, Context
from uagents.network import get_ledger
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# --- 🔒 THE COMMAND CENTER HARD-LOCK ---
HEX_KEY = os.environ.get("AGENT_1_KEY")
MY_HARD_WALLET = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# 1. Convert HEX to RAW BYTES (The real secret)
key_bytes = bytes.fromhex(HEX_KEY)
# 2. Create the real PrivateKey and Wallet object
# This is the "Truth" that matches your phone.
priv_key = PrivateKey(key_bytes)
wallet = LocalWallet(priv_key)

# 3. Initialize the Agent with a placeholder (it doesn't matter, we override it)
agent = Agent(name="alpha_1", port=8000, endpoint=["http://127.0.0.1:8000/submit"])

# 🎯 THE SURGERY: We force the agent to use our cosmpy wallet
agent._wallet = wallet

@agent.on_event("startup")
async def verify_identity(ctx: Context):
    ctx.logger.info("🛡️ FINAL SYNC ATTEMPT")
    # Get the address from the wallet we injected
    current_addr = str(agent.wallet.address())
    ctx.logger.info(f"📍 WALLET IN USE: {current_addr}")
    
    if current_addr == MY_HARD_WALLET:
        ctx.logger.info("✅ SUCCESS: 1:1 MATCH! The library has been bypassed.")
    else:
        ctx.logger.info("❌ STILL A MISMATCH.")
        ctx.logger.info(f"Wallet address is: {current_addr}")
        ctx.logger.info("This means the Hex string itself is for a different address.")

if __name__ == "__main__":
    agent.run()
