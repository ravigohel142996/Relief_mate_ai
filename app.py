import streamlit as st
import pandas as pd
import datetime
import random
import google.generativeai as genai
from datetime import date, timedelta
import numpy as np
import os

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="ReliefMate - Disaster Relief Management Platform",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------
# Professional Dashboard Styling
# ----------------------------
def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Premium Light Gradient Background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 50%, #f1f5f9 100%) !important;
        position: relative;
    }
    
    [data-testid="stApp"] {
        background: transparent !important;
    }
    
    /* Header Section - Premium White Card */
    .hero-container {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 32px 40px;
        text-align: left;
        margin: 20px auto 32px auto;
        max-width: 1400px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06);
        position: relative;
        z-index: 1;
        transition: all 0.2s ease;
    }
    
    .hero-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06);
    }
    
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 8px;
        color: #0f172a;
        letter-spacing: 0.02em;
    }
    
    .hero-subtitle {
        font-size: 1rem;
        margin-bottom: 16px;
        color: #334155;
        font-weight: 400;
    }
    
    .status-text {
        display: inline-block;
        color: #64748b;
        padding: 6px 16px;
        border-radius: 6px;
        font-size: 0.875rem;
        font-weight: 500;
        background: #f8fafc;
        border: 1px solid #e5e7eb;
    }
    
    .emergency-info {
        margin-top: 16px;
        padding: 12px 16px;
        background: #f8fafc;
        border-radius: 8px;
        border-left: 3px solid #2563eb;
        color: #334155;
        font-size: 0.875rem;
    }
    
    /* Premium White Cards */
    .glass-card {
        background: #ffffff !important;
        border-radius: 14px !important;
        border: 1px solid #e5e7eb !important;
        padding: 24px !important;
        margin: 20px 0 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06) !important;
        color: #334155 !important;
        position: relative !important;
        z-index: 1 !important;
        transition: all 0.2s ease !important;
    }
    
    .glass-card:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06) !important;
    }
    
    /* Chat Interface - Clean Premium Style */
    .chat-container {
        background: #ffffff !important;
        border-radius: 14px !important;
        padding: 24px !important;
        border: 1px solid #e5e7eb !important;
        margin: 24px 0 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06) !important;
    }
    
    .chat-message {
        background: #f8fafc;
        padding: 16px 20px;
        border-radius: 8px;
        margin: 12px 0;
        border-left: 3px solid #2563eb;
    }
    
    .chat-message strong {
        color: #2563eb;
        font-weight: 600;
    }
    
    /* Clean Premium Buttons */
    .stButton > button {
        background: #2563eb !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08) !important;
    }
    
    .stButton > button:hover {
        background: #1d4ed8 !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stButton > button:active {
        transform: scale(0.98) !important;
    }
    
    /* Text Input - Clean and Professional */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        color: #334155 !important;
        padding: 12px 16px !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
        background: #ffffff !important;
        outline: none !important;
    }
    
    .stSelectbox > div > div {
        background: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        color: #334155 !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #2563eb !important;
    }
    
    /* Metrics - Premium Stats Cards */
    .metric-container {
        background: #ffffff;
        border-radius: 14px;
        padding: 24px 20px;
        text-align: center;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06);
        transition: all 0.2s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06);
    }
    
    .metric-value {
        font-size: 2.25rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 6px;
        letter-spacing: 0.02em;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #64748b;
        font-weight: 600;
    }
    
    /* Tab Styling - Clean Pill-Style Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
        border-bottom: none;
        padding-bottom: 0;
        margin-bottom: 32px;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #ffffff !important;
        border-radius: 10px;
        color: #64748b !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        border: 1px solid #e5e7eb !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #f8fafc !important;
        border-color: #cbd5e1 !important;
        color: #334155 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: #ffffff !important;
        color: #2563eb !important;
        border: 1px solid #2563eb !important;
        border-bottom: 3px solid #2563eb !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {display: none;}
    footer {display: none;}
    
    /* Improved spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1400px;
        position: relative;
        z-index: 1;
    }
    
    h1, h2, h3 {
        color: #0f172a;
        font-weight: 700;
        letter-spacing: 0.02em;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
    }
    
    h2 {
        margin-bottom: 16px;
        margin-top: 32px;
        font-size: 1.6rem;
        font-weight: 700;
        color: #0f172a;
    }
    
    h3 {
        font-size: 1.2rem;
        margin-top: 24px;
        font-weight: 700;
        color: #0f172a;
    }
    
    p, label {
        color: #334155;
        line-height: 1.6;
        margin-bottom: 0.8rem;
    }
    
    /* Status badges - Clean, professional */
    .status-critical {
        background: #fef2f2;
        color: #dc2626;
        padding: 6px 14px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid #fecaca;
    }
    
    .status-active {
        background: #fffbeb;
        color: #d97706;
        padding: 6px 14px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid #fde68a;
    }
    
    .status-resolved {
        background: #f0fdf4;
        color: #16a34a;
        padding: 6px 14px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid #bbf7d0;
    }
    
    .status-monitoring {
        background: #eff6ff;
        color: #2563eb;
        padding: 6px 14px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid #bfdbfe;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 1.8rem;
        }
        .hero-subtitle {
            font-size: 0.9rem;
        }
    }
    
    /* Streamlit Native Components */
    .stMetric {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06);
        transition: all 0.2s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06);
    }
    
    .stMetric label {
        color: #64748b !important;
        font-weight: 600;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #0f172a !important;
        font-weight: 800;
        font-size: 2.25rem !important;
    }
    
    /* File Uploader */
    .stFileUploader {
        background: #ffffff;
        border: 2px dashed #d1d5db;
        border-radius: 14px;
        padding: 28px;
        transition: all 0.2s ease;
    }
    
    .stFileUploader:hover {
        border-color: #2563eb;
        background: #f8fafc;
    }
    
    /* Data Frame */
    .stDataFrame {
        background: #ffffff;
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    }
    
    /* Header overrides */
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    [data-testid="stToolbar"] {
        right: 2rem;
    }
    
    /* Global Text Colors */
    body {
        color: #334155;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Gemini API Setup
# ----------------------------
def setup_gemini():
    """
    Setup Gemini API with graceful fallback handling.
    Returns: (model, status_text) where status is 'Operational' or 'Limited Mode'
    """
    # Try to read API key from Streamlit secrets
    try:
        GEMINI_KEY = st.secrets["general"]["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        GEMINI_KEY = None
    
    # Attempt to initialize Gemini API with stable model
    if GEMINI_KEY and GEMINI_KEY != "your_actual_gemini_api_key_here":
        try:
            genai.configure(api_key=GEMINI_KEY)
            model = genai.GenerativeModel("gemini-pro")
            # Test the model with a simple call to verify it works
            _ = model.generate_content("test")
            return model, "Operational"
        except Exception as e:
            # Log error for debugging but don't show to user
            print(f"Gemini API initialization failed: {e}")
            return None, "Limited Mode"
    else:
        # No API key configured - run in demo mode
        return None, "Limited Mode"

# ----------------------------
# Sample Data Generation
# ----------------------------
def generate_sample_data():
    # Relief Reports
    reports = [
        {"location": "Rajkot", "type": "Flood", "status": "Critical", "needs": "Food, Water, Medical Supplies", "team": "Team A"},
        {"location": "Ahmedabad", "type": "Earthquake", "status": "Resolved", "needs": "Search & Rescue Complete", "team": "Team B"},
        {"location": "Surat", "type": "Cyclone", "status": "Active", "needs": "Evacuation, Shelter", "team": "Team C"},
        {"location": "Bhavnagar", "type": "Fire", "status": "Critical", "needs": "Fire Brigade, Medical Aid", "team": "Team D"},
        {"location": "Vadodara", "type": "Landslide", "status": "Monitoring", "needs": "Geological Survey", "team": "Team E"}
    ]
    
    # Analytics Data
    dates = [date.today() - timedelta(days=i) for i in range(7, 0, -1)]
    analytics = {
        "dates": dates,
        "requests": [random.randint(50, 200) for _ in range(7)],
        "resolved": [random.randint(20, 150) for _ in range(7)],
        "active": [random.randint(10, 80) for _ in range(7)]
    }
    
    return reports, analytics

# ----------------------------
# Hero Section - Professional Header
# ----------------------------
def render_hero():
    st.markdown("""
    <div class="glass-card" style="margin-top: 24px;">
        <h1 style="font-size:2.2rem; margin-bottom:8px; font-weight: 700; letter-spacing: 0.02em; color: #0f172a;">ReliefMate</h1>
        <p style="color:#334155; font-size:1rem; margin-bottom:16px;">
            Disaster Relief Management Platform
        </p>
        <div style="margin-top:16px; display:flex; gap:12px; flex-wrap:wrap; align-items:center;">
            <span class="status-text">System Status: Operational</span>
            <span class="status-text">
                Emergency Numbers: 112 | 108 | 101
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------
# University Header Section
# ----------------------------
def render_university_header():
    st.markdown("""
    <div style="
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 20px 28px;
        text-align: center;
        margin: 20px auto;
        max-width: 900px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06);
    ">
        <p style="color: #0f172a; font-size: 1.1rem; font-weight: 700; margin: 0 0 6px 0; letter-spacing: 0.02em;">
            Marwadi University
        </p>
        <p style="color: #64748b; font-size: 0.95rem; margin: 0; font-weight: 500;">
            Department of Computer Science & Engineering (AI & ML)
        </p>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------
# Chat Interface - Decision Support
# ----------------------------
def render_chat_interface(model, api_status):
    st.markdown("## Guidance")
    st.markdown('<p style="color: #64748b; margin-bottom: 24px; text-align: center;">Get instant guidance on emergency procedures, resource allocation, and disaster response protocols</p>', unsafe_allow_html=True)
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # System status indicator
    st.markdown("""
    <div style="text-align: center; margin-bottom: 24px;">
        <span class="status-text">
            System Ready
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat input container
    st.markdown("""
    <div style="
        max-width: 1000px; 
        margin: 0 auto 24px auto; 
        background: #ffffff; 
        border-radius: 14px; 
        padding: 28px; 
        border: 1px solid #e5e7eb; 
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06);
    ">
        <p style="
            text-align: center; 
            color: #334155; 
            font-size: 1rem; 
            font-weight: 500; 
            margin: 0 0 16px 0;
        ">
            Enter your question below
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat input
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Ask your question:",
            placeholder="Ask about floods, earthquakes, safe zones, shelters, live updates…",
            key="chat_input",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send", use_container_width=True)
    
    st.markdown('<div style="margin-bottom: 24px;"></div>', unsafe_allow_html=True)
    
    # Process message
    if send_button and user_input.strip():
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Generate AI response
        if model:
            with st.spinner("Processing your request..."):
                try:
                    enhanced_prompt = f"""
                    You are ReliefMate, a disaster relief assistant for Gujarat, India.
                    Provide helpful, actionable advice in 100-150 words.
                    Include relevant emergency contacts when appropriate.
                    Be empathetic, clear, and focus on immediate safety.
                    
                    User Question: {user_input}
                    """
                    response = model.generate_content(enhanced_prompt)
                    ai_response = response.text.strip()
                except Exception as e:
                    # Log error for debugging
                    print(f"Gemini API error: {e}")
                    # Provide clean fallback response to user
                    ai_response = "**Emergency Guidance**: For immediate assistance, contact emergency services: 112 (Police), 108 (Medical), 101 (Fire). Our automated guidance system is temporarily processing your request. Please try again or refer to the emergency protocols below."
        else:
            # Demo responses for when API is not available
            demo_responses = [
                "**Emergency Protocol**: For immediate danger, call 112 (Police), 108 (Ambulance), or 101 (Fire). Stay calm, move to safety, and follow official evacuation routes. Keep emergency kit ready with water, food, medicine, and important documents.",
                "**Flood Safety**: Move to higher ground immediately. Never walk or drive through flood water. Stay informed via official radio/TV channels. If trapped, signal for help from highest available point. Emergency services: 108 for rescue operations.",
                "**Fire Emergency**: GET OUT, STAY OUT, CALL 101. Crawl low under smoke. Close doors behind you. Meet at designated family meeting spot. Don't use elevators. If clothes catch fire: Stop, Drop, Roll.",
                "**Medical Emergency**: Call 108 immediately. Check for breathing and pulse. Apply pressure to bleeding wounds. Keep victim warm and conscious. Don't move someone with potential spinal injury unless in immediate danger.",
                "**Emergency Kit**: Include water (1 gallon per person per day), non-perishable food, flashlight, radio, first aid kit, medications, documents, cash, and phone chargers. Update kit every 6 months."
            ]
            ai_response = random.choice(demo_responses)
        
        # Add AI response to history
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown('<div style="max-width: 1000px; margin: 24px auto;">', unsafe_allow_html=True)
        st.markdown("### Conversation History")
        for message in reversed(st.session_state.chat_history[-10:]):  # Show last 10 messages
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message" style="border-left: 3px solid #dc2626; background: #fef2f2;">
                    <strong style="color: #dc2626;">You:</strong><br>
                    <span style="color: #334155;">{message["content"]}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message" style="border-left: 3px solid #2563eb; background: #eff6ff;">
                    <strong style="color: #2563eb;">ReliefMate:</strong><br>
                    <span style="color: #334155;">{message["content"]}</span>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 60px 40px; background: #ffffff; border-radius: 14px; margin: 24px auto; max-width: 700px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06); border: 1px solid #e5e7eb;">
            <h3 style="color: #0f172a; margin-bottom: 12px; font-weight: 700; letter-spacing: 0.02em;">Assistance Ready</h3>
            <p style="color: #64748b;">Ask about emergency procedures, disaster preparedness, or resource management</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# Relief Reports Dashboard
# ----------------------------
def render_reports_dashboard(reports):
    st.markdown("## Live Reports")
    st.markdown('<p style="color: #64748b; margin-bottom: 24px; text-align: center;">Real-time monitoring of active disaster response operations</p>', unsafe_allow_html=True)
    
    # Status summary
    col1, col2, col3, col4 = st.columns(4)
    
    critical_count = len([r for r in reports if "Critical" in r["status"]])
    active_count = len([r for r in reports if "Active" in r["status"]])
    resolved_count = len([r for r in reports if "Resolved" in r["status"]])
    monitoring_count = len([r for r in reports if "Monitoring" in r["status"]])
    
    with col1:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value">{}</div>
            <div class="metric-label">Critical Cases</div>
        </div>
        """.format(critical_count), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value">{}</div>
            <div class="metric-label">Active Operations</div>
        </div>
        """.format(active_count), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value">{}</div>
            <div class="metric-label">Resolved Cases</div>
        </div>
        """.format(resolved_count), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value">{}</div>
            <div class="metric-label">Under Monitoring</div>
        </div>
        """.format(monitoring_count), unsafe_allow_html=True)
    
    # Live Incident Map
    st.markdown("### Live Incident Map (Demo)")
    st.markdown('<p style="color: #64748b; margin-bottom: 20px; text-align: center;">Demo – Live integration ready with real-time GPS tracking</p>', unsafe_allow_html=True)
    
    # Demo coordinates for Gujarat cities
    map_data = pd.DataFrame({
        'lat': [22.3039, 23.0225, 21.1702, 21.7645],
        'lon': [70.8022, 72.5714, 72.8311, 72.1519]
    })
    
    st.markdown('<div style="background: #ffffff; padding: 24px; border-radius: 14px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06); margin-bottom: 24px; border: 1px solid #e5e7eb;">', unsafe_allow_html=True)
    st.map(map_data, zoom=6)
    st.markdown('<p style="color: #64748b; font-size: 0.85rem; text-align: center; margin-top: 12px;">Showing: Rajkot • Ahmedabad • Surat • Bhavnagar</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Detailed reports
    st.markdown("### Operations Report")
    st.markdown("")  # spacing
    
    for i, report in enumerate(reports):
        # Determine status styling
        if "Critical" in report["status"]:
            status_class = "status-critical"
        elif "Active" in report["status"]:
            status_class = "status-active"
        elif "Resolved" in report["status"]:
            status_class = "status-resolved"
        else:  # Monitoring
            status_class = "status-monitoring"
        
        st.markdown(f"""
        <div class="glass-card" style="margin-bottom: 24px !important; padding: 28px !important;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 12px;">
                <h2 style="color: #0f172a; margin: 0; font-size: 1.6rem; font-weight: 700; letter-spacing: 0.02em;">
                    {report["location"]}
                </h2>
                <span class="{status_class}" style="font-size: 0.9rem; padding: 6px 14px;">
                    {report["status"]}
                </span>
            </div>
            <div style="background: #f8fafc; padding: 18px; border-radius: 8px; margin-bottom: 12px; border-left: 3px solid #2563eb;">
                <p style="margin: 0 0 8px 0; font-size: 0.95rem;"><strong style="color: #334155; font-weight: 600;">Disaster Type:</strong> <span style="color: #334155;">{report["type"]}</span></p>
                <p style="margin: 0; font-size: 0.95rem;"><strong style="color: #334155; font-weight: 600;">Requirements:</strong> <span style="color: #334155;">{report["needs"]}</span></p>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; color: #64748b; font-size: 0.85rem;">
                <p style="margin: 0;"><strong style="color: #64748b;">Response Team:</strong> <span style="color: #334155; font-weight: 600;">{report["team"]}</span></p>
                <p style="margin: 0; color: #64748b; font-style: italic;">Last Updated: {datetime.datetime.now().strftime('%H:%M')} IST</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# Analytics Dashboard
# ----------------------------
def render_analytics(analytics_data):
    st.markdown("## Insights")
    st.markdown('<p style="color: #64748b; margin-bottom: 20px; text-align: center; font-size: 0.95rem;">Operational trends from the last 7 days</p>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Map Integration Placeholder
    st.markdown("### Live Map (Future Integration)")
    st.markdown("""
    <div style="
        background: #ffffff;
        padding: 48px 32px;
        border-radius: 14px;
        text-align: center;
        border: 2px dashed #d1d5db;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06);
        margin-bottom: 32px;
    ">
        <h3 style="color: #0f172a; margin-bottom: 12px; font-weight: 700; letter-spacing: 0.02em;">Live Map Integration</h3>
        <p style="color: #64748b; font-size: 0.95rem; margin: 0;">
            Google Maps / ISRO Bhuvan / NDMA Integration – Planned
        </p>
        <p style="color: #64748b; font-size: 0.85rem; margin-top: 10px;">
            Real-time GPS tracking, disaster zones, and safe routes visualization
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Safe Zones and Shelters
    st.markdown("### Nearby Safe Zones")
    st.markdown('<div style="background: #ffffff; padding: 24px; border-radius: 14px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06); margin-bottom: 24px; border: 1px solid #e5e7eb;">', unsafe_allow_html=True)
    
    safe_places = [
        {"name": "Govt. School - Sector 12", "distance": "1.2 km", "type": "Shelter"},
        {"name": "City Hospital - Main Road", "distance": "2.3 km", "type": "Medical"},
        {"name": "Sports Stadium - Civil Lines", "distance": "3.5 km", "type": "Shelter"},
        {"name": "Municipal Building - Center", "distance": "1.8 km", "type": "Admin"}
    ]
    
    cols = st.columns(4)
    for idx, place in enumerate(safe_places):
        with cols[idx]:
            st.markdown(f"""
            <div style="text-align: center; padding: 16px; background: #f8fafc; border-radius: 8px; border: 1px solid #e5e7eb;">
                <p style="color: #334155; font-weight: 600; font-size: 0.9rem; margin: 0 0 6px 0;">{place['name']}</p>
                <p style="color: #2563eb; font-size: 0.85rem; margin: 0 0 6px 0;">{place['distance']}</p>
                <span style="background: #eff6ff; color: #2563eb; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; border: 1px solid #bfdbfe;">{place['type']}</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Operational Parameters
    st.markdown("### Operational Parameters")
    st.markdown('<p style="color: #64748b; margin-bottom: 20px; text-align: center;">Key disaster response metrics and indicators</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Generate demo values
    earthquake_mag = round(random.uniform(3.5, 6.2), 1)
    safe_zones = ["Govt School - Sector 12", "Community Hall", "Sports Stadium", "Municipal Building"]
    safe_zone = random.choice(safe_zones)
    distance = round(random.uniform(0.8, 3.5), 1)
    eta = random.randint(5, 15)
    
    with col1:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; min-height: 160px;">
            <div class="metric-value" style="font-size: 1.8rem; color: #dc2626;">{earthquake_mag}</div>
            <div class="metric-label" style="font-size: 0.8rem;">Earthquake Magnitude</div>
            <p style="color: #64748b; font-size: 0.75rem; margin: 8px 0 0 0;">(Richter Scale)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; min-height: 160px;">
            <div style="font-size: 0.9rem; color: #2563eb; font-weight: 600; margin: 12px 0;">{safe_zone}</div>
            <div class="metric-label" style="font-size: 0.8rem;">Nearest Safe Zone</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; min-height: 160px;">
            <div class="metric-value" style="font-size: 1.8rem; color: #d97706;">{distance} km</div>
            <div class="metric-label" style="font-size: 0.8rem;">Distance to Safety</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; min-height: 160px;">
            <div class="metric-value" style="font-size: 1.8rem; color: #16a34a;">{eta} min</div>
            <div class="metric-label" style="font-size: 0.8rem;">Response ETA</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Date': analytics_data['dates'],
        'New Requests': analytics_data['requests'],
        'Resolved Cases': analytics_data['resolved'],
        'Active Cases': analytics_data['active']
    })
    
    # Charts
    st.markdown("### 7-Day Operational Trends")
    st.markdown('<p style="color: #64748b; margin-bottom: 16px; text-align: center; font-size: 0.9rem;">Track relief operations performance over the past week</p>', unsafe_allow_html=True)
    st.markdown('<div style="background: #ffffff; padding: 24px; border-radius: 14px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06); margin-bottom: 28px; border: 1px solid #e5e7eb;">', unsafe_allow_html=True)
    
    # Line chart
    chart_data = df.set_index('Date')[['New Requests', 'Resolved Cases', 'Active Cases']]
    st.line_chart(chart_data, use_container_width=True, height=400)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Bar chart
    st.markdown("### Daily Performance Comparison")
    st.markdown('<p style="color: #64748b; margin-bottom: 16px; text-align: center; font-size: 0.9rem;">Side-by-side comparison of daily operations metrics</p>', unsafe_allow_html=True)
    st.markdown('<div style="background: #ffffff; padding: 24px; border-radius: 14px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06); margin-bottom: 28px; border: 1px solid #e5e7eb;">', unsafe_allow_html=True)
    st.bar_chart(chart_data, use_container_width=True, height=400)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Summary statistics
    st.markdown("### Key Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_requests = sum(analytics_data['requests']) // 7
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <div class="metric-value">{avg_requests}</div>
            <div class="metric-label">Avg Daily Requests</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_resolved = sum(analytics_data['resolved'])
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <div class="metric-value">{total_resolved}</div>
            <div class="metric-label">Total Resolved</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        resolution_rate = round((total_resolved / sum(analytics_data['requests'])) * 100, 1)
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <div class="metric-value">{resolution_rate}%</div>
            <div class="metric-label">Resolution Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional metrics using Streamlit metrics
    st.markdown("### Key Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Critical Cases",
            value="23",
            delta="-5",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            label="Avg Response Time",
            value="2.3 min",
            delta="-0.8 min",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="Active Teams",
            value="12",
            delta="+2"
        )
    
    with col4:
        st.metric(
            label="Coverage Areas",
            value="45",
            delta="+3"
        )

# ----------------------------
# Admin Panel
# ----------------------------
def render_admin_panel():
    st.markdown("## Administration")
    st.markdown('<p style="color: #64748b; margin-bottom: 24px; text-align: center;">Manage relief operations and system configuration</p>', unsafe_allow_html=True)
    
    # Live Tracking Status
    st.markdown("### Live Tracking Status")
    st.markdown('<p style="color: #64748b; margin-bottom: 20px; text-align: center;">Real-time monitoring of field operations and resource deployment</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    # Generate demo values
    teams_online = random.randint(5, 15)
    vehicles_deployed = random.randint(3, 10)
    
    with col1:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <p style="margin: 8px 0; font-weight: 600; font-size: 1.2rem; color: #16a34a;">Active</p>
            <p style="margin: 0; font-size: 0.85rem; color: #64748b;">GPS Tracking</p>
            <div style="margin-top: 12px;">
                <span class="status-text">Online</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <div class="metric-value" style="font-size: 2rem; color: #2563eb;">{teams_online}</div>
            <p style="margin: 0; font-size: 0.85rem; color: #64748b;">Teams Online</p>
            <div style="margin-top: 12px;">
                <span class="status-text">Live</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <div class="metric-value" style="font-size: 2rem; color: #d97706;">{vehicles_deployed}</div>
            <p style="margin: 0; font-size: 0.85rem; color: #64748b;">Vehicles Deployed</p>
            <div style="margin-top: 12px;">
                <span class="status-text">Active</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3 style="margin-bottom: 20px; color: #0f172a; font-weight: 600;">
                Submit New Report
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        location = st.selectbox("Location", ["Rajkot", "Ahmedabad", "Surat", "Bhavnagar", "Vadodara", "Other"])
        disaster_type = st.selectbox("Disaster Type", ["Flood", "Fire", "Earthquake", "Cyclone", "Landslide", "Other"])
        severity = st.selectbox("Severity Level", ["Critical", "Active", "Monitoring"])
        description = st.text_area("Description", placeholder="Describe the situation and required assistance...", height=120)
        
        if st.button("Submit Report", use_container_width=True):
            st.success(f"Report submitted successfully! Location: {location}, Type: {disaster_type}, Severity: {severity}")
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3 style="margin-bottom: 20px; color: #0f172a; font-weight: 600;">
                Bulk Data Upload
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #f8fafc; border: 2px dashed #d1d5db; border-radius: 14px; padding: 32px; text-align: center; margin-bottom: 20px;">
            <p style="color: #64748b; margin: 0; font-weight: 500;">Drop CSV file or click to browse</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Upload CSV file with relief data",
            type=["csv"],
            help="Upload CSV files containing relief operation data",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f"File uploaded successfully! {len(df)} records found.")
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
    
    # System Status Section
    st.markdown("### System Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <p style="margin: 0; font-weight: 600; color: #16a34a;">Operational</p>
            <p style="margin: 0; font-size: 0.85rem; color: #64748b;">System Status</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <p style="margin: 0; font-weight: 600; color: #16a34a;">Connected</p>
            <p style="margin: 0; font-size: 0.85rem; color: #64748b;">API Status</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <p style="margin: 0; font-weight: 600; color: #16a34a;">Online</p>
            <p style="margin: 0; font-size: 0.85rem; color: #64748b;">Database</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <p style="margin: 0; font-weight: 600; color: #2563eb;">&lt;2s</p>
            <p style="margin: 0; font-size: 0.85rem; color: #64748b;">Response Time</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# Main Application
# ----------------------------
def main():
    # Inject custom CSS
    inject_custom_css()
    
    # Setup Gemini
    model, api_status = setup_gemini()
    
    # Generate sample data
    reports, analytics_data = generate_sample_data()
    
    # Hero Section
    render_hero()
    
    # University Header
    render_university_header()
    
    # Status indicator
    st.markdown(f"""
    <div style="text-align: center; margin: 24px 0 32px 0;">
        <span style="background: #ffffff; padding: 8px 20px; border-radius: 8px; border: 1px solid #e5e7eb; color: #64748b; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08); font-size: 0.9rem;">
            API Status: {api_status}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Navigation Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Guidance", "Live Reports", "Insights", "Administration"])
    
    with tab1:
        render_chat_interface(model, api_status)
    
    with tab2:
        render_reports_dashboard(reports)
    
    with tab3:
        render_analytics(analytics_data)
    
    with tab4:
        render_admin_panel()
    
    # Footer - Professional and Clean
    st.html("""
    <div style="margin-top: 60px; padding: 36px 24px; text-align: center; background: #ffffff; border-radius: 14px; border: 1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06);">
        <p style="color: #0f172a; font-size: 1.1rem; font-weight: 700; letter-spacing: 0.02em; margin-bottom: 6px;">Marwadi University</p>
        <p style="color: #334155; font-size: 0.95rem; margin-bottom: 4px;">Department of Computer Science & Engineering (AI & ML)</p>
        <p style="color: #334155; font-size: 0.9rem; margin-bottom: 3px;">Student: Ravi Gohel N. (2nd Year)</p>
        <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 24px;">Email: <a href="mailto:ravi.n.gohel811@gmail.com" style="color: #2563eb; text-decoration: none;">ravi.n.gohel811@gmail.com</a></p>
        
        <div style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 16px; margin: 20px auto; max-width: 500px;">
            <p style="color: #dc2626; font-weight: 600; font-size: 1rem; margin-bottom: 6px;">Emergency Numbers</p>
            <p style="color: #dc2626; font-size: 1.05rem; font-weight: 600; margin: 0;">112 | 108 | 101</p>
        </div>
        
        <p style="color: #64748b; font-size: 0.85rem; margin-top: 24px; margin-bottom: 3px;">© 2025 ReliefMate</p>
        <p style="color: #64748b; font-size: 0.8rem; margin: 0;">Disaster Relief Management Platform</p>
    </div>
    """)

if __name__ == "__main__":
    main()
