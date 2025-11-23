import os
from dotenv import load_dotenv

# 1. Print where Python is looking
print(f"Current Folder: {os.getcwd()}")

# 2. List all files here
print("Files found:", os.listdir(os.getcwd()))

# 3. Try to load
load_dotenv()
key = os.environ.get("GEMINI_API_KEY")

if key:
    print(f"✅ SUCCESS! Key found: {key[:5]}...")
else:
    print("❌ FAILURE: .env loaded but Key is None.")