import os
import json
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

# 1. Load the API Key
load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("❌ CRITICAL ERROR: API Key is missing from .env file!")
    exit()

# 2. Connect to Gemini
client = genai.Client(api_key=API_KEY)

def clean_json(text):
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:] 
    if text.startswith("```"):
        text = text[3:] 
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def analyze_media_feed(media_path, platform_strategy):
    """
    Sends Video OR Image to Gemini 2.5 and returns a list of items found.
    """
    
    # A. Upload Media (Gemini handles both video and image via Files API)
    print(f"📡 Uploading to Gemini... ({os.path.basename(media_path)})")
    if not os.path.exists(media_path):
        raise FileNotFoundError(f"Media file not found: {media_path}")

    uploaded_file = client.files.upload(file=media_path)
    
    # B. Wait for Processing (Mainly for videos, images are fast)
    while uploaded_file.state.name == "PROCESSING":
        print("... AI is processing media ...")
        time.sleep(1)
        uploaded_file = client.files.get(name=uploaded_file.name)

    if uploaded_file.state.name == "FAILED":
        raise ValueError("Gemini failed to process the media file.")

    # C. The "HawkEye" Prompt
    print("🧠 HawkEye Thinking...")
    
    prompt = f"""
    You are 'HawkEye', an expert reseller AI.
    Strategy: {platform_strategy}.
    
    INSTRUCTIONS:
    1. Analyze the media (Video or Image). Identify EVERY distinct item you see.
    2. **TIMESTAMPS (Video Only)**: If this is a video, provide the timestamp (seconds) where the item is MOST VISIBLE. If this is a still image, use 0.
    3. **DISTINCTNESS**: Do NOT output multiple items with the exact same timestamp/ID unless they are clearly different objects.
    4. **AUDIO (Video Only)**: Listen to audio if available. Did the user mention damage or brand names?
    5. Return pure JSON.
    
    OUTPUT SCHEMA (List of Objects):
    [
      {{
        "title": "Item Name",
        "timestamp": 2.5,
        "voice_note": "User said...",
        "description": "Sales copy for {platform_strategy}",
        "prices": {{ "quick": 10, "market": 15, "reach": 20 }}
      }}
    ]
    """

    # D. Call the Model
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[uploaded_file, prompt],
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())], 
            temperature=0.3 
        )
    )

    # E. Parse the Result
    try:
        clean_text = clean_json(response.text)
        return json.loads(clean_text)
    except Exception as e:
        print(f"❌ JSON Error. Raw text was:\n{response.text}")
        return []

# --- TEST BLOCK ---
if __name__ == "__main__":
    # You can change this to test.jpg to test images
    test_media = "static/uploads/test.mp4" 
    try:
        results = analyze_media_feed(test_media, "eBay")
        print("\n✅ AI RESULTS:")
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")