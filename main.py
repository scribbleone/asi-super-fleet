import os
from uagents.crypto import Identity

def extract_current_identity():
    print("🔍 Searching for active Agent 1 identity...")
    
    # This looks for the default 'agent.utils' or '.env' where uagents saves keys
    # If you are running this in a folder with an existing agent, it should find it.
    try:
        # Check if an identity is already loaded in the environment
        agent_address = os.environ.get("AGENT_ADDRESS")
        print(f"Current Environment Address: {agent_address}")
        
        # We are going to attempt to find any local .env files
        if os.path.exists(".env"):
            with open(".env", "r") as f:
                print("📄 Found .env file. Content (Redacted for security):")
                for line in f:
                    if "SEED" in line or "PRIVATE_KEY" in line:
                        print(f"Found a key entry: {line.split('=')[0]}...")

    except Exception as e:
        print(f"❌ Error during extraction: {e}")

if __name__ == "__main__":
    extract_current_identity()
