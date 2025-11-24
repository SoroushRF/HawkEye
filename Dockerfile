# Use a lightweight Python version
FROM python:3.9-slim

# 1. Install FFmpeg (Critical for your backend_video.py)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean

# 2. Set up the app folder
WORKDIR /app
COPY . .

# 3. Install Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# 4. Start the server using Gunicorn
# It will listen on Port 10000 (Render's default)
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]