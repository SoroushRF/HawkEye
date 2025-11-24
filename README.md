# HawkEye

HawkEye is a small web-backed Python project that provides a browser UI and video/AI backend components. The backend extracts items from short video clips using Google's Gemini model and builds quick marketplace links and thumbnail crops for each detected item.

This README explains how to run the project locally (via a VS Code venv), what environment variables are required, and key implementation notes.

Table of contents
- Quickstart (VS Code / local)
- Docker (optional)
- Configuration (.env and API key)
- Requirements
- Key files
- Project layout
- Notes & troubleshooting
- License

Quickstart (VS Code / local)
1. Open this repository in VS Code.

2. Create and activate a virtual environment (in the integrated terminal):
   - Create venv:
     python -m venv .venv
   - Activate:
     - macOS / Linux:
       source .venv/bin/activate
     - Windows (PowerShell):
       .venv\Scripts\Activate.ps1
     - Windows (cmd):
       .venv\Scripts\activate.bat

   In VS Code, select the created interpreter (.venv) from the Command Palette → Python: Select Interpreter so the terminal uses the venv automatically.

3. Install dependencies:
   pip install -r requirements.txt

4. Create a .env file (see "Configuration" below), then run the app:
   python app.py

5. Open the app in your browser:
   http://127.0.0.1:5000/

(If you run the app inside Docker / with Gunicorn, the container uses port 10000 — see the Docker section.)

Docker (optional)
A Dockerfile is included and installs ffmpeg and Python dependencies, then runs Gunicorn serving app:app on port 10000.

Build and run:
- Build:
  docker build -t hawkeye:latest .
- Run:
  docker run -d -p 10000:10000 --name hawkeye hawkeye:latest
- Open:
  http://127.0.0.1:10000/

Configuration (.env and API key)
- Create a .env file in the repository root.
- Add your Gemini API key (the app expects GEMINI_API_KEY):
  GEMINI_API_KEY=your_api_key_here

Important:
- backend_ai.py uses Google's GenAI client and is configured to call the gemini-2.5-flash model. Provide your own API key; the app will exit if GEMINI_API_KEY is not set.
- backend_video.py requires ffmpeg for video frame extraction. If running locally (not in Docker), install ffmpeg on your host (apt, brew, or from ffmpeg.org).

Requirements
- Python 3.9+ (project uses python:3.9-slim in Dockerfile)
- pip
- ffmpeg (system binary) for local video processing
- Python packages listed in requirements.txt:
  pip install -r requirements.txt

Key files
- app.py — Flask application and main entrypoint. Running python app.py serves the web UI on 0.0.0.0:5000 by default.
- backend_ai.py — Handles uploading video to Gemini and generating the JSON report. Uses model: gemini-2.5-flash.
- backend_video.py — Video processing utilities (frame cropping, thumbnails). Depends on ffmpeg.
- requirements.txt — Python dependencies.
- Dockerfile — Builds an image with ffmpeg and runs Gunicorn (app:app) on port 10000.
- templates/ and static/ — Frontend HTML/CSS/JS and uploaded/derived media folders.

Project layout (important paths)
- app.py
- backend_ai.py
- backend_video.py
- requirements.txt
- Dockerfile
- templates/ (HTML)
- static/
  - uploads/ (incoming videos)
  - products/ (generated thumbnails)

Notes & troubleshooting
- Missing API key: backend_ai.py loads GEMINI_API_KEY from .env and will exit if not found. Create .env with your key before running.
- FFmpeg: If you get errors when crops or frames are generated, ensure ffmpeg is installed and available in PATH.
- Local dev vs Docker:
  - Local quick dev: python app.py → http://127.0.0.1:5000/
  - Docker (production-like): gunicorn app:app → container exposes port 10000 (http://127.0.0.1:10000/)

Security & privacy
- Do not commit your .env with real API keys. Add .env to .gitignore.
- Video files uploaded to static/uploads are stored locally; handle sensitive content accordingly.

Acknowledgements
- Gemini model: this repository uses the gemini-2.5-flash model in backend_ai.py for video understanding and JSON generation.

License
- See repository LICENSE file for terms.
