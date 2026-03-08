import os, asyncio, http.server, socketserver, threading, requests
from uagents import Agent, Context, Model

print("--- ALPHA SUPER-AGENT: LIVE DATA HUB ---")

# REPLIT HEALTH CHECK (Fixes the "Provisioning" loop)
def run_health_check():
    with socketserver.TCPServer(("0.0.0.0", 5000), http.server.SimpleHTTPRequestHandler) as httpd:
        httpd.serve_forever()
threading.Thread(target=run_health_check, daemon=True).start()

API_KEY = os.environ.get("CG_API_KEY")
BETA_LEAD_ADDRESS = "fetch1p079k6sq95v40l08msfms8p62v9g9tjsu5l9re"
class MarketData(Model): price: float; trend: str

# Focusing on ONE Super-Manager for stability
Manager = Agent(name="Alpha_Manager", seed="super_alpha_v4_final", port=8000, endpoint=["http://127.0.0.1:8000/submit"])

@Manager.on_interval(period=300.0)
async def fetch_real_price(ctx: Context):
    # Fetching real FET (ASI) price
    url = f"https://api.coingecko.com/api/v3/simple/price?ids=fetch-ai&vs_currencies=usd&x_cg_demo_api_key={API_KEY}"
    try:
        r = requests.get(url).json()
        price = r['fetch-ai']['usd']
        print(f"💰 REAL-TIME PRICE: {price} USD")
        await ctx.send(BETA_LEAD_ADDRESS, MarketData(price=price, trend="live"))
    except Exception as e:
        print(f"⚠️ API Busy or Key Missing: {e}")

if __name__ == "__main__":
    Manager.run()
  
