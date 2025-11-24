![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

# HawkEye: AI-Powered Video Analysis 🦅

HawkEye is a tool that turns an inventory into cash. By analyzing a single video of multiple items, it identifies products, detects condition issues, it saves resellers hours of manual listing work.

### 🏆 A 12-Hour Hackathon Project

HawkEye was born out of the **CSHub Local Day Hack**, an intense **12-hour coding competition**. The challenge was to build a project from zero to a fully functional, demo-ready product within the strict time limit.

A core requirement of the hackathon was to integrate the powerful **Google Gemini API**, pushing us to rapidly learn and implement its capabilities. This project is the result of that effort, showcasing what can be built and deployed in just half a day.

### 👥 Our Team

*   **Soroush - Backend Lead**
    *   Architected the core backend using **Flask**, creating a robust server to handle all application logic.
    *   Engineered the **Google Gemini** integration, enabling the multi-modal analysis that serves as the project's cognitive engine.
    *   Developed the **FFmpeg** video processing pipeline, responsible for efficient frame extraction and precise timestamping.
    *   Orchestrated the containerization with **Docker** and managed the final deployment on **Render**.

*   **Parsa - Frontend Lead**
    *   Designed and implemented the "Tactical" UI/UX with **Tailwind CSS**, focusing on a clean and intuitive user experience.
    *   Built the responsive scanning interface, including the signature "Radar" animation and a "Cinema Mode" for enhanced usability.
    *   Optimized the frontend JavaScript for **iOS PWA compatibility**, resolving critical touch event and file input challenges on mobile devices.

### 🚀 The Power of Google Gemini

We leveraged Google Gemini to empower HawkEye with multi-modal intelligence. Gemini (2.5 Flash API) synthesizes uploaded audiovisual and static media to:

*   **Classify inventory** (e.g., "Vintage Levi's 501 Jeans")
*   **Extract auditory condition reports** (e.g., "Missing button on cuff")
*   **Appraise market value** (by scraping live pricing data)

Gemini serves as the cognitive engine bridging visual inputs and resale analytics, interpreting multimedia streams instantly to automate listing operations.

### 🛠️ Tech Stack

| Category | Technologies |
| :--- | :--- |
| **Backend** | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) |
| **AI & Data** | ![Google Gemini](https://img.shields.io/badge/Google_Gemini-4A90E2?style=for-the-badge&logo=google-gemini&logoColor=white) ![FFmpeg](https://img.shields.io/badge/FFmpeg-007800?style=for-the-badge&logo=ffmpeg&logoColor=white) |
| **Frontend** | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) |
| **DevOps** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white) |

### Key Features

*   **Easy Video Upload**: A simple, user-friendly interface for uploading video files.
*   **Advanced AI Analysis**: Leverages Google's powerful Gemini 2.5 Flash model to understand video content.
*   **Frame-by-Frame Processing**: Uses FFmpeg to efficiently extract and analyze video frames.
*   **Text-Based Summaries**: Generates clear and concise descriptions of the video's content.
*   **Containerized & Deployable**: Fully containerized with Docker for easy deployment on any platform.

### Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

#### Prerequisites

*   Python 3.9+
*   Docker (Recommended)
*   An API key for Google Gemini

#### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/SoroushRF/HawkEye.git
    cd HawkEye
    ```

2.  **Set up your environment variables:**
    Create a file named `.env` in the root of the project and add your Google Gemini API key:
    ```env
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```

3.  **Build and run with Docker (Recommended):**
    Ensure Docker is running on your machine, then execute:
    ```sh
    docker build -t hawkeye-app .
    docker run -p 5000:10000 -v $(pwd):/app hawkeye-app
    ```
    The application will be available at `http://localhost:5000`.

4.  **Run locally without Docker:**
    Install the required Python packages and FFmpeg:
    ```sh
    # Install Python dependencies
    pip install -r requirements.txt

    # Install FFmpeg (example for Debian/Ubuntu)
    sudo apt-get update && sudo apt-get install ffmpeg

    # Run the Flask app
    python app.py
    ```
    The application will be available at `http://127.0.0.1:5000`.

### How It Works

1.  **Video Upload**: The user uploads a video file through the Flask web interface.
2.  **Frame Extraction**: The `backend_video.py` script uses **FFmpeg** to extract frames from the video at a rate of one frame per second.
3.  **AI Analysis**: The extracted frames are passed to the `backend_ai.py` script, which communicates with the **Google Gemini API**.
4.  **Content Generation**: The Gemini model analyzes the sequence of frames and generates a descriptive text summary of the video's content.
5.  **Display Results**: The generated text is displayed back to the user on the web interface.

### Deployment

This application is containerized with Docker and can be easily deployed on cloud services like Render, Heroku, or AWS. The included `Dockerfile` and `gunicorn` dependency are configured for a production environment. On Render, the app will automatically be served on port 10000.
