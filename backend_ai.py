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
    """
    Helper to strip markdown formatting (```json ... ```) 
    that Gemini sometimes adds when Search is enabled.
    """
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:] 
    if text.startswith("```"):
        text = text[3:] 
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def analyze_video_feed(video_path, platform_strategy):
    """
    Sends the video to Gemini 2.5 and returns a list of items found.
    """
    
    # A. Upload Video
    print(f"📡 Uploading to Gemini... ({os.path.basename(video_path)})")
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    uploaded_file = client.files.upload(file=video_path)
    
    # B. Wait for Google to Process it
    while uploaded_file.state.name == "PROCESSING":
        print("... AI is watching the video ...")
        time.sleep(2)
        uploaded_file = client.files.get(name=uploaded_file.name)

    if uploaded_file.state.name == "FAILED":
        raise ValueError("Gemini failed to process the video.")

    # C. The "HawkEye" Prompt (HARDENED FOR HACKATHON)
    print("🧠 HawkEye Thinking...")
    
    prompt = f"""
    You are 'HawkEye', an expert reseller AI.
    Strategy: {platform_strategy}.
    
    INSTRUCTIONS:
    1. Watch the video. Identify EVERY distinct item you see.
    2. **TIMESTAMPS**: Provide the exact timestamp (in seconds) where the item is MOST VISIBLE. 
    3. **IMPORTANT**: Ensure timestamps are distinct. Do not put all items at 0.0s. Spread them out as they appear.
    4. Listen to the AUDIO. Did the user mention damage or brand names?
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
    test_video = "static/uploads/test.mp4"
    try:
        results = analyze_video_feed(test_video, "eBay")
        print("\n✅ AI RESULTS:")
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")