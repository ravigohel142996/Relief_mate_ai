import streamlit as st
import pandas as pd
import datetime
import random
import google.generativeai as genai
from datetime import date, timedelta
import numpy as np
import os

# ----------------------------
# 🎨 Page Config
# ----------------------------
st.set_page_config(
    page_title="ReliefMate AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------
# 🎨 FUTURISTIC PREMIUM UI - GLASSMORPHISM + 3D DEPTH
# ----------------------------
def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles - Deep Gradient Background */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* 🔥 CLOUD-SAFE FULL PAGE DARK GRADIENT - Using data-testid selectors */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f172a 0%, #020617 25%, #0f172a 50%, #1e293b 75%, #0f172a 100%) !important;
        position: relative;
    }
    
    [data-testid="stApp"] {
        background: transparent !important;
    }
    
    /* Animated Background Overlay with Radial Gradients */
    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle at 20% 50%, rgba(6, 182, 212, 0.08) 0%, transparent 50%),
                    radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.08) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Header Section - Premium Glass Command Center */
    .hero-container {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(24px) saturate(180%);
        -webkit-backdrop-filter: blur(24px) saturate(180%);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 20px;
        padding: 48px 40px 40px 40px;
        text-align: left;
        margin: 20px auto 48px auto;
        max-width: 1400px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37), 
                    0 1px 2px rgba(6, 182, 212, 0.1),
                    inset 0 1px 0 rgba(255, 255, 255, 0.05);
        position: relative;
        z-index: 1;
    }
    
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 12px;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 16px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3), 0 0 20px rgba(6, 182, 212, 0.3);
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        margin-bottom: 20px;
        color: #94a3b8;
        font-weight: 400;
        letter-spacing: 0.01em;
    }
    
    .status-badge {
        display: inline-block;
        background: rgba(16, 185, 129, 0.15);
        color: #10b981;
        padding: 8px 20px;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        border: 1px solid rgba(16, 185, 129, 0.3);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        animation: pulse-glow 3s ease-in-out infinite;
    }
    
    @keyframes pulse-glow {
        0%, 100% { 
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25),
                        inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        50% { 
            box-shadow: 0 4px 16px rgba(16, 185, 129, 0.35),
                        inset 0 1px 0 rgba(255, 255, 255, 0.15);
        }
    }
    
    .emergency-info {
        margin-top: 20px;
        padding: 16px 20px;
        background: rgba(15, 23, 42, 0.5);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 12px;
        border-left: 3px solid #fbbf24;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    }
    
    /* Glassmorphism Cards with 3D Depth */
    .glass-card {
        background: rgba(30, 41, 59, 0.5) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(148, 163, 184, 0.18) !important;
        padding: 28px !important;
        margin: 24px 0 !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37),
                    0 1px 2px rgba(6, 182, 212, 0.1),
                    inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
        color: #e2e8f0 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        z-index: 1 !important;
    }
    
    .glass-card:hover {
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.45),
                    0 2px 4px rgba(6, 182, 212, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
        transform: translateY(-4px) !important;
        border-color: rgba(6, 182, 212, 0.3) !important;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(6, 182, 212, 0.5), transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .glass-card:hover::before {
        opacity: 1;
    }
    
    /* Chat Interface - Command Console Style */
    .chat-container {
        background: rgba(30, 41, 59, 0.5) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border-radius: 16px !important;
        padding: 28px !important;
        border: 1px solid rgba(148, 163, 184, 0.18) !important;
        margin: 28px 0 !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37),
                    0 1px 2px rgba(6, 182, 212, 0.1),
                    inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
    }
    
    .chat-message {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 16px 20px;
        border-radius: 12px;
        margin: 12px 0;
        border-left: 3px solid #06b6d4;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        transition: all 0.2s ease;
    }
    
    .chat-message:hover {
        background: rgba(15, 23, 42, 0.75);
        transform: translateX(4px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
    }
    
    .chat-message strong {
        color: #06b6d4;
        font-weight: 600;
    }
    
    /* Futuristic Buttons with Subtle Glow */
    .stButton > button {
        background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%) !important;
        color: white !important;
        border: 1px solid rgba(6, 182, 212, 0.4) !important;
        border-radius: 12px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 16px rgba(6, 182, 212, 0.25),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.15);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%) !important;
        box-shadow: 0 6px 24px rgba(6, 182, 212, 0.35),
                    inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
        transform: translateY(-2px) !important;
        border-color: rgba(6, 182, 212, 0.6) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0px) scale(0.98) !important;
    }
    
    /* Text Input - Tactile Console Feel */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(100, 116, 139, 0.3) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        padding: 14px 16px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) inset !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #06b6d4 !important;
        box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.2),
                    0 4px 16px rgba(0, 0, 0, 0.3) inset !important;
        background: rgba(15, 23, 42, 0.9) !important;
    }
    
    .stSelectbox > div > div {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(100, 116, 139, 0.3) !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: rgba(6, 182, 212, 0.5) !important;
    }
    
    /* Metrics - Command Center Stats */
    .metric-container {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-radius: 16px;
        padding: 28px 24px;
        text-align: center;
        border: 1px solid rgba(148, 163, 184, 0.18);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37),
                    0 1px 2px rgba(6, 182, 212, 0.1),
                    inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-container::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #06b6d4, transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .metric-container:hover {
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.45),
                    0 2px 4px rgba(6, 182, 212, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.08);
        transform: translateY(-4px);
        border-color: rgba(6, 182, 212, 0.3);
    }
    
    .metric-container:hover::after {
        opacity: 1;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 8px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3), 0 0 15px rgba(6, 182, 212, 0.3);
        letter-spacing: -0.02em;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #94a3b8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Tab Styling - Floating Glass Pills */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: transparent;
        border-bottom: none;
        padding-bottom: 0;
        margin-bottom: 40px;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px) saturate(150%);
        -webkit-backdrop-filter: blur(12px) saturate(150%);
        border-radius: 24px;
        color: #94a3b8;
        padding: 12px 28px;
        font-weight: 600;
        border: 1px solid rgba(148, 163, 184, 0.15);
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(30, 41, 59, 0.6);
        border-color: rgba(6, 182, 212, 0.25);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.25) 0%, rgba(8, 145, 178, 0.2) 100%) !important;
        color: #06b6d4 !important;
        border: 1px solid rgba(6, 182, 212, 0.4) !important;
        box-shadow: 0 4px 24px rgba(6, 182, 212, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        transform: translateY(-2px) scale(1.05) !important;
        text-shadow: 0 0 15px rgba(6, 182, 212, 0.4);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {display: none;}
    footer {display: none;}

    
    /* Improved spacing - Max Width Container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
        position: relative;
        z-index: 1;
    }
    
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    h2 {
        margin-bottom: 12px;
        font-size: 1.8rem;
    }
    
    h3 {
        font-size: 1.3rem;
    }
    
    p, label {
        color: #94a3b8;
        line-height: 1.6;
    }
    
    /* Status badges with Subtle Glow */
    .status-critical {
        background: rgba(220, 38, 38, 0.15);
        color: #ef4444;
        padding: 6px 14px;
        border-radius: 16px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid rgba(220, 38, 38, 0.3);
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.25),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        animation: pulse-critical 3s ease-in-out infinite;
    }
    
    @keyframes pulse-critical {
        0%, 100% { 
            box-shadow: 0 4px 12px rgba(220, 38, 38, 0.25),
                        inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        50% { 
            box-shadow: 0 4px 16px rgba(220, 38, 38, 0.35),
                        inset 0 1px 0 rgba(255, 255, 255, 0.15);
        }
    }
    
    .status-active {
        background: rgba(217, 119, 6, 0.15);
        color: #f59e0b;
        padding: 6px 14px;
        border-radius: 16px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid rgba(217, 119, 6, 0.3);
        box-shadow: 0 4px 12px rgba(217, 119, 6, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .status-resolved {
        background: rgba(16, 185, 129, 0.15);
        color: #10b981;
        padding: 6px 14px;
        border-radius: 16px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid rgba(16, 185, 129, 0.3);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .status-monitoring {
        background: rgba(37, 99, 235, 0.15);
        color: #3b82f6;
        padding: 6px 14px;
        border-radius: 16px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid rgba(37, 99, 235, 0.3);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        .hero-subtitle {
            font-size: 1rem;
        }
    }
    
    /* Streamlit Native Components Styling */
    .stMetric {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37);
    }
    
    .stMetric label {
        color: #94a3b8 !important;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 800;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3), 0 0 15px rgba(6, 182, 212, 0.2);
    }
    
    /* File Uploader */
    .stFileUploader {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border: 2px dashed rgba(100, 116, 139, 0.3);
        border-radius: 16px;
        padding: 32px;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: rgba(6, 182, 212, 0.4);
        background: rgba(30, 41, 59, 0.65);
    }
    
    /* Data Frame */
.stDataFrame {
    background: rgba(30, 41, 59, 0.5);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(148, 163, 184, 0.18);
}

/* 🔥 STREAMLIT CLOUD OVERRIDES - Ensure Dark Theme Everywhere */
[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stToolbar"] {
    right: 2rem;
}

/* Global Text Colors */
body {
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# 🔑 Gemini API Setup - FIXED VERSION
# ----------------------------
def setup_gemini():
    # Correct way to read from Streamlit secrets
    try:
        GEMINI_KEY = st.secrets["general"]["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        GEMINI_KEY = None
        st.warning("Gemini API key not found in secrets.toml")
    
    if GEMINI_KEY and GEMINI_KEY != "your_actual_gemini_api_key_here":
        try:
            genai.configure(api_key=GEMINI_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            return model, "✅ Gemini AI Connected"
        except Exception as e:
            return None, f"❌ API Error: {str(e)[:50]}..."
    else:
        return None, "⚠️ Demo Mode (Add real GEMINI_API_KEY to secrets)"

# ----------------------------
# 📊 Sample Data Generation
# ----------------------------
def generate_sample_data():
    # Relief Reports
    reports = [
        {"location": "Rajkot", "type": "Flood", "status": "🚨 Critical", "needs": "Food, Water, Medical Supplies", "team": "Team A"},
        {"location": "Ahmedabad", "type": "Earthquake", "status": "✅ Resolved", "needs": "Search & Rescue Complete", "team": "Team B"},
        {"location": "Surat", "type": "Cyclone", "status": "⚠️ Active", "needs": "Evacuation, Shelter", "team": "Team C"},
        {"location": "Bhavnagar", "type": "Fire", "status": "🔥 Critical", "needs": "Fire Brigade, Medical Aid", "team": "Team D"},
        {"location": "Vadodara", "type": "Landslide", "status": "📋 Monitoring", "needs": "Geological Survey", "team": "Team E"}
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
# 🏠 Hero Section - Futuristic Command Center
# ----------------------------
def render_hero():
    st.markdown("""
    <div class="hero-container">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <h1 class="hero-title">
                    <span style="font-size: 2rem;">🌍</span> ReliefMate AI
                </h1>
                <p class="hero-subtitle">Advanced Disaster Relief Management System</p>
                <span class="status-badge">● System Operational</span>
            </div>
        </div>
        <div class="emergency-info" style="margin-top: 20px;">
            <strong style="color: #fbbf24;">⚡ Emergency Hotlines:</strong>
            <span style="color: #cbd5e1; margin-left: 16px;">
                Police: 112  |  Medical: 108  |  Fire: 101
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------
# 💬 Enhanced Chat Interface - Command Console
# ----------------------------
def render_chat_interface(model, api_status):
    st.markdown("## 🤖 AI Assistant")
    st.markdown('<p style="color: #94a3b8; margin-bottom: 32px; text-align: center;">Get instant guidance on emergency procedures, resource allocation, and disaster response protocols</p>', unsafe_allow_html=True)
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # System Ready indicator with glow
    st.markdown("""
    <div style="text-align: center; margin-bottom: 32px;">
        <span style="background: rgba(16, 185, 129, 0.15); color: #10b981; padding: 8px 20px; border-radius: 20px; font-size: 0.875rem; font-weight: 600; border: 1px solid rgba(16, 185, 129, 0.3); box-shadow: 0 0 20px rgba(16, 185, 129, 0.3), 0 0 40px rgba(16, 185, 129, 0.1) inset; animation: pulse-glow 2s ease-in-out infinite;">
            ● System Online
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Centered chat input container with glass effect
    st.markdown('<div style="max-width: 900px; margin: 0 auto; background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(20px); border-radius: 16px; padding: 24px; border: 1px solid rgba(148, 163, 184, 0.2); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);">', unsafe_allow_html=True)
    
    # Chat input
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Ask your question:",
            placeholder="e.g., 'What should I do during a flood emergency?'",
            key="chat_input",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process message
    if send_button and user_input.strip():
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Generate AI response
        if model:
            with st.spinner("🤖 ReliefMate AI is analyzing..."):
                try:
                    enhanced_prompt = f"""
                    You are ReliefMate AI, a disaster relief assistant for Gujarat, India.
                    Provide helpful, actionable advice in 100-150 words.
                    Include relevant emergency contacts when appropriate.
                    Be empathetic, clear, and focus on immediate safety.
                    
                    User Question: {user_input}
                    """
                    response = model.generate_content(enhanced_prompt)
                    ai_response = response.text.strip()
                except Exception as e:
                    ai_response = f"❌ Service temporarily unavailable. For immediate help: 112 (Police), 108 (Medical), 101 (Fire). Error: {str(e)[:50]}..."
        else:
            # Demo responses for when API is not available
            demo_responses = [
                "🚨 **Emergency Protocol**: For immediate danger, call 112 (Police), 108 (Ambulance), or 101 (Fire). Stay calm, move to safety, and follow official evacuation routes. Keep emergency kit ready with water, food, medicine, and important documents.",
                "🌊 **Flood Safety**: Move to higher ground immediately. Never walk or drive through flood water. Stay informed via official radio/TV channels. If trapped, signal for help from highest available point. Emergency services: 108 for rescue operations.",
                "🔥 **Fire Emergency**: GET OUT, STAY OUT, CALL 101. Crawl low under smoke. Close doors behind you. Meet at designated family meeting spot. Don't use elevators. If clothes catch fire: Stop, Drop, Roll.",
                "🏥 **Medical Emergency**: Call 108 immediately. Check for breathing and pulse. Apply pressure to bleeding wounds. Keep victim warm and conscious. Don't move someone with potential spinal injury unless in immediate danger.",
                "📋 **Emergency Kit**: Include water (1 gallon per person per day), non-perishable food, flashlight, radio, first aid kit, medications, documents, cash, and phone chargers. Update kit every 6 months."
            ]
            ai_response = random.choice(demo_responses)
        
        # Add AI response to history
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown('<div style="max-width: 1000px; margin: 32px auto;">', unsafe_allow_html=True)
        st.markdown("### 📋 Mission Briefing")
        for message in reversed(st.session_state.chat_history[-10:]):  # Show last 10 messages
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message" style="border-left: 3px solid #ef4444; background: rgba(220, 38, 38, 0.1);">
                    <strong style="color: #ef4444;">You:</strong><br>
                    <span style="color: #e2e8f0;">{message["content"]}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message" style="border-left: 3px solid #06b6d4; background: rgba(6, 182, 212, 0.1);">
                    <strong style="color: #06b6d4;">ReliefMate AI:</strong><br>
                    <span style="color: #e2e8f0;">{message["content"]}</span>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 80px 40px; background: rgba(30, 41, 59, 0.6); backdrop-filter: blur(20px); border-radius: 16px; margin: 32px auto; max-width: 700px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4); border: 1px solid rgba(148, 163, 184, 0.2);">
            <div style="font-size: 3.5rem; margin-bottom: 20px;">💬</div>
            <h3 style="color: #ffffff; margin-bottom: 16px; font-weight: 700;">Assistant Ready</h3>
            <p style="color: #94a3b8;">Ask me about emergency procedures, disaster preparedness, or resource management</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# 📊 Relief Reports Dashboard - 3D Glass Cards
# ----------------------------
def render_reports_dashboard(reports):
    st.markdown("## 🚨 Live Relief Operations")
    st.markdown('<p style="color: #94a3b8; margin-bottom: 32px; text-align: center;">Real-time monitoring of active disaster response operations</p>', unsafe_allow_html=True)
    
    # Status summary with glowing metrics
    col1, col2, col3, col4 = st.columns(4)
    
    critical_count = len([r for r in reports if "Critical" in r["status"]])
    active_count = len([r for r in reports if "Active" in r["status"]])
    resolved_count = len([r for r in reports if "Resolved" in r["status"]])
    monitoring_count = len([r for r in reports if "Monitoring" in r["status"]])
    
    with col1:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value" style="color: #ef4444; text-shadow: 0 0 25px rgba(239, 68, 68, 0.6);">{}</div>
            <div class="metric-label">Critical Cases</div>
        </div>
        """.format(critical_count), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value" style="color: #f59e0b; text-shadow: 0 0 25px rgba(245, 158, 11, 0.6);">{}</div>
            <div class="metric-label">Active Operations</div>
        </div>
        """.format(active_count), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value" style="color: #10b981; text-shadow: 0 0 25px rgba(16, 185, 129, 0.6);">{}</div>
            <div class="metric-label">Resolved Cases</div>
        </div>
        """.format(resolved_count), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value" style="color: #3b82f6; text-shadow: 0 0 25px rgba(59, 130, 246, 0.6);">{}</div>
            <div class="metric-label">Under Monitoring</div>
        </div>
        """.format(monitoring_count), unsafe_allow_html=True)
    
    # Detailed reports with glowing chips
    st.markdown("### 📍 Operations Report")
    st.markdown("")  # spacing
    
    for i, report in enumerate(reports):
        # Determine status styling with glow
        if "Critical" in report["status"]:
            status_class = "status-critical"
            icon = "🚨"
            card_glow = "0 0 40px rgba(220, 38, 38, 0.2)"
        elif "Active" in report["status"]:
            status_class = "status-active"
            icon = "⚠️"
            card_glow = "0 0 40px rgba(245, 158, 11, 0.15)"
        elif "Resolved" in report["status"]:
            status_class = "status-resolved"
            icon = "✅"
            card_glow = "0 0 40px rgba(16, 185, 129, 0.15)"
        else:  # Monitoring
            status_class = "status-monitoring"
            icon = "📋"
            card_glow = "0 0 40px rgba(59, 130, 246, 0.15)"
        
        disaster_icons = {
            "Flood": "🌊",
            "Fire": "🔥",
            "Earthquake": "🌍",
            "Cyclone": "🌀",
            "Landslide": "⛰️"
        }
        disaster_icon = disaster_icons.get(report["type"], "⚠️")
        
        st.markdown(f"""
        <div class="glass-card" style="box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), {card_glow}, 0 0 60px rgba(6, 182, 212, 0.05) inset !important;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 12px;">
                <h3 style="color: #ffffff; margin: 0; display: flex; align-items: center; gap: 10px; font-size: 1.3rem; font-weight: 700;">
                    {disaster_icon} {report["location"]} • {report["type"]}
                </h3>
                <span class="{status_class}">
                    {report["status"].replace("🚨 ", "").replace("🔥 ", "").replace("⚠️ ", "").replace("✅ ", "").replace("📋 ", "")}
                </span>
            </div>
            <div style="display: flex; flex-direction: column; gap: 12px; color: #cbd5e1;">
                <p style="margin: 0;"><strong style="color: #94a3b8;">📦 Requirements:</strong> <span style="color: #e2e8f0;">{report["needs"]}</span></p>
                <p style="margin: 0; color: #94a3b8;"><strong style="color: #94a3b8;">👥 Team:</strong> <span style="color: #cbd5e1;">{report["team"]}</span></p>
                <p style="margin: 0; color: #64748b; font-size: 0.85rem;">🕐 Updated: {datetime.datetime.now().strftime('%H:%M')} IST</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# 📈 Analytics Dashboard - Command Center
# ----------------------------
def render_analytics(analytics_data):
    st.markdown("## 📊 Performance Analytics")
    st.markdown('<p style="color: #94a3b8; margin-bottom: 32px; text-align: center;">Data-driven insights for operational efficiency</p>', unsafe_allow_html=True)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Date': analytics_data['dates'],
        'New Requests': analytics_data['requests'],
        'Resolved Cases': analytics_data['resolved'],
        'Active Cases': analytics_data['active']
    })
    
    # Charts with better styling - Embedded in glass panels
    st.markdown("### 📈 7-Day Operations Trend")
    st.markdown('<div style="background: rgba(30, 41, 59, 0.6); backdrop-filter: blur(20px); padding: 28px; border-radius: 16px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4); margin-bottom: 32px; border: 1px solid rgba(148, 163, 184, 0.2);">', unsafe_allow_html=True)
    
    # Line chart using Streamlit
    chart_data = df.set_index('Date')[['New Requests', 'Resolved Cases', 'Active Cases']]
    st.line_chart(chart_data, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Bar chart for comparison
    st.markdown("### 📊 Daily Comparison")
    st.markdown('<div style="background: rgba(30, 41, 59, 0.6); backdrop-filter: blur(20px); padding: 28px; border-radius: 16px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4); margin-bottom: 32px; border: 1px solid rgba(148, 163, 184, 0.2);">', unsafe_allow_html=True)
    st.bar_chart(chart_data, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Summary statistics with neon underlines
    st.markdown("### 💎 Key Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_requests = sum(analytics_data['requests']) // 7
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">📈</div>
            <div class="metric-value">{avg_requests}</div>
            <div class="metric-label">Avg Daily Requests</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_resolved = sum(analytics_data['resolved'])
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">✅</div>
            <div class="metric-value">{total_resolved}</div>
            <div class="metric-label">Total Resolved</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        resolution_rate = round((total_resolved / sum(analytics_data['requests'])) * 100, 1)
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">🎯</div>
            <div class="metric-value">{resolution_rate}%</div>
            <div class="metric-label">Resolution Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional metrics using Streamlit metrics
    st.markdown("### 🎯 Key Indicators")
    
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
# 🛠️ Admin Panel - Pro Tool Feel
# ----------------------------
def render_admin_panel():
    st.markdown("## 🛠️ Administration Panel")
    st.markdown('<p style="color: #94a3b8; margin-bottom: 32px; text-align: center;">Manage relief operations and system configuration</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3 style="margin-bottom: 24px; color: #ffffff; display: flex; align-items: center; gap: 10px;">
                📝 Submit New Report
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        location = st.selectbox("Location", ["Rajkot", "Ahmedabad", "Surat", "Bhavnagar", "Vadodara", "Other"])
        disaster_type = st.selectbox("Disaster Type", ["Flood", "Fire", "Earthquake", "Cyclone", "Landslide", "Other"])
        severity = st.selectbox("Severity Level", ["Critical", "Active", "Monitoring"])
        description = st.text_area("Description", placeholder="Describe the situation and required assistance...", height=120)
        
        if st.button("Submit Report", use_container_width=True):
            st.success(f"✅ Report submitted successfully! Location: {location}, Type: {disaster_type}, Severity: {severity}")
            st.balloons()
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3 style="margin-bottom: 24px; color: #ffffff; display: flex; align-items: center; gap: 10px;">
                📁 Bulk Data Upload
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(10px); border: 2px dashed rgba(100, 116, 139, 0.4); border-radius: 16px; padding: 40px; text-align: center; margin-bottom: 24px; transition: all 0.3s ease; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);">
            <div style="font-size: 2.5rem; margin-bottom: 16px; color: #06b6d4;">📁</div>
            <p style="color: #94a3b8; margin: 0; font-weight: 500;">Drop CSV file or click to browse</p>
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
                st.success(f"✅ File uploaded successfully! {len(df)} records found.")
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
    
    # System Status Section with glowing indicators
    st.markdown("### 🔧 System Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">🟢</div>
            <p style="margin: 0; font-weight: 600; color: #10b981; text-shadow: 0 0 15px rgba(16, 185, 129, 0.5);">Operational</p>
            <p style="margin: 0; font-size: 0.85rem; color: #94a3b8;">System Status</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">🟢</div>
            <p style="margin: 0; font-weight: 600; color: #10b981; text-shadow: 0 0 15px rgba(16, 185, 129, 0.5);">Connected</p>
            <p style="margin: 0; font-size: 0.85rem; color: #94a3b8;">API Status</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">🟢</div>
            <p style="margin: 0; font-weight: 600; color: #10b981; text-shadow: 0 0 15px rgba(16, 185, 129, 0.5);">Online</p>
            <p style="margin: 0; font-size: 0.85rem; color: #94a3b8;">Database</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">⚡</div>
            <p style="margin: 0; font-weight: 600; color: #06b6d4; text-shadow: 0 0 15px rgba(6, 182, 212, 0.5);">&lt;2s</p>
            <p style="margin: 0; font-size: 0.85rem; color: #94a3b8;">Response Time</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# 🚀 Main Application
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
    
    # Status indicator with glassmorphism
    st.markdown(f"""
    <div style="text-align: center; margin: 32px 0 40px 0;">
        <span style="background: rgba(30, 41, 59, 0.6); backdrop-filter: blur(20px); padding: 10px 24px; border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.2); color: #94a3b8; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3); font-size: 0.9rem;">
            ⚡ API Status: {api_status}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Navigation Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🤖 AI Assistant", "🚨 Relief Reports", "📊 Analytics", "🛠️ Admin Panel"])
    
    with tab1:
        render_chat_interface(model, api_status)
    
    with tab2:
        render_reports_dashboard(reports)
    
    with tab3:
        render_analytics(analytics_data)
    
    with tab4:
        render_admin_panel()
    
    # Footer - Minimal & Professional
    st.markdown("""
    <div style="text-align: center; margin-top: 80px; padding: 32px; border-top: 1px solid rgba(148, 163, 184, 0.2); background: rgba(15, 23, 42, 0.5); backdrop-filter: blur(10px);">
        <p style="color: #64748b; margin: 0; font-size: 0.875rem; font-weight: 500;">
            © 2025 ReliefMate AI • Emergency Hotline: <span style="color: #06b6d4;">112 (Police) | 108 (Medical) | 101 (Fire)</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
