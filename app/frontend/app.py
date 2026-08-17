from __future__ import annotations
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
import time
import json
import requests
from typing import List, Dict, Any

API_BASE = "http://127.0.0.1:8432/api/v1"

st.set_page_config(
    page_title="EcoInfraMind AI",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    .stSidebar { background-color: #1a1d24; }
    .stChatMessage { border-radius: 12px; padding: 12px; margin: 8px 0; }
    .metric-card { background: #1e2128; border-radius: 8px; padding: 16px; text-align: center; }
    .main-header { color: #4fc3f7; font-size: 1.8rem; font-weight: 600; }
    .stButton>button { border-radius: 8px; }
    div[data-testid="stChatMessageContent"] p { margin: 0; }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "expert_messages" not in st.session_state:
        st.session_state.expert_messages = {}
    if "expert_type" not in st.session_state:
        st.session_state.expert_type = "engineering"
    if "calc_results" not in st.session_state:
        st.session_state.calc_results = {}
    if "page" not in st.session_state:
        st.session_state.page = "Chat"


init_session_state()


def api_health():
    try:
        r = requests.get(f"{API_BASE}/health", timeout=5)
        return r.json()
    except:
        return {"status": "offline"}


def api_chat(message: str, history: list) -> dict:
    try:
        r = requests.post(f"{API_BASE}/chat", json={"message": message, "history": history}, timeout=120)
        return r.json()
    except Exception as e:
        return {"response": f"Error: {e}", "cpu_percent": 0, "ram_gb": 0, "response_time_s": 0, "tokens": 0}


def api_expert(message: str, expert_type: str, history: list) -> dict:
    try:
        r = requests.post(
            f"{API_BASE}/expert",
            json={"message": message, "expert_type": expert_type, "history": history},
            timeout=120,
        )
        return r.json()
    except Exception as e:
        return {"response": f"Error: {e}", "cpu_percent": 0, "ram_gb": 0, "response_time_s": 0, "tokens": 0}


def api_upload(file) -> dict:
    try:
        r = requests.post(f"{API_BASE}/upload", files={"file": file}, timeout=120)
        return r.json()
    except Exception as e:
        return {"filename": file.name, "chunks_indexed": 0, "status": f"error: {e}"}


def api_knowledge_stats() -> dict:
    try:
        r = requests.get(f"{API_BASE}/knowledge/stats", timeout=10)
        return r.json()
    except:
        return {"total_chunks": 0, "status": "offline"}


def api_calculator(calc_name: str, params: dict) -> dict:
    try:
        r = requests.post(f"{API_BASE}/calculator", json={"calculator": calc_name, "params": params}, timeout=30)
        return r.json()
    except Exception as e:
        return {"result": {"error": str(e)}, "cpu_percent": 0, "ram_gb": 0}


def api_metrics() -> dict:
    try:
        r = requests.get(f"{API_BASE}/metrics", timeout=5)
        return r.json()
    except:
        return {}


def render_metrics(cpu: float, ram: float, time_s: float = 0, tokens: int = 0):
    cols = st.columns(4)
    cols[0].metric("CPU", f"{cpu:.1f}%")
    cols[1].metric("RAM", f"{ram:.2f} GB")
    if time_s:
        cols[2].metric("Response Time", f"{time_s:.2f}s")
    if tokens:
        cols[3].metric("Tokens", tokens)


def chat_page():
    st.markdown('<p class="main-header">💬 EcoInfraMind AI Chat</p>', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask an engineering question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("EcoInfraMind is thinking..."):
                result = api_chat(prompt, st.session_state.messages[:-1])
                response = result.get("response", "No response")
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

            render_metrics(
                result.get("cpu_percent", 0),
                result.get("ram_gb", 0),
                result.get("response_time_s", 0),
                result.get("tokens", 0),
            )

    if st.button("🗑️ Reset Conversation"):
        st.session_state.messages = []
        st.rerun()


def expert_page():
    expert_type = st.sidebar.selectbox(
        "Expert Mode",
        ["engineering", "climate", "proposal", "research"],
        index=["engineering", "climate", "proposal", "research"].index(st.session_state.expert_type),
    )
    st.session_state.expert_type = expert_type

    labels = {
        "engineering": "🏗️ Engineering Expert",
        "climate": "🌿 Climate & Sustainability",
        "proposal": "📋 Proposal Generator",
        "research": "📚 Research Assistant",
    }
    st.markdown(f'<p class="main-header">{labels[expert_type]}</p>', unsafe_allow_html=True)

    if expert_type not in st.session_state.expert_messages:
        st.session_state.expert_messages[expert_type] = []

    messages = st.session_state.expert_messages[expert_type]
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask your expert question..."):
        messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner(f"{labels[expert_type]} is working..."):
                result = api_expert(prompt, expert_type, messages[:-1])
                response = result.get("response", "No response")
                st.markdown(response)
                messages.append({"role": "assistant", "content": response})

            render_metrics(
                result.get("cpu_percent", 0),
                result.get("ram_gb", 0),
                result.get("response_time_s", 0),
                result.get("tokens", 0),
            )

    if st.button("🗑️ Clear"):
        st.session_state.expert_messages[expert_type] = []
        st.rerun()


def upload_page():
    st.markdown('<p class="main-header">📄 Document Intelligence</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        uploaded_file = st.file_uploader(
            "Upload Engineering Document",
            type=["pdf", "docx", "txt", "md"],
            help="Upload PDF, DOCX, TXT, or Markdown files",
        )
        if uploaded_file:
            with st.spinner("Processing document..."):
                result = api_upload(uploaded_file)
            if result["status"] == "indexed":
                st.success(f"✅ {result['filename']}: {result['chunks_indexed']} chunks indexed")
            else:
                st.warning(f"⚠️ {result['filename']}: {result['status']}")

    with col2:
        st.markdown("### Knowledge Base")
        stats = api_knowledge_stats()
        st.metric("Total Chunks", stats.get("total_chunks", 0))
        st.metric("Status", stats.get("status", "unknown"))

        if st.button("🔄 Index Knowledge Folder"):
            with st.spinner("Indexing knowledge base..."):
                try:
                    r = requests.post(f"{API_BASE}/knowledge/index-all", timeout=300)
                    data = r.json()
                    st.success(f"Indexed {data.get('files_indexed', 0)} chunks")
                except Exception as e:
                    st.error(f"Indexing error: {e}")

        if st.button("🗑️ Clear Knowledge Base"):
            try:
                requests.post(f"{API_BASE}/knowledge/clear", timeout=10)
                st.success("Knowledge base cleared")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")


def calculator_page():
    st.markdown('<p class="main-header">🧮 Engineering Calculators</p>', unsafe_allow_html=True)

    calc_type = st.selectbox(
        "Select Calculator",
        [
            "Concrete Mix Ratio",
            "Traffic Volume",
            "AADT Calculation",
            "Pavement Thickness",
            "Earthwork Volume",
            "Drainage Flow",
            "Bearing Capacity",
            "Area Calculator",
            "Volume Calculator",
            "Slope Calculator",
            "Unit Conversion",
        ]
    )

    result = None

    if calc_type == "Concrete Mix Ratio":
        col1, col2 = st.columns(2)
        with col1:
            cement = st.number_input("Cement (kg)", min_value=0.0, value=350.0, step=10.0)
            sand = st.number_input("Sand (kg)", min_value=0.0, value=700.0, step=10.0)
        with col2:
            aggregate = st.number_input("Aggregate (kg)", min_value=0.0, value=1400.0, step=10.0)
            water = st.number_input("Water (kg)", min_value=0.0, value=175.0, step=5.0)
        if st.button("Calculate Mix"):
            result = api_calculator("concrete_mix", {"cement": cement, "sand": sand, "aggregate": aggregate, "water": water})

    elif calc_type == "Traffic Volume":
        col1, col2 = st.columns(2)
        with col1:
            vehicles = st.number_input("Vehicle Count", min_value=0, value=500)
        with col2:
            minutes = st.number_input("Observation Time (minutes)", min_value=1, value=60)
        if st.button("Calculate Volume"):
            result = api_calculator("traffic_volume", {"vehicle_count": vehicles, "observation_time_minutes": minutes})

    elif calc_type == "AADT Calculation":
        st.markdown("Enter daily traffic counts (comma-separated):")
        counts_str = st.text_input("Daily Counts", "1200,1350,1100,1400,1250,1300,1280")
        adj = st.number_input("Adjustment Factor", min_value=0.1, value=1.0, step=0.1)
        if st.button("Calculate AADT"):
            counts = [float(x.strip()) for x in counts_str.split(",") if x.strip()]
            result = api_calculator("aadt", {"daily_counts": counts, "adjustment_factor": adj})

    elif calc_type == "Pavement Thickness":
        col1, col2, col3 = st.columns(3)
        with col1:
            cbr = st.number_input("CBR Value (%)", min_value=0.1, value=15.0)
        with col2:
            esa = st.number_input("Traffic ESA (millions)", min_value=0.1, value=5.0)
        with col3:
            reliability = st.number_input("Reliability (%)", min_value=50.0, value=90.0)
        if st.button("Calculate Thickness"):
            result = api_calculator("pavement_thickness", {"cbr": cbr, "traffic_esa": esa * 1e6 if esa < 1000 else esa, "reliability": reliability})

    elif calc_type == "Earthwork Volume":
        col1, col2, col3 = st.columns(3)
        with col1:
            length = st.number_input("Length (m)", min_value=0.1, value=100.0)
        with col2:
            width = st.number_input("Width (m)", min_value=0.1, value=20.0)
        with col3:
            depth = st.number_input("Depth (m)", min_value=0.1, value=2.0)
        swell = st.number_input("Swell Factor", min_value=1.0, value=1.25, step=0.05)
        if st.button("Calculate Volume"):
            result = api_calculator("earthwork", {"length": length, "width": width, "depth": depth, "swell_factor": swell})

    elif calc_type == "Drainage Flow":
        col1, col2, col3 = st.columns(3)
        with col1:
            area = st.number_input("Catchment Area (ha)", min_value=0.1, value=50.0)
        with col2:
            runoff = st.number_input("Runoff Coefficient (C)", min_value=0.0, max_value=1.0, value=0.6, step=0.05)
        with col3:
            intensity = st.number_input("Rainfall Intensity (mm/hr)", min_value=0.1, value=50.0)
        if st.button("Calculate Flow"):
            result = api_calculator("drainage", {"area_ha": area, "runoff_coefficient": runoff, "rainfall_intensity_mm_hr": intensity})

    elif calc_type == "Bearing Capacity":
        col1, col2 = st.columns(2)
        with col1:
            cohesion = st.number_input("Cohesion (kPa)", min_value=0.0, value=25.0)
            unit_weight = st.number_input("Unit Weight (kN/m³)", min_value=0.0, value=18.0)
            phi = st.number_input("Friction Angle (°)", min_value=0.0, value=30.0)
        with col2:
            width = st.number_input("Foundation Width (m)", min_value=0.1, value=1.5)
            depth = st.number_input("Foundation Depth (m)", min_value=0.0, value=1.0)
            sf = st.number_input("Safety Factor", min_value=1.0, value=3.0)
        if st.button("Calculate Capacity"):
            result = api_calculator("bearing_capacity", {"cohesion": cohesion, "unit_weight": unit_weight, "width": width, "depth": depth, "phi_deg": phi, "safety_factor": sf})

    elif calc_type == "Area Calculator":
        shape = st.selectbox("Shape", ["rectangle", "circle", "triangle", "trapezoid"])
        params = {"shape": shape}
        if shape == "rectangle":
            cols = st.columns(2)
            params["length"] = cols[0].number_input("Length (m)", value=10.0)
            params["width"] = cols[1].number_input("Width (m)", value=5.0)
        elif shape == "circle":
            params["radius"] = st.number_input("Radius (m)", value=5.0)
        elif shape == "triangle":
            cols = st.columns(2)
            params["base"] = cols[0].number_input("Base (m)", value=10.0)
            params["height"] = cols[1].number_input("Height (m)", value=5.0)
        elif shape == "trapezoid":
            cols = st.columns(3)
            params["base1"] = cols[0].number_input("Base 1 (m)", value=10.0)
            params["base2"] = cols[1].number_input("Base 2 (m)", value=6.0)
            params["height"] = cols[2].number_input("Height (m)", value=4.0)
        if st.button("Calculate Area"):
            result = api_calculator("area", params)

    elif calc_type == "Volume Calculator":
        shape = st.selectbox("Shape", ["cube", "cylinder", "sphere", "cone"])
        params = {"shape": shape}
        if shape == "cube":
            params["side"] = st.number_input("Side (m)", value=5.0)
        elif shape == "cylinder":
            cols = st.columns(2)
            params["radius"] = cols[0].number_input("Radius (m)", value=3.0)
            params["height"] = cols[1].number_input("Height (m)", value=10.0)
        elif shape == "sphere":
            params["radius"] = st.number_input("Radius (m)", value=5.0)
        elif shape == "cone":
            cols = st.columns(2)
            params["radius"] = cols[0].number_input("Radius (m)", value=3.0)
            params["height"] = cols[1].number_input("Height (m)", value=9.0)
        if st.button("Calculate Volume"):
            result = api_calculator("volume", params)

    elif calc_type == "Slope Calculator":
        col1, col2 = st.columns(2)
        with col1:
            rise = st.number_input("Rise (m)", min_value=0.0, value=5.0)
        with col2:
            run = st.number_input("Run (m)", min_value=0.1, value=100.0)
        if st.button("Calculate Slope"):
            result = api_calculator("slope", {"rise": rise, "run": run})

    elif calc_type == "Unit Conversion":
        col1, col2 = st.columns(2)
        with col1:
            value = st.number_input("Value", value=1.0)
            from_unit = st.text_input("From Unit", "m")
        with col2:
            to_unit = st.text_input("To Unit", "ft")
        if st.button("Convert"):
            result = api_calculator("unit_conversion", {"value": value, "from_unit": from_unit, "to_unit": to_unit})

    if result:
        res_data = result.get("result", {})
        if "error" in res_data:
            st.error(res_data["error"])
        else:
            st.success("Calculation Result")
            for k, v in res_data.items():
                if k != "error":
                    st.metric(k.replace("_", " ").title(), v)
            render_metrics(result.get("cpu_percent", 0), result.get("ram_gb", 0))


def settings_page():
    st.markdown('<p class="main-header">⚙️ Settings & Metrics</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("System Metrics")
        metrics = api_metrics()
        if metrics:
            st.metric("CPU Usage", f"{metrics.get('cpu_percent', 0):.1f}%")
            st.metric("RAM Usage", f"{metrics.get('ram_gb', 0):.2f} GB")
            st.metric("RAM Percent", f"{metrics.get('ram_percent', 0):.1f}%")
            st.metric("Model Loaded", "✅ Yes" if metrics.get("model_loaded") else "❌ No")
            st.metric("Cache Size", metrics.get("cache_size", 0))
        else:
            st.warning("API not reachable. Start the backend server.")

    with col2:
        st.subheader("Knowledge Base")
        stats = api_knowledge_stats()
        st.metric("Total Indexed Chunks", stats.get("total_chunks", 0))
        st.metric("Status", stats.get("status", "unknown"))

    st.subheader("About EcoInfraMind AI")
    st.markdown("""
    **EcoInfraMind AI** v1.0.0 - Offline African Infrastructure Intelligence Assistant
    
    - **LLM**: Qwen2.5-3B-Instruct (4-bit GGUF)
    - **Embeddings**: nomic-embed-text
    - **Vector DB**: ChromaDB
    - **Framework**: FastAPI + Streamlit
    
    Built for the Africa Deep Tech Challenge 2026.
    """)


def main():
    st.sidebar.markdown("## 🏗️ EcoInfraMind AI")
    st.sidebar.markdown("---")

    health = api_health()
    if health.get("status") == "ok":
        st.sidebar.success("✅ API Connected")
    else:
        st.sidebar.error("❌ API Offline")

    pages = {
        "Chat": chat_page,
        "Expert Assistant": expert_page,
        "Document Intelligence": upload_page,
        "Calculators": calculator_page,
        "Settings": settings_page,
    }

    selection = st.sidebar.radio("Navigation", list(pages.keys()))
    st.session_state.page = selection

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**RAM**: {health.get('ram_gb', '?'):.1f} GB" if health.get("ram_gb") else "")
    st.sidebar.markdown(f"**Model**: {'Loaded' if health.get('model_loaded') else 'Not Loaded'}" if health.get("model_loaded") is not None else "")
    st.sidebar.markdown("---")
    st.sidebar.markdown("Africa Deep Tech Challenge 2026")

    pages[selection]()


if __name__ == "__main__":
    main()
