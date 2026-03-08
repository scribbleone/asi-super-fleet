import os, asyncio, requests
from uagents import Agent, Context, Model
from cosmpy.aerial.client import LedgerClient, NetworkConfig

print("--- ALPHA SUPER-AGENT: MAINNET ACTIVE ---")

# 1. Connect to Fetch.ai Mainnet to see your 9.6 FET
ledger_client = LedgerClient(NetworkConfig.fetchai_mainnet())

# 2. Pull Secrets from GitHub
API_KEY = os.environ.get("CG_API_KEY")
AGENT_SEED = os.environ.get("AGENT_SEED") 
BETA_LEAD_ADDRESS = "fetch1p079k6sq95v40l08msfms8p62v9g9tjsu5l9re"

class MarketData(Model): price: float; trend: str

# 3. Initialize Agent with YOUR real seed
Manager = Agent(
    name="Alpha_Manager", 
    seed=AGENT_SEED, 
    port=8000, 
    endpoint=["http://127.0.0.1:8000/submit"]
)

@Manager.on_interval(period=300.0)
async def fetch_and_audit(ctx: Context):
    # Check your real balance first
    try:
        query_bal = ledger_client.query_bank_balance(ctx.address)
        actual_fet = query_bal / 1e18 # Convert from 'atto' to FET
        print(f"🏦 WALLET: {ctx.address}")
        print(f"💰 BALANCE: {actual_fet} FET")
    except Exception as e:
        print(f"⚠️ Ledger Busy: {e}")

    # Fetching real FET (ASI) price using your specific Key
    url = f"https://api.coingecko.com/api/v3/simple/price?ids=fetch-ai&vs_currencies=usd&x_cg_demo_api_key={API_KEY}"
    try:
        r = requests.get(url).json()
        price = r['fetch-ai']['usd']
        print(f"💹 MARKET PRICE: ${price} USD")
        await ctx.send(BETA_LEAD_ADDRESS, MarketData(price=price, trend="live"))
    except Exception as e:
        print(f"⚠️ API Error: {e}")

if __name__ == "__main__":
    Manager.run()
  
