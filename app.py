
import streamlit as st
import time
import datetime
import json
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from io import BytesIO
import base64

# Set page configuration
st.set_page_config(
    page_title="Lock-In App",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    /* Main theme colors */
    .main {
        background-color: #1E1E1E;
    }
    
    .sidebar .sidebar-content {
        background-color: #2D2D2D;
    }
    
    /* Custom card styling */
    .metric-card {
        background-color: #2D2D2D;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4A90E2;
        margin: 0.5rem 0;
    }
    
    /* Timer display */
    .timer-display {
        background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
        border-radius: 1rem;
        padding: 2rem;
        text-align: center;
        border: 2px solid #4A90E2;
        margin: 1rem 0;
    }
    
    .timer-text {
        font-size: 4rem;
        font-weight: bold;
        color: #4A90E2;
        font-family: 'Courier New', monospace;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #4A90E2;
        color: white;
        border-radius: 0.5rem;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: background-color 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #0066CC;
    }
    
    /* Alarm card */
    .alarm-card {
        background-color: #2D2D2D;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #00CC66;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Success/Error styling */
    .stSuccess {
        background-color: #00CC6620;
        border: 1px solid #00CC66;
    }
    
    .stError {
        background-color: #CC006620;
        border: 1px solid #CC0066;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    """Initialize all session state variables"""
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
    if 'timer_seconds' not in st.session_state:
        st.session_state.timer_seconds = 0
    if 'timer_total' not in st.session_state:
        st.session_state.timer_total = 0
    if 'uploaded_docs' not in st.session_state:
        st.session_state.uploaded_docs = []
    if 'alarms' not in st.session_state:
        st.session_state.alarms = []
    if 'study_time_today' not in st.session_state:
        st.session_state.study_time_today = 127
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = {}

def format_time(seconds):
    """Format seconds into HH:MM:SS format"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def create_timer_card(title, time_str, description=""):
    """Create a styled timer card"""
    st.markdown(f"""
    <div class="timer-display">
        <h3 style="color: #4A90E2; margin: 0;">{title}</h3>
        <div class="timer-text">{time_str}</div>
        <p style="color: #CCCCCC; margin: 0;">{description}</p>
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(title, value, delta=None):
    """Create a styled metric card"""
    delta_html = f"<small style='color: #00CC66;'>{delta}</small>" if delta else ""
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color: #4A90E2; margin: 0 0 0.5rem 0;">{title}</h4>
        <h2 style="color: white; margin: 0;">{value}</h2>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

# Main dashboard
def main_dashboard():
    st.title("🎯 Lock-In Dashboard")
    st.markdown("### Focus. Study. Achieve.")
    
    # Quick stats row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_metric_card("Today's Study Time", f"{st.session_state.study_time_today} min", "+12 min")
    
    with col2:
        create_metric_card("Documents", len(st.session_state.uploaded_docs), "+2 today")
    
    with col3:
        create_metric_card("Focus Sessions", "12", "+3 today")
    
    with col4:
        create_metric_card("Analysis Done", len(st.session_state.analysis_results), "+1 today")

    st.markdown("---")

    # Timer and Alarm sections
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### ⏱️ Study Timer")
        
        # Timer display
        if st.session_state.timer_total > 0:
            current_time = st.session_state.timer_seconds
            progress = (st.session_state.timer_total - current_time) / st.session_state.timer_total
            
            # Progress bar
            st.progress(progress)
            
            # Timer display
            create_timer_card("Current Session", format_time(current_time), 
                            "Stay focused!" if st.session_state.timer_running else "Timer paused")
        else:
            create_timer_card("Ready to Start", "00:00:00", "Set your focus time below")
        
        # Timer controls
        timer_col1, timer_col2, timer_col3 = st.columns(3)
        
        with timer_col1:
            hours = st.selectbox("Hours", range(0, 24), index=0)
        with timer_col2:
            minutes = st.selectbox("Minutes", range(0, 60), index=25)
        with timer_col3:
            seconds = st.selectbox("Seconds", range(0, 60), index=0)
        
        # Control buttons
        btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
        
        with btn_col1:
            if st.button("🎯 Start Timer", type="primary"):
                total_seconds = hours * 3600 + minutes * 60 + seconds
                if total_seconds > 0:
                    st.session_state.timer_seconds = total_seconds
                    st.session_state.timer_total = total_seconds
                    st.session_state.timer_running = True
                    st.success("Timer started! Stay focused!")
                    st.rerun()
        
        with btn_col2:
            if st.button("⏸️ Pause"):
                st.session_state.timer_running = False
                st.rerun()
        
        with btn_col3:
            if st.button("▶️ Resume"):
                if st.session_state.timer_seconds > 0:
                    st.session_state.timer_running = True
                    st.rerun()
        
        with btn_col4:
            if st.button("🔄 Reset"):
                st.session_state.timer_running = False
                st.session_state.timer_seconds = 0
                st.session_state.timer_total = 0
                st.rerun()
        
        # Quick preset buttons
        st.markdown("#### ⚡ Quick Presets")
        preset_col1, preset_col2, preset_col3, preset_col4 = st.columns(4)
        
        presets = [
            ("🍅 Pomodoro", 25 * 60),
            ("📚 Deep Work", 90 * 60),
            ("⚡ Quick Review", 15 * 60),
            ("📝 Mock Test", 120 * 60)
        ]
        
        for i, (name, duration) in enumerate(presets):
            with [preset_col1, preset_col2, preset_col3, preset_col4][i]:
                if st.button(name):
                    st.session_state.timer_seconds = duration
                    st.session_state.timer_total = duration
                    st.session_state.timer_running = True
                    st.success(f"{name} started!")
                    st.rerun()

    with col2:
        st.markdown("### ⏰ Alarms")
        
        # Add new alarm
        with st.expander("➕ Add New Alarm"):
            alarm_time = st.time_input("Alarm Time", datetime.time(9, 0))
            alarm_label = st.text_input("Alarm Label", "Study Time!")
            
            if st.button("Set Alarm"):
                new_alarm = {
                    'time': alarm_time.strftime("%H:%M"),
                    'label': alarm_label,
                    'active': True,
                    'id': len(st.session_state.alarms)
                }
                st.session_state.alarms.append(new_alarm)
                st.success("Alarm set successfully!")
                st.rerun()
        
        # Display alarms
        if st.session_state.alarms:
            st.markdown("#### Active Alarms")
            for i, alarm in enumerate(st.session_state.alarms):
                alarm_status = "🔔" if alarm['active'] else "🔕"
                st.markdown(f"""
                <div class="alarm-card">
                    <strong>{alarm_status} {alarm['time']}</strong><br>
                    <small>{alarm['label']}</small>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"❌ Remove", key=f"remove_alarm_{i}"):
                    st.session_state.alarms.pop(i)
                    st.rerun()
        else:
            st.info("No alarms set. Add one above!")

    # Timer auto-update
    if st.session_state.timer_running and st.session_state.timer_seconds > 0:
        time.sleep(1)
        st.session_state.timer_seconds -= 1
        if st.session_state.timer_seconds <= 0:
            st.session_state.timer_running = False
            st.balloons()
            st.success("🎉 Timer completed! Great job!")
        st.rerun()

# Sidebar navigation
def sidebar_navigation():
    """Create sidebar navigation"""
    st.sidebar.markdown("# 🎯 Lock-In App")
    st.sidebar.markdown("### Focus • Study • Achieve")
    
    # Navigation buttons
    pages = {
        "🏠 Dashboard": "dashboard",
        "📁 Documents": "documents", 
        "🤖 AI Analysis": "analysis",
        "🎯 Focus Mode": "focus",
        "⚙️ Settings": "settings"
    }
    
    # Current page indicator
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "dashboard"
    
    for page_name, page_key in pages.items():
        if st.sidebar.button(page_name, key=page_key, 
                           type="primary" if st.session_state.current_page == page_key else "secondary"):
            st.session_state.current_page = page_key
            st.rerun()
    
    st.sidebar.markdown("---")
    
    # Quick stats in sidebar
    st.sidebar.metric("Study Streak", "15 days", "🔥")
    st.sidebar.metric("Total Documents", len(st.session_state.uploaded_docs))
    
    # Progress toward daily goal
    daily_goal = 120  # 2 hours
    progress_pct = min(st.session_state.study_time_today / daily_goal, 1.0)
    st.sidebar.progress(progress_pct)
    st.sidebar.caption(f"Daily Goal: {st.session_state.study_time_today}/{daily_goal} min")

# Main app logic
def main():
    initialize_session_state()
    sidebar_navigation()
    
    # Route to appropriate page
    if st.session_state.current_page == "dashboard":
        main_dashboard()
    elif st.session_state.current_page == "documents":
        st.switch_page("pages/documents.py")
    elif st.session_state.current_page == "analysis":
        st.switch_page("pages/ai_analysis.py")
    elif st.session_state.current_page == "focus":
        st.switch_page("pages/focus_mode.py")
    elif st.session_state.current_page == "settings":
        st.switch_page("pages/settings.py")

if __name__ == "__main__":
    main()
