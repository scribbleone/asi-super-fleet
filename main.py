import os
from uagents import Agent, Context
from uagents.network import get_ledger
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# --- 🔒 THE COMMAND CENTER ---
HEX_KEY = os.environ.get("AGENT_1_KEY")
MY_HARD_WALLET = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"

# Mainnet Config (March 9th requirements)
MAINNET_CONFIG = {
    "chain_id": "fetchhub-4",
    "url": "grpc+https://grpc-fetchhub.fetch.ai:443",
    "fee_minimum_gas_price": 5000000000,
    "fee_denomination": "afet",
    "staking_denomination": "afet",
}

# 1. Create the REAL wallet from your HEX
key_bytes = bytes.fromhex(HEX_KEY)
priv_key = PrivateKey(key_bytes)
my_wallet = LocalWallet(priv_key)

# 2. Initialize Agent using the HEX as the seed for Identity
agent = Agent(
    name="alpha_1",
    seed=HEX_KEY, 
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

# 3. THE FINAL SYNC: Force override Identity and Wallet
# This ensures the 'Registration' address matches your FET address
agent._wallet = my_wallet
agent._ledger = get_ledger("mainnet") # Apply the Mainnet ledger

@agent.on_event("startup")
async def verify_identity(ctx: Context):
    ctx.logger.info("🛡️ TOTAL SYNC ACTIVE")
    ctx.logger.info(f"📍 WALLET: {agent.wallet.address()}")
    
    if str(agent.wallet.address()) == MY_HARD_WALLET:
        ctx.logger.info("✅ 1:1 MATCH: Wallet and Identity are fused.")
        ctx.logger.info("The Almanac registration will now use your Hard Wallet funds.")

if __name__ == "__main__":
    agent.run()
