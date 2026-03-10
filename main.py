import os
from uagents import Agent, Context
from uagents.network import get_ledger, wait_for_tx_to_complete
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

# --- 🔒 THE COMMAND CENTER ---
HEX_KEY = os.environ.get("AGENT_1_KEY")
MY_HARD_WALLET = "fetch1c6djwc0jytzkpzdxwamlq62huwnhqh59ynyyl0"

if not HEX_KEY:
    print("❌ ERROR: AGENT_1_KEY not found in GitHub Secrets!")
    exit()

# 1. THE NORD-PHONE WALLET (The Source of Truth)
key_bytes = bytes.fromhex(HEX_KEY)
wallet = LocalWallet(PrivateKey(key_bytes))
ledger = get_ledger("mainnet")

# 2. START THE AGENT (Disable Auto-Registration)
# We set 'registration_policy=None' (if supported) or handle it manually
agent = Agent(
    name="alpha_1",
    seed=HEX_KEY,
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

# 3. THE HIJACK
agent._ledger = ledger
agent._wallet = wallet

@agent.on_event("startup")
async def manual_registration(ctx: Context):
    ctx.logger.info("☢️ NUCLEAR OPTION ACTIVE: MANUAL REGISTRATION")
    ctx.logger.info(f"📍 TARGET WALLET: {agent.wallet.address()}")
    
    # Check if we have the 0.05 FET (approx 50,000,000,000,000,000 afet)
    balance = agent.ledger.query_bank_balance(agent.wallet.address())
    ctx.logger.info(f"💰 CURRENT BALANCE: {balance} afet")

    if balance < 5000000000000000: # Threshold for registration
        ctx.logger.info("⚠️ STATUS: WAITING FOR 0.05 FET FUNDING...")
        ctx.logger.info(f"Please send funds to: {agent.wallet.address()}")
        return

    # If funds exist, we force the registration using YOUR wallet
    try:
        ctx.logger.info("🚀 FUNDING DETECTED! Registering agent manually...")
        # This bypasses the library's background ghost-wallet loop
        success = await agent._register() 
        ctx.logger.info(f"✅ REGISTRATION STATUS: {success}")
    except Exception as e:
        ctx.logger.info(f"❌ REGISTRATION ERROR: {e}")

if __name__ == "__main__":
    agent.run()
