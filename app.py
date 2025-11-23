import os
import urllib.parse
from flask import Flask, render_template, request
from backend_video import crop_frame
from backend_ai import analyze_video_feed

app = Flask(__name__)

# --- CONFIGURATION ---
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PRODUCT_FOLDER'] = 'static/products'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PRODUCT_FOLDER'], exist_ok=True)

# DEMO MODE: Set to True if Wi-Fi fails during the pitch
DEMO_MODE = False 

@app.route('/')
def home():
    return render_template('scan.html')

@app.route('/scan', methods=['POST'])
def scan_endpoint():
    # 1. Validation
    if 'video' not in request.files:
        return "No video uploaded", 400
    
    video = request.files['video']
    
    # Capture inputs
    platform = request.form.get('platform', 'eBay')
    
    # 2. Save Video Locally (This defines video_path!)
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
    video.save(video_path)
    print(f"✅ Video saved to: {video_path}")

    # 3. PANIC BUTTON (Safety Net)
    if DEMO_MODE:
        import json
        import time
        time.sleep(3)
        # Ensure dummy_data.json exists if you use this!
        with open('dummy_data.json') as f:
            return render_template('report.html', listings=json.load(f), platform=platform)

    # 4. Run AI Logic (The Brain)
    try:
        listings = analyze_video_feed(video_path, platform)
    except Exception as e:
        print(f"❌ AI Error: {e}")
        return f"AI Processing Failed: {str(e)}", 500

    # 5. Run Video Logic & BUILD LINKS
    print("✂️ Processing Items...")
    for item in listings:
        # A. Crop Image
        image_name = crop_frame(
            video_path, 
            item.get('timestamp', 0), 
            app.config['PRODUCT_FOLDER'], 
            item.get('title', 'Unknown_Item')
        )
        item['image'] = image_name

        # B. BUILD LIVE MARKET LINKS (The Fix)
        # We URL-encode the title so spaces become %20, etc.
        safe_query = urllib.parse.quote(item['title'])
        
        # Link 1: eBay SOLD Listings (Shows actual market value)
        ebay_link = f"https://www.ebay.com/sch/i.html?_nkw={safe_query}&LH_Sold=1&LH_Complete=1"
        
        # Link 2: Google Shopping
        google_link = f"https://www.google.com/search?q={safe_query}&tbm=shop"
        
        # Add these to the item dictionary
        item['sources'] = [ebay_link, google_link]

    # 6. Render Results
    print(f"🚀 Rendering report with {len(listings)} items...")
    return render_template('report.html', listings=listings, platform=platform)

if __name__ == '__main__':
    # Host 0.0.0.0 allows your phone to connect
    app.run(debug=True, host='0.0.0.0', port=5000)