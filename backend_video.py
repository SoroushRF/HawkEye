import ffmpeg
import os
import uuid # NEW IMPORT

def crop_frame(video_path, timestamp, output_folder, item_name):
    try:
        # Generate a unique ID so images never overwrite each other
        unique_id = str(uuid.uuid4())[:8]
        
        # Clean name + Timestamp + Unique ID
        clean_name = "".join(x for x in item_name if x.isalnum())[:10]
        filename = f"{clean_name}_{int(timestamp)}_{unique_id}.jpg"
        
        output_path = os.path.join(output_folder, filename)
        
        (
            ffmpeg
            .input(video_path, ss=timestamp)
            .filter('scale', 1080, -1)
            .output(output_path, vframes=1, **{'q:v': 2})
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return filename

    except ffmpeg.Error as e:
        print(f"❌ FFmpeg Error: {e.stderr.decode('utf8')}")
        return None