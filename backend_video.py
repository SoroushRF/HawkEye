import ffmpeg
import os

def crop_frame(video_path, timestamp, output_folder, item_name):
    """
    Takes a video, goes to a specific timestamp, cuts a square image,
    and saves it to the output folder.
    """
    try:
        # 1. Clean the filename (remove spaces/symbols so Windows doesn't crash)
        clean_name = "".join(x for x in item_name if x.isalnum())[:15]
        filename = f"{clean_name}_{int(timestamp)}.jpg"
        output_path = os.path.join(output_folder, filename)
        
        # 2. Run FFmpeg
        # ss = seek to second
        # scale = resize to 800px width (keeps file size small)
        # vframes = grab only 1 frame
        (
            ffmpeg
            .input(video_path, ss=timestamp)
            .filter('scale', 800, -1)
            .output(output_path, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        print(f"✅ Extracted: {filename}")
        return filename

    except ffmpeg.Error as e:
        # If this prints, your FFmpeg installation is wrong
        print(f"❌ FFmpeg Error: {e.stderr.decode('utf8')}")
        return None
    # TEST BLOCK
if __name__ == "__main__":
    # Fake a call
    crop_frame('static/uploads/test.mp4', 2.0, 'static/products', 'TestItem')