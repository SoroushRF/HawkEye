import os
import shutil
import urllib.parse
import mimetypes
from flask import Flask, render_template, request
from backend_video import crop_frame
from backend_ai import analyze_media_feed
import datetime

app = Flask(__name__)

# --- CONFIGURATION ---
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PRODUCT_FOLDER'] = 'static/products'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PRODUCT_FOLDER'], exist_ok=True)

# DEMO MODE
DEMO_MODE = False 

@app.route('/')
def home():
    return render_template('scan.html')

@app.route('/scan', methods=['POST'])
def scan_endpoint():
    # 1. Validation
    if 'media_file' not in request.files:
        return "No media uploaded", 400

    media = request.files['media_file']
    filename = media.filename
    
    # Capture inputs
    platform = request.form.get('platform', 'eBay')
    
    # 2. Save Media Locally
    media_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    media.save(media_path)
    print(f"✅ Media saved to: {media_path}")

    # Determine type (Video vs Image)
    mime_type, _ = mimetypes.guess_type(media_path)
    is_video = mime_type and mime_type.startswith('video')

    # 3. PANIC BUTTON
    if DEMO_MODE:
        import json
        import time
        time.sleep(3)
        with open('dummy_data.json') as f:
            scan_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return render_template('report.html', listings=json.load(f), platform=platform, scan_date=scan_date)

    # 4. Run AI Logic (Works for both Image and Video)
    try:
        listings = analyze_media_feed(media_path, platform)
    except Exception as e:
        print(f"❌ AI Error: {e}")
        return f"AI Processing Failed: {str(e)}", 500

    # 5. Process Listings (Crop/Copy & Link Building)
    print("✂️ Processing Items...")
    
    # Track used timestamps to prevent duplicate frames in videos
    used_timestamps = []

    for i, item in enumerate(listings):
        title = item.get('title', 'Unknown_Item')
        
        # --- UNIQUE FILENAME GENERATION ---
        # {Index}_{CleanTitle} guarantees Item 1's pic != Item 2's pic
        clean_title = "".join(x for x in title if x.isalnum())[:10]
        unique_filename = f"{i}_{clean_title}.jpg"
        output_path = os.path.join(app.config['PRODUCT_FOLDER'], unique_filename)

        if is_video:
            # === VIDEO LOGIC ===
            raw_time = float(item.get('timestamp', 0))
            
            # Timestamp Shifting (Collision Avoidance)
            adjusted_time = raw_time
            for used_time in used_timestamps:
                if abs(adjusted_time - used_time) < 1.5:
                    print(f"   ⚠️ Timestamp collision at {adjusted_time}s. Shifting +2s...")
                    adjusted_time += 2.0
            
            used_timestamps.append(adjusted_time)
            
            # Extract Frame
            crop_frame(media_path, adjusted_time, app.config['PRODUCT_FOLDER'], f"{i}_{clean_title}")
            
            # Update Item Data
            item['image'] = unique_filename
            item['timestamp'] = f"{round(adjusted_time, 1)}s"
            
        else:
            # === IMAGE LOGIC ===
            # No cropping needed. We copy the source image for this item.
            # If the user uploaded one photo with 3 items, all 3 items get the full photo.
            shutil.copy(media_path, output_path)
            
            # Update Item Data
            item['image'] = unique_filename
            item['timestamp'] = "(Still Image)"

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