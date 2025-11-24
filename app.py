import streamlit as st
import uuid
import time
import json
from typing import Dict, Any

# -----------------------------
# Helper utilities
# -----------------------------

def unique_key(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def kpi_card(title: str, value: str, delta: str = ""):
    st.markdown(
        f"<div style='background:#ffffffcc;padding:12px;border-radius:12px;box-shadow:0 2px 6px rgba(0,0,0,0.06);'>"
        f"<div style='font-size:14px;color:#666'>{title}</div>"
        f"<div style='font-size:20px;font-weight:700;margin-top:6px'>{value}</div>"
        f"<div style='font-size:12px;color:#1f8ef1;margin-top:6px'>{delta}</div>"
        f"</div>", unsafe_allow_html=True)


# -----------------------------
# Presets & utilities
# -----------------------------

PROMPT_PRESETS = {
    "Cinematic Romantic (8s)": "A romantic, cinematic scene of a couple dancing under warm golden lights, close-up shots, soft lens flare, slow camera dolly.",
    "Drone Shot Cityscape": "Sweeping drone shot over downtown at golden hour, wide establishing shots, crisp details, subtle vignette.",
    "Action Sequence (Car Chase)": "High-energy car chase through neon-lit streets, quick cuts, motion blur, dynamic camera shakes.",
}


def load_preset(name: str) -> str:
    return PROMPT_PRESETS.get(name, "")


# -----------------------------
# Layout & styling
# -----------------------------

st.set_page_config(page_title="Veo Studio — Creator UI", layout="wide", initial_sidebar_state="collapsed")

st.markdown(
    """
    <style>
    .stButton>button {border-radius: 10px}
    .stDownloadButton>button {background-color: #1558d6}
    </style>
    """,
    unsafe_allow_html=True,
)

# ensure session ID
if "session_id" not in st.session_state:
    st.session_state["session_id"] = uuid.uuid4().hex

# -----------------------------
# Top header with KPIs
# -----------------------------

col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1])
with col1:
    st.title("Veo Studio — Creator")
    st.caption("Polished UI for text→video, image→video, reference images and more")
with col2:
    kpi_card("Active Jobs", str(len(st.session_state.get("jobs", []))), delta="+2 today")
with col3:
    kpi_card("Avg. Render Time", "00:08:23", delta="-10%")
with col4:
    kpi_card("Errors (24h)", "0", delta="—")

st.markdown("---")

# -----------------------------
# Main tab area
# -----------------------------

tabs = st.tabs(["Text → Video", "Image → Video", "Reference Images", "First+Last Frames", "Extend Video", "Logs & Metrics"])

# -----------------------------
# 1: Text → Video
# -----------------------------
with tabs[0]:
    st.header("Text → Video — Quick Create")
    c1, c2 = st.columns([2, 1])
    with c1:
        prompt = st.text_area("Prompt", height=180, placeholder="Write a cinematic prompt...", key=unique_key("prompt_area"))
        preset = st.selectbox("Load preset", options=["--none--"] + list(PROMPT_PRESETS.keys()), key=unique_key("preset_select"))
        if preset and preset != "--none--":
            if st.button("Load preset into prompt", key=unique_key("load_preset_btn")):
                prompt = load_preset(preset)
                st.experimental_rerun()
        style = st.selectbox("Style", ["Cinematic", "Photorealistic", "Cartoon", "Anime"], key=unique_key("style_select"))
        duration = st.slider("Duration (seconds)", 2, 30, 8, key=unique_key("duration"))
        seed = st.text_input("Seed (optional)", key=unique_key("seed"))

    with c2:
        st.subheader("Reference & Outputs")
        ref_upload = st.file_uploader("Upload a reference image (optional)", type=["png", "jpg", "jpeg"], key=unique_key("ref_upload"))
        st.markdown("**Preview**")
        preview_box = st.empty()
        st.markdown("----")
        if st.button("Generate Video", key=unique_key("gen_text_btn")):
            # minimal optimistic UI flow
            job_id = uuid.uuid4().hex
            jobs = st.session_state.get("jobs", [])
            jobs.append({"id": job_id, "type": "text_to_video", "status": "queued", "prompt": prompt})
            st.session_state["jobs"] = jobs
            with st.spinner("Submitting to backend..."):
                # in a real app: call backend with requests or httpx
                time.sleep(1)
            st.success("Job submitted — polling for completion")

    st.markdown("### Recent Jobs")
    jobs = st.session_state.get("jobs", [])
    for j in reversed(jobs[-5:]):
        st.write(f"[{j['id'][:8]}] {j['type']} — {j.get('status')}")

# -----------------------------
# 2: Image → Video
# -----------------------------
with tabs[1]:
    st.header("Image → Video")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        images = st.file_uploader("Upload 1–10 images (order will determine frames)", accept_multiple_files=True, type=["png", "jpg", "jpeg"], key=unique_key("img_upload"))
        motion_strength = st.slider("Motion Strength", 0, 100, 30, key=unique_key("motion_strength"))
        if st.button("Create from images", key=unique_key("create_from_images")):
            job_id = uuid.uuid4().hex
            jobs = st.session_state.get("jobs", [])
            jobs.append({"id": job_id, "type": "image_to_video", "status": "processing", "files": len(images) if images else 0})
            st.session_state["jobs"] = jobs
            st.info("Starting job...")

    with col_b:
        st.markdown("**Tips**")
        st.write("- Use consistent lighting across images")
        st.write("- Higher resolution images give better results")

# -----------------------------
# 3: Reference Images
# -----------------------------
with tabs[2]:
    st.header("Reference Images — Style Transfer & Guidance")
    ref_imgs = st.file_uploader("Upload reference images (4 recommended)", accept_multiple_files=True, type=["png", "jpg", "jpeg"], key=unique_key("ref_imgs"))
    influence = st.slider("Reference Influence", 0, 100, 60, key=unique_key("ref_influence"))
    if st.button("Generate with references", key=unique_key("gen_refs")):
        job_id = uuid.uuid4().hex
        jobs = st.session_state.get("jobs", [])
        jobs.append({"id": job_id, "type": "reference_images", "status": "queued"})
        st.session_state["jobs"] = jobs
        st.success("Job queued")

# -----------------------------
# 4: First + Last Frames
# -----------------------------
with tabs[3]:
    st.header("First + Last Frame Generation")
    colx, coly = st.columns(2)
    with colx:
        first = st.file_uploader("Upload first frame", type=["png", "jpg", "jpeg"], key=unique_key("first_frame"))
    with coly:
        last = st.file_uploader("Upload last frame", type=["png", "jpg", "jpeg"], key=unique_key("last_frame"))
    inbetweens = st.slider("Number of intermediate frames", 1, 60, 8, key=unique_key("inbetweens"))
    if st.button("Create Transition", key=unique_key("create_transition")):
        job_id = uuid.uuid4().hex
        jobs = st.session_state.get("jobs", [])
        jobs.append({"id": job_id, "type": "first_last", "status": "processing"})
        st.session_state["jobs"] = jobs
        st.info("Transition job started")

# -----------------------------
# 5: Extend Video
# -----------------------------
with tabs[4]:
    st.header("Extend Existing Video")
    base_video = st.file_uploader("Upload base video to extend", type=["mp4", "mov", "webm"], key=unique_key("base_video_upload"))
    extend_seconds = st.number_input("Extend by seconds", min_value=1, max_value=120, value=8, key=unique_key("extend_seconds"))
    if st.button("Extend Video", key=unique_key("extend_video_btn")):
        job_id = uuid.uuid4().hex
        jobs = st.session_state.get("jobs", [])
        jobs.append({"id": job_id, "type": "extend_video", "status": "queued"})
        st.session_state["jobs"] = jobs
        st.success("Extend job queued")

# -----------------------------
# 6: Logs & Metrics
# -----------------------------
with tabs[5]:
    st.header("Logs & Metrics")
    if st.button("Fetch Logs", key=unique_key("fetch_logs")):
        # example static logs
        sample_logs = [
            {"time": "2025-11-24 09:00", "msg": "Job submitted: abc123"},
            {"time": "2025-11-24 09:01", "msg": "Job completed: abc123"},
        ]
        st.json(sample_logs)

    st.markdown("---")
    st.subheader("Usage Chart (example)")
    try:
        import plotly.graph_objects as go
        fig = go.Figure(go.Bar(x=["Mon","Tue","Wed","Thu","Fri"], y=[10,12,8,15,7]))
        fig.update_layout(height=300, margin=dict(t=30,l=0,r=0,b=0))
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.write("Plotly not available")

# -----------------------------
# Footer actions: job manager, error handling
# -----------------------------

st.sidebar.markdown("---")
if st.sidebar.button("Clear jobs"):
    st.session_state["jobs"] = []
    st.experimental_rerun()

if st.session_state.get("jobs"):
    st.sidebar.markdown("### Recent Jobs")
    for j in reversed(st.session_state.get("jobs")[-8:]):
        st.sidebar.write(f"{j['id'][:8]} — {j['type']} — {j.get('status')}")

# lightweight optimistic poll example
if st.session_state.get("jobs"):
    last_job = st.session_state["jobs"][-1]
    if last_job.get("status") in ("queued", "processing"):
        poll = st.sidebar.empty()
        with poll.container():
            st.write(f"Polling job {last_job['id'][:8]} — status: {last_job['status']}")
            progress = st.progress(0)
            for i in range(1, 101, 10):
                time.sleep(0.02)
                progress.progress(i)
            # simulate completion
            last_job["status"] = "completed"
            last_job["result_url"] = "https://example.com/video.mp4"
            st.session_state["jobs"][-1] = last_job
            st.success("Last job completed — ready to download")
            st.download_button("Download video", data=b"FAKE_MP4_BYTES", file_name="render.mp4")


# small helpful footer
st.markdown("---")
st.caption("Need changes? Tell me what UI area to refine next — presets, layout, or accessibility.")
