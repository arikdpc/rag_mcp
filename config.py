import os
import requests

SECRETBOX_URL = os.getenv("SECRETBOX_URL")
MASTER_TOKEN = os.getenv("MASTER_TOKEN")

if not SECRETBOX_URL or not MASTER_TOKEN:
    print("[ERROR] SECRETBOX_URL or MASTER_TOKEN environment variable is missing.")
    SECRETBOX_CONNECTED = False
else:
    print("[INFO] Attempting to connect to Secretbox...")
    SECRETBOX_CONNECTED = True

def get_secret(key):
    if not SECRETBOX_CONNECTED:
        print(f"[ERROR] Cannot retrieve '{key}': Secretbox not connected.")
        return None
    headers = {"Authorization": f"Bearer {MASTER_TOKEN}"}
    try:
        response = requests.get(f"{SECRETBOX_URL}/secret/{key}", headers=headers)
        if response.ok:
            value = response.json()["value"]
            print(f"[INFO] Retrieved secret for '{key}'.")
            return value
        else:
            print(f"[ERROR] Failed to retrieve secret '{key}': {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Exception while retrieving secret '{key}': {e}")
        return None

class Settings:
    SUPABASE_URL = get_secret("SUPABASE_URL")
    SUPABASE_KEY = get_secret("SUPABASE_SERVICE_KEY")
    OPENAI_API_KEY = get_secret("OPENAI_API_KEY")
    GPT_MODEL = "gpt-4o-mini"
    EMBEDDING_MODEL = "text-embedding-3-small"

    def __init__(self):
        missing = []
        if not self.SUPABASE_URL:
            missing.append("SUPABASE_URL")
        if not self.SUPABASE_KEY:
            missing.append("SUPABASE_SERVICE_KEY")
        if not self.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")
        if missing:
            print(f"[ERROR] Missing required secrets: {', '.join(missing)}")
            print("[ERROR] Secretbox connection or key retrieval failed. Exiting gracefully.")
            exit(1)
        print("[INFO] All required secrets retrieved successfully.")

settings = Settings()
