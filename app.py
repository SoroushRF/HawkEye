import os
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
    if 'video' not in request.files:
        return "No video uploaded", 400
    
    video = request.files['video']
    
    # Capture the new inputs from your friend's form
    platform = request.form.get('platform', 'eBay')
    confidence = request.form.get('confidence', '75') # New!
    
    # ... rest of your code ...
    
    # 2. Save Video Locally
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
    video.save(video_path)
    print(f"✅ Video saved to: {video_path}")

    # 3. PANIC BUTTON (Safety Net)
    if DEMO_MODE:
        import json
        import time
        time.sleep(3)
        # You will create this file later as a backup
        with open('dummy_data.json') as f:
            return render_template('report.html', listings=json.load(f), platform=platform)

    # 4. Run AI Logic (The Brain)
    try:
        # Call the function you just verified
        listings = analyze_video_feed(video_path, platform)
    except Exception as e:
        print(f"❌ AI Error: {e}")
        return f"AI Processing Failed: {str(e)}", 500

    # 5. Run Video Logic (The Cropper)
    print("✂️ Cutting images based on AI timestamps...")
    for item in listings:
        # Use .get() to be safe if AI forgets a field
        timestamp = item.get('timestamp', 0)
        title = item.get('title', 'Unknown_Item')
        
        # Call the FFmpeg function
        image_name = crop_frame(
            video_path, 
            timestamp, 
            app.config['PRODUCT_FOLDER'], 
            title
        )
        
        # Add the filename to the dictionary so HTML can find it
        item['image'] = image_name

    # 6. Render Results
    print(f"🚀 Rendering report with {len(listings)} items...")
    return render_template('report.html', listings=listings, platform=platform)

if __name__ == '__main__':
    # Host 0.0.0.0 allows your phone to connect
    app.run(debug=True, host='0.0.0.0', port=5000)