import streamlit as st
import requests
import json
from datetime import datetime
import time

# Add this import for custom CSS
st.set_page_config(
    page_title="VESA Dashboard",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for dark theme UI
st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap');
    @import url('https://api.fontshare.com/v2/css?f[]=cal-sans@400,700&display=swap');
    
    /* Base styles */
    .main {
        background-color: #1a1a1a;
        color: #ffffff;
        padding: 2rem;
        font-family: 'Space Mono', monospace;
    }
    
    /* Card containers */
    .conversation-container {
        margin: 15px auto;
        padding: 20px;
        border-radius: 12px;
        background-color: #2d2d2d;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        max-width: 800px;
        width: 100%;
        font-family: 'Space Mono', monospace;
    }
    
    /* Keyword detection */
    .status-active {
        color: #8ab4f8;
        animation: pulse 2s infinite;
        background: linear-gradient(45deg, #1a1a1a, #2d2d2d);
        border-left: 4px solid #8ab4f8;
    }
    
    /* User message */
    .user-message {
        background: linear-gradient(45deg, #2d2d2d, #353535);
        border-left: 4px solid #8ab4f8;
    }
    
    /* Assistant message */
    .assistant-message {
        background: linear-gradient(45deg, #2d2d2d, #353535);
        border-left: 4px solid #00ff95;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-family: 'Cal Sans', sans-serif !important;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    /* Status message */
    .status-message {
        text-align: center;
        color: #8ab4f8;
        padding: 10px;
        border-radius: 10px;
        background: linear-gradient(45deg, #2d2d2d, #353535);
        margin: 10px auto;
        max-width: 800px;
        font-family: 'Space Mono', monospace;
    }
    
    /* Streamlit elements override */
    .stMarkdown, .stText, .stStatus {
        font-family: 'Space Mono', monospace !important;
    }
    
    .sidebar .stMarkdown {
        font-family: 'Cal Sans', sans-serif !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #4d4d4d;
        border-radius: 4px;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.6; }
        100% { opacity: 1; }
    }

    /* Sliding Sidebar */
    .sidebar-content {
        position: fixed;
        right: -300px;
        top: 0;
        width: 300px;
        height: 100vh;
        background: #2d2d2d;
        transition: right 0.3s ease-in-out;
        padding: 2rem;
        z-index: 1000;
        box-shadow: -2px 0 10px rgba(0,0,0,0.3);
    }

    .sidebar-content.visible {
        right: 0;
    }

    .sidebar-toggle {
        position: fixed;
        right: 20px;
        top: 20px;
        z-index: 1001;
        background: #8ab4f8;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    /* Keyword Detection Card */
    .keyword-active {
        background: linear-gradient(45deg, #1a472a, #2d503d);
        border-left: 4px solid #00ff95;
        animation: glow 2s infinite;
    }

    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(0,255,149,0.2); }
        50% { box-shadow: 0 0 20px rgba(0,255,149,0.4); }
        100% { box-shadow: 0 0 5px rgba(0,255,149,0.2); }
    }
    </style>

    <script>
        function toggleSidebar() {
            const sidebar = document.querySelector('.sidebar-content');
            sidebar.classList.toggle('visible');
        }
    </script>
""", unsafe_allow_html=True)

# Constants
FLASK_SERVER_URL = "http://localhost:5000"

def fetch_latest_status():
    try:
        response = requests.get(f"{FLASK_SERVER_URL}/get_latest_status")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# Main layout with enhanced styling
st.title("VESA Assistant Dashboard")
st.markdown("---")

# Create vertical containers
keyword_container = st.container()
with keyword_container:
    st.markdown("### Keyword Detection")
    keyword_placeholder = st.empty()

transcription_container = st.container()
with transcription_container:
    st.markdown("### User Input")
    transcription_placeholder = st.empty()

response_container = st.container()
with response_container:
    st.markdown("### VESA Response")
    response_placeholder = st.empty()

# Update the update_dashboard function
def update_dashboard():
    status = fetch_latest_status()
    if status:
        # Update keyword detection with conditional styling
        if 'keyword' in status and status['keyword'] is not None:
            is_adam = status['keyword'].lower() == 'adam'
            card_class = 'keyword-active' if is_adam else 'status-active'
            keyword_placeholder.markdown(
                f"""
                <div class='conversation-container {card_class}'>
                    <div style='display: flex; align-items: center; justify-content: space-between'>
                        <span>Keyword Detected</span>
                        <span style='color: {"#00ff95" if is_adam else "#8ab4f8"}; font-weight: bold'>
                            {status['keyword']}
                        </span>
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        # Enhanced transcription display
        if 'transcription' in status:
            transcription_placeholder.markdown(
                f"""
                <div class='conversation-container user-message'>
                    <b style='color: #8ab4f8'>User:</b> {status['transcription']}
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        # Enhanced response display
        if 'response' in status:
            response_type = status.get('response_type', 'general')
            response_placeholder.markdown(
                f"""
                <div class='conversation-container assistant-message'>
                    <span style='color: #00ff95'><b>Type:</b> {response_type}</span><br>
                    <b style='color: #00ff95'>VESA:</b> {status['response']}
                </div>
                """, 
                unsafe_allow_html=True
            )

# Sidebar with better styling
st.sidebar.markdown("### Dashboard Controls")
refresh_rate = st.sidebar.slider('Refresh Rate (seconds)', 1, 10, 2)

# Status message with loading animation
status_container = st.container()
status_placeholder = status_container.empty()

# Auto-refresh section with enhanced status display
auto_refresh = st.sidebar.checkbox('Enable Auto-refresh', value=True)

if auto_refresh:
    while True:
        update_dashboard()
        status_placeholder.markdown(
            """
            <div class='status-message'>
                <h4>Dashboard updating in real-time...</h4>
            </div>
            """,
            unsafe_allow_html=True
        )
        time.sleep(refresh_rate)

# Enhanced manual refresh button
if not auto_refresh and st.button('Refresh Now'):
    update_dashboard()

# Add sidebar toggle button and container
st.markdown("""
    <button onclick="toggleSidebar()" class="sidebar-toggle">≡</button>
    <div class="sidebar-content">
        <h3 style="color: #ffffff; margin-bottom: 2rem;">Dashboard Controls</h3>
        <!-- Controls will be injected here -->
    </div>
""", unsafe_allow_html=True)