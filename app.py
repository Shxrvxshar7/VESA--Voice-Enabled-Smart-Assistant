import streamlit as st
from pymongo import MongoClient
from datetime import datetime, timedelta
import time
import threading

# MongoDB Setup
client = MongoClient("mongodb+srv://llm:llm@alpha1.aul5rqy.mongodb.net/?retryWrites=true&w=majority&appName=Alpha1")
db = client["vesa_db"]

# Collections
status_col = db["system_status"]
conversations_col = db["conversations"]

# UI Refresh Settings
POLL_INTERVAL = 1  # Seconds between checks
MAX_HISTORY = 20    # Max conversation items to show

def get_real_time_data():
    """Simplified data fetch"""
    return {
        "status": status_col.find_one(sort=[("timestamp", -1)]),
        "conversations": list(conversations_col.find()
                             .sort("timestamp", -1)
                             .limit(MAX_HISTORY))
    }

def status_indicator(current_status):
    """Display system status with color coding"""
    status_map = {
        "listening": ("🎧 Listening", "green"),
        "processing": ("⚙️ Processing", "blue"),
        "idle": ("💤 Idle", "gray")
    }
    
    status_text, color = status_map.get(
        current_status.lower(), 
        ("❓ Unknown", "red")
    )
    
    st.markdown(f"""
    <div style="
        border: 2px solid {color};
        border-radius: 5px;
        padding: 10px;
        text-align: center;
        margin: 10px 0;
    ">
        <h3 style="color: {color}; margin:0;">{status_text}</h3>
    </div>
    """, unsafe_allow_html=True)

def conversation_stream():
    st.subheader("Real-time Processing Pipeline")
    
    status_placeholder = st.empty()
    history_placeholder = st.empty()
    
    while True:
        current_data = get_real_time_data()
        
        # Status Indicator
        with status_placeholder.container():
            status = current_data["status"].get("status", "idle")
            st.metric("Current Status", status,
                     help=f"Last update: {current_data['status']['timestamp']}")
        
        # Conversation History
        with history_placeholder.container():
            st.write("### Recent Interactions")
            
            for convo in current_data["conversations"]:
                cols = st.columns([1,3,3])
                
                cols[0].write(f"**{convo['timestamp'].time()}**")
                
                cols[1].write(f"🗣️ {convo.get('input', '')}")
                
                response_text = convo.get('response', '')
                if 'error' in convo:
                    cols[2].error(f"❌ {convo['error']}")
                else:
                    cols[2].write(f"🤖 {response_text[:75]}{'...' if len(response_text)>75 else ''}")

        time.sleep(POLL_INTERVAL)

def main():
    st.set_page_config(
        page_title="VESA Live Monitor",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("VESA - Real-time Monitoring Dashboard")
    
    # Start real-time updates in thread
    threading.Thread(target=conversation_stream, daemon=True).start()
    
    # Static components
    with st.sidebar:
        st.header("System Controls")
        st.slider("Polling Interval (sec)", 1, 10, POLL_INTERVAL)
        st.button("Force Refresh")
        st.write("### Database Stats")
        st.write(f"Conversations: {conversations_col.count_documents({})}")
        st.write(f"Status Updates: {status_col.count_documents({})}")

if __name__ == "__main__":
    main()