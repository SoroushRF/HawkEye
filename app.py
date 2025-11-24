import os
import urllib.parse
from flask import Flask, render_template, request
from backend_video import crop_frame
from backend_ai import analyze_video_feed
import datetime

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
    if 'media_file' not in request.files:
        return "No video uploaded", 400

    video = request.files['media_file']
    
    # Capture inputs
    platform = request.form.get('platform', 'eBay')
    
    # 2. Save Video Locally
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
    video.save(video_path)
    print(f"✅ Video saved to: {video_path}")

    # 3. PANIC BUTTON (Demo Mode)
    if DEMO_MODE:
        import json
        import time
        time.sleep(3)
        with open('dummy_data.json') as f:
            scan_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return render_template('report.html', listings=json.load(f), platform=platform, scan_date=scan_date)

    # 4. Run AI Logic
    try:
        listings = analyze_video_feed(video_path, platform)
    except Exception as e:
        print(f"❌ AI Error: {e}")
        return f"AI Processing Failed: {str(e)}", 500

    # 5. Run Video Logic & BUILD LINKS
    print("✂️ Processing Items...")
    
    # Used to prevent duplicate timestamps
    seen_timestamps = set()

    for i, item in enumerate(listings):
        title = item.get('title', 'Unknown_Item')
        timestamp = float(item.get('timestamp', 0))
        
        print(f"   Processing Item {i+1}: {title} at {timestamp}s")
        
        # --- TIMESTAMP DE-DUPLICATION ---
        # If this timestamp was already used (e.g. two items at 0:05), 
        # bump this one by 1.5 seconds to try and find a distinct frame.
        if int(timestamp) in seen_timestamps:
            print(f"      ⚠️ Duplicate timestamp detected. Shifting {timestamp} -> {timestamp + 1.5}")
            timestamp += 1.5
        
        seen_timestamps.add(int(timestamp))
        
        # --- UNIQUE FILENAME GENERATION ---
        # We append the index 'i' to the name. 
        # This prevents "Shirt" overwriting the previous "Shirt".
        clean_title = "".join(x for x in title if x.isalnum())[:10]
        unique_name_for_file = f"{i}_{clean_title}"

        # A. Crop Image
        image_name = crop_frame(
            video_path, 
            timestamp, 
            app.config['PRODUCT_FOLDER'], 
            unique_name_for_file 
        )
        
        # Assign the unique image to this specific item
        item['image'] = image_name
        # Update timestamp in display to match the shifted one
        item['timestamp'] = round(timestamp, 1)

        print(f"      -> Generated Image: {image_name}")

        # B. BUILD LIVE MARKET LINKS
        safe_query = urllib.parse.quote(title)
        
        ebay_link = f"https://www.ebay.com/sch/i.html?_nkw={safe_query}&LH_Sold=1&LH_Complete=1"
        google_link = f"https://www.google.com/search?q={safe_query}&tbm=shop"
        
        item['sources'] = [ebay_link, google_link]

    # 6. Render Results
    print(f"🚀 Rendering report with {len(listings)} items...")
    scan_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('report.html', listings=listings, platform=platform, scan_date=scan_date)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)