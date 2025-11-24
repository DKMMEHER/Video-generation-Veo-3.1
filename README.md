🚀 Veo Video Generation Suite
Text → Video • Image → Video • Reference Images • First + Last Frames • Extend Video

This project is a full-featured AI Video Generation Suite built using:

Streamlit (Frontend)

FastAPI (Backend)

Google Veo 3.1 / 3.1-Fast APIs

FFmpeg (Video processing)

It supports five advanced video-generation workflows with a clean UI and cloud-ready backend.

✨ Features
🎬 1. Text → Video

Generate cinematic videos from plain text prompts.

🖼️ 2. Image → Video

Upload an image → Animate it into a realistic AI-generated video.

🧩 3. Multiple Reference Images

Use 2–6 reference images to generate consistent characters across the video.

📘 4. First + Last Frame → Video

Provide starting & ending frames → system generates smooth in-between motion.

➕ 5. Extend an Existing Video

Upload any Veo-generated clip → extend it forward with visual consistency.

🧱 Tech Stack
Layer	Technologies
Frontend	Streamlit, Plotly, Python
Backend	FastAPI, Pydantic
AI Models	Google Veo 3.1, Veo 3.1-Fast
Video Tools	FFmpeg
Environment	Python 3.10+



Access_to_Veo3/
│── app.py                 # Streamlit UI
│── backend.py             # FastAPI backend
│── helper.py              # Video utilities, FFmpeg helpers
│── requirements.txt
│── .gitignore
│── Dependencies/          # FFmpeg, binaries

