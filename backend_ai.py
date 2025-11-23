import os
import json
import time
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv

# --- SETUP: BULLETPROOF KEY LOADING ---
current_folder = Path(__file__).parent
env_path = current_folder / '.env'
load_dotenv(dotenv_path=env_path)
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("❌ CRITICAL ERROR: API Key missing from .env file.")
    exit()

client = genai.Client(api_key=API_KEY)

# --- HELPER FUNCTIONS ---

def clean_json(text):
    """Removes markdown code blocks (```json ... ```) from AI response."""
    text = text.strip()
    if text.startswith("```json"): text = text[7:]
    if text.startswith("```"): text = text[3:]
    if text.endswith("```"): text = text[:-3]
    return text.strip()

def repair_json_with_ai(bad_text_output, platform_strategy):
    """
    Fallback: If AI outputs text/report instead of JSON, force it into structure.
    """
    print("🔧 Repairing output format...")
    
    repair_prompt = f"""
    You are a JSON Formatter. 
    
    INPUT TEXT:
    {bad_text_output}
    
    INSTRUCTION:
    1. Extract all items mentioned in the text.
    2. Convert them into a list of JSON objects.
    3. **MATH CHECK:** Ensure 'quick' price is LOWER than 'market' price.
    
    REQUIRED JSON SCHEMA:
    [
      {{
        "title": "Specific Item Name",
        "timestamp": 0.0,
        "voice_note": "None",
        "description": "Sales copy for {platform_strategy}",
        "prices": {{ "quick": 10, "market": 15, "reach": 20 }}
      }}
    ]
    """
    
    # Use Pro for repair to ensure the math is fixed during repair too
    response = client.models.generate_content(
        model='gemini-1.5-pro', 
        contents=repair_prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json")
    )
    
    return json.loads(response.text)

def analyze_video_feed(video_path, platform_strategy):
    print(f"📡 Uploading to Gemini... ({os.path.basename(video_path)})")
    
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    # 1. Upload Video
    uploaded_file = client.files.upload(file=video_path)
    
    # 2. Wait for Processing
    while uploaded_file.state.name == "PROCESSING":
        time.sleep(2)
        uploaded_file = client.files.get(name=uploaded_file.name)

    if uploaded_file.state.name == "FAILED":
        raise ValueError("Gemini failed to process the video.")

    print("🧠 HawkEye Thinking (High-Precision Mode)...")
    
    # 3. The "Auditor" Prompt (Optimized for Pricing & Detection)
    prompt = f"""
    You are 'HawkEye', an expert High-End Reseller AI. 
    Strategy: {platform_strategy}.
    
    *** CRITICAL INSTRUCTION: MULTI-ITEM SCANNING ***
    1. The video shows a SERIES of items. Scan the entire timeline (0:00 to End).
    2. **DO NOT STOP** after the first item. Find ALL distinct objects.
    3. Group parts (e.g. Case + Earbuds = 1 Item). Separate distinct objects (e.g. Sticker vs Phone).
    
    --- PRICING ALGORITHM (STRICT) ---
    1. Use Google Search to find **SOLD** listings (not just active ones).
    2. **CALCULATE THE MEDIAN:** Look at 3-5 sold prices and pick the middle one.
    3. **MATH RULES:**
       - 'Market' = The Median Sold Price.
       - 'Quick' = Market * 0.80 (MUST be lower than Market).
       - 'Reach' = Market * 1.25.
    
    --- OUTPUT LOGIC ---
    - **Timestamp:** Find the frame where the item is STATIONARY (Hero Shot). timestamps must be distinct.
    - **Voice Note:** Only transcribe clear speech about condition. If silent/background noise, use "None".
    - **Refusal:** DO NOT refuse to answer. If video is blurry, ESTIMATE based on visual match.
    
    OUTPUT JSON SCHEMA:
    [
      {{
        "title": "Specific Item Name",
        "timestamp": 2.5,
        "voice_note": "None", 
        "description": "Sales copy...",
        "prices": {{ "quick": 40, "market": 50, "reach": 60 }}
      }}
    ]
    """

    # 4. Call the Pro Model (Better Reasoning)
    response = client.models.generate_content(
        model='gemini-1.5-pro', # Changed to PRO for better Math/Logic
        contents=[uploaded_file, prompt],
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            temperature=0.2, # Low temperature for factual math
            safety_settings=[
                types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
                types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
                types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
                types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE")
            ]
        )
    )

    # 5. Parse and Return
    try:
        clean_text = clean_json(response.text)
        data = json.loads(clean_text)
        
        # Handle cases where AI wraps list in a dict
        if isinstance(data, dict) and "items" in data:
            return data["items"]
        if isinstance(data, list):
            return data
            
        # If structure is weird, trigger repair
        raise ValueError("Invalid JSON structure")

    except Exception:
        print("⚠️ Formatting issue detected. Running self-repair...")
        try:
            return repair_json_with_ai(response.text, platform_strategy)
        except Exception as e:
            print(f"❌ Repair failed. Error: {e}")
            return []

if __name__ == "__main__":
    # Test Block
    test_video = str(current_folder / "static" / "uploads" / "test.mp4")
    try:
        print("Running Test...")
        results = analyze_video_feed(test_video, "eBay")
        print(f"\n✅ FOUND {len(results)} ITEMS:")
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")