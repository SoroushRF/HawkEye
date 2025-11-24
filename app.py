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

    # 3. PANIC BUTTON
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
    
    # DEBUG: Print the whole list to see timestamps
    print(f"🔍 RAW AI DATA: {listings}")

    for i, item in enumerate(listings):
        print(f"   Processing Item {i+1}: {item.get('title')}")
        
        # A. Crop Image
        image_name = crop_frame(
            video_path, 
            item.get('timestamp', 0), 
            app.config['PRODUCT_FOLDER'], 
            item.get('title', 'Unknown_Item')
        )
        
        # CRITICAL FIX: Force unique assignment
        item['image'] = image_name
        print(f"      -> Generated Image: {image_name}")

        # B. BUILD LIVE MARKET LINKS
        safe_query = urllib.parse.quote(item['title'])
        
        ebay_link = f"https://www.ebay.com/sch/i.html?_nkw={safe_query}&LH_Sold=1&LH_Complete=1"
        google_link = f"https://www.google.com/search?q={safe_query}&tbm=shop"
        
        item['sources'] = [ebay_link, google_link]

    # 6. Render Results
    print(f"🚀 Rendering report with {len(listings)} items...")
    scan_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('report.html', listings=listings, platform=platform, scan_date=scan_date)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)