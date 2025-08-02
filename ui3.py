import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time
import random
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any
import threading
import queue

# Page configuration
st.set_page_config(
    page_title="⚡ BatteryFlow Pro",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with Light/Dark Theme Support
def apply_modern_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Light/Dark Theme Variables */
    :root {
        --primary-color: #00d4ff;
        --secondary-color: #0099cc;
        --accent-color: #ff6b6b;
        --success-color: #51cf66;
        --warning-color: #ffd43b;
        --danger-color: #ff6b6b;
    }
    
    /* Dark Theme (Default) */
    :root {
        --text-primary: #ffffff;
        --text-secondary: #b0b0b0;
        --text-muted: #666666;
        --bg-primary: #0a0a0a;
        --bg-secondary: #1a1a1a;
        --bg-tertiary: #2a2a2a;
        --bg-card: #1e1e1e;
        --bg-input: #2d2d2d;
        --border-color: #333333;
        --border-hover: #555555;
        --shadow-light: 0 2px 8px rgba(0, 212, 255, 0.1);
        --shadow-medium: 0 4px 16px rgba(0, 212, 255, 0.15);
        --shadow-heavy: 0 8px 32px rgba(0, 212, 255, 0.2);
        --gradient-primary: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        --gradient-danger: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        --gradient-success: linear-gradient(135deg, #51cf66 0%, #40c057 100%);
        --border-radius: 12px;
        --border-radius-lg: 16px;
    }
    
    /* Light Theme */
    [data-theme="light"] {
        --text-primary: #1a1a1a;
        --text-secondary: #4a4a4a;
        --text-muted: #888888;
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fa;
        --bg-tertiary: #e9ecef;
        --bg-card: #ffffff;
        --bg-input: #f8f9fa;
        --border-color: #dee2e6;
        --border-hover: #adb5bd;
        --shadow-light: 0 2px 8px rgba(0, 0, 0, 0.1);
        --shadow-medium: 0 4px 16px rgba(0, 0, 0, 0.15);
        --shadow-heavy: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    /* Global Styles */
    .stApp {
        background: var(--bg-primary);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Sidebar Styling */
    .css-1d391kg, .css-1cypcdb {
        background: var(--bg-secondary);
        border-right: 1px solid var(--border-color);
    }
    
    .css-1lcbmhc {
        background: transparent;
    }
    
    /* Button Styling - Fixed for better responsiveness */
    .stButton > button {
        background: var(--bg-tertiary);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        width: 100%;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        background: var(--primary-color);
        border-color: var(--primary-color);
        color: var(--bg-primary);
        transform: translateY(-1px);
        box-shadow: var(--shadow-medium);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: var(--shadow-light);
    }
    
    /* Emergency Button - Fixed positioning and responsiveness */
    .emergency-button {
        position: relative;
        margin: 1rem 0;
        animation: pulse-emergency 2s infinite;
    }
    
    .emergency-button button {
        background: var(--gradient-danger) !important;
        color: white !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.8rem 1.5rem !important;
    }
    
    .emergency-button:hover button {
        animation: none !important;
        transform: scale(1.05) !important;
    }
    
    @keyframes pulse-emergency {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* Navigation Button Fixes */
    .nav-button-container {
        margin: 0.5rem 0;
    }
    
    .nav-button-container button {
        background: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        transition: all 0.3s ease !important;
    }
    
    .nav-button-container button:hover {
        background: var(--primary-color) !important;
        color: var(--bg-primary) !important;
        border-color: var(--primary-color) !important;
    }
    
    .nav-button-active button {
        background: var(--gradient-primary) !important;
        color: var(--bg-primary) !important;
        border-color: var(--primary-color) !important;
    }
    
    /* Setup Button on Dashboard - Fixed */
    .setup-redirect-btn {
        background: var(--gradient-primary) !important;
        color: var(--bg-primary) !important;
        border: none !important;
        padding: 1rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border-radius: var(--border-radius) !important;
        transition: all 0.3s ease !important;
        text-decoration: none !important;
        display: inline-block !important;
        text-align: center !important;
        cursor: pointer !important;
    }
    
    .setup-redirect-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-heavy) !important;
    }
    
    /* Form Controls */
    .stSelectbox > div > div,
    .stNumberInput > div > div,
    .stTextInput > div > div,
    .stSlider > div {
        background: var(--bg-input);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        color: var(--text-primary);
    }
    
    .stSelectbox > div > div:focus-within,
    .stNumberInput > div > div:focus-within,
    .stTextInput > div > div:focus-within {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(0, 212, 255, 0.2);
    }
    
    /* Main Header */
    .main-header {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-lg);
        padding: 2rem;
        margin: 1rem 0 2rem 0;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow-light);
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-primary);
        border-radius: var(--border-radius-lg) var(--border-radius-lg) 0 0;
    }
    
    .main-header h1 {
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        font-size: 2.5rem;
        margin: 0;
        letter-spacing: -1px;
    }
    
    .main-header p {
        color: var(--text-secondary);
        font-weight: 400;
        margin: 1rem 0 0 0;
        font-size: 1rem;
    }
    
    /* Content Cards */
    .content-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-lg);
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-light);
    }
    
    .content-card:hover {
        border-color: var(--border-hover);
        box-shadow: var(--shadow-medium);
    }
    
    .content-card h2, .content-card h3 {
        color: var(--text-primary);
        margin-top: 0;
        font-weight: 600;
    }
    
    /* Welcome Card with Setup Button */
    .welcome-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-lg);
        padding: 3rem;
        margin: 2rem 0;
        text-align: center;
        box-shadow: var(--shadow-medium);
    }
    
    .welcome-card h2 {
        color: var(--text-primary);
        margin-bottom: 1rem;
        font-size: 2rem;
    }
    
    .welcome-card p {
        color: var(--text-secondary);
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    
    /* Cell Cards */
    .cell-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-lg);
        margin: 1rem 0;
        overflow: hidden;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-light);
    }
    
    .cell-card:hover {
        border-color: var(--primary-color);
        box-shadow: var(--shadow-medium);
        transform: translateY(-2px);
    }
    
    .cell-header {
        background: var(--gradient-primary);
        color: var(--bg-primary);
        padding: 1.25rem;
        position: relative;
    }
    
    .cell-header.lfp {
        background: linear-gradient(135deg, #51cf66 0%, #40c057 100%);
    }
    
    .cell-header.nmc {
        background: linear-gradient(135deg, #339af0 0%, #228be6 100%);
    }
    
    .cell-header.lto {
        background: linear-gradient(135deg, #ff8cc8 0%, #ff6b6b 100%);
    }
    
    .cell-info {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .cell-avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: rgba(255,255,255,0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1rem;
        border: 2px solid rgba(255,255,255,0.3);
        font-family: 'JetBrains Mono', monospace;
    }
    
    .cell-name {
        font-size: 1.2rem;
        font-weight: 700;
        margin: 0;
    }
    
    .cell-type {
        font-size: 0.85rem;
        opacity: 0.9;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .cell-content {
        padding: 1.25rem;
    }
    
    .cell-metrics {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .metric-item {
        text-align: center;
        padding: 0.75rem;
        background: var(--bg-tertiary);
        border-radius: var(--border-radius);
        border: 1px solid var(--border-color);
    }
    
    .metric-value {
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin: 0;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: var(--text-muted);
        margin: 0.25rem 0 0 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 500;
        font-size: 0.85rem;
        margin: 0.5rem 0;
    }
    
    .status-normal {
        background: var(--gradient-success);
        color: var(--bg-primary);
    }
    
    .status-warning {
        background: linear-gradient(135deg, var(--warning-color), #fcc419);
        color: var(--bg-primary);
    }
    
    .status-critical {
        background: var(--gradient-danger);
        color: var(--text-primary);
    }
    
    /* Progress Bar */
    .progress-container {
        background: var(--bg-tertiary);
        border-radius: 6px;
        height: 6px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        background: var(--gradient-primary);
        border-radius: 6px;
        transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Dashboard Metrics Grid */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-lg);
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow-light);
    }
    
    .metric-card:hover {
        border-color: var(--primary-color);
        box-shadow: var(--shadow-medium);
        transform: translateY(-2px);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-primary);
    }
    
    .metric-number {
        font-size: 2rem;
        font-weight: 800;
        color: var(--primary-color);
        margin: 0;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .metric-title {
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin: 0.5rem 0 0 0;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 500;
    }
    
    /* Theme Toggle */
    .theme-toggle {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-medium);
    }
    
    .theme-toggle:hover {
        box-shadow: var(--shadow-heavy);
        transform: scale(1.1);
    }
    
    /* Timeline */
    .timeline {
        position: relative;
        padding: 2rem 0;
    }
    
    .timeline::before {
        content: '';
        position: absolute;
        left: 20px;
        top: 0;
        bottom: 0;
        width: 2px;
        background: var(--gradient-primary);
    }
    
    .timeline-item {
        position: relative;
        margin: 2rem 0;
        padding-left: 3rem;
    }
    
    .timeline-marker {
        position: absolute;
        left: 11px;
        top: 50%;
        transform: translateY(-50%);
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: var(--primary-color);
        border: 3px solid var(--bg-primary);
        box-shadow: var(--shadow-light);
    }
    
    .timeline-content {
        background: var(--bg-card);
        padding: 1.25rem;
        border-radius: var(--border-radius);
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-light);
    }
    
    /* Chart Styling */
    .chart-container {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-lg);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-light);
    }
    
    /* Animations */
    .fade-in {
        animation: fadeIn 0.6s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-in-left {
        animation: slideInLeft 0.6s ease-in-out;
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .bounce-in {
        animation: bounceIn 0.8s ease-in-out;
    }
    
    @keyframes bounceIn {
        0% { opacity: 0; transform: scale(0.3); }
        50% { opacity: 1; transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { transform: scale(1); }
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .cell-metrics {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .metrics-grid {
            grid-template-columns: 1fr;
        }
        
        .theme-toggle {
            position: relative;
            margin: 1rem auto;
        }
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-color);
    }
    
    /* Override Streamlit specific styles */
    .stApp > div:first-child {
        background: var(--bg-primary);
    }
    
    /* Fix for plotly charts in different themes */
    .js-plotly-plot {
        background: var(--bg-card) !important;
        border-radius: var(--border-radius-lg);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    defaults = {
        'cells_data': {},
        'task_queue': [],
        'current_task_index': 0,
        'task_running': False,
        'emergency_stop': False,
        'process_history': [],
        'stress_test_mode': False,
        'history': [],
        'favorites': [],
        'temp_history': {},
        'current_page': 'Dashboard',
        'live_animation': True,
        'auto_refresh': True,
        'theme': 'dark',
        'sidebar_visible': True
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Apply CSS and initialize
def initialize_app():
    init_session_state()
    apply_modern_css()
    
    # Apply theme
    if st.session_state.theme == 'light':
        st.markdown("""
        <script>
        document.documentElement.setAttribute('data-theme', 'light');
        </script>
        """, unsafe_allow_html=True)

# Utility Functions
def get_cell_specs(cell_type):
    specs = {
        "LFP": {"voltage": 3.2, "min_voltage": 2.5, "max_voltage": 3.6, "color": "#51cf66"},
        "NMC": {"voltage": 3.6, "min_voltage": 3.0, "max_voltage": 4.2, "color": "#339af0"},
        "LTO": {"voltage": 2.4, "min_voltage": 1.5, "max_voltage": 2.8, "color": "#ff8cc8"}
    }
    return specs.get(cell_type, specs["NMC"])

def calculate_charge_percentage(voltage, min_voltage, max_voltage):
    return max(0, min(100, ((voltage - min_voltage) / (max_voltage - min_voltage)) * 100))

def get_safety_status(cell_data):
    voltage = cell_data.get("voltage", 0)
    current = cell_data.get("current", 0)
    temp = cell_data.get("temp", cell_data.get("temperature", 25))
    min_voltage = cell_data.get("min_voltage", 2.8)
    max_voltage = cell_data.get("max_voltage", 4.0)
    
    warnings = []
    if voltage < min_voltage * 1.1:
        warnings.append("⚠️ Low Voltage")
    if voltage > max_voltage * 0.95:
        warnings.append("⚠️ High Voltage")
    if temp > 45:
        warnings.append("🌡️ High Temperature")
    if temp < 10:
        warnings.append("❄️ Low Temperature")
    if abs(current) > 5:
        warnings.append("⚡ High Current")
    
    return warnings

def create_cell(cell_type: str, cell_id: str) -> Dict[str, Any]:
    specs = get_cell_specs(cell_type)
    return {
        "type": cell_type,
        "cell_type": cell_type,
        "voltage": specs["voltage"],
        "current": 0.0,
        "temp": round(random.uniform(25, 35), 1),
        "temperature": round(random.uniform(25, 35), 1),
        "capacity": 0.0,
        "min_voltage": specs["min_voltage"],
        "max_voltage": specs["max_voltage"],
        "health": 100.0,
        "cycles": 0,
        "status": "Idle",
        "created_at": datetime.now()
    }

def update_cell_real_time(cell_id: str):
    if cell_id in st.session_state.cells_data:
        cell = st.session_state.cells_data[cell_id]
        
        # Add realistic variations
        temp_variation = random.uniform(-0.2, 0.2)
        voltage_variation = random.uniform(-0.003, 0.003)
        
        current_temp = cell.get("temp", cell.get("temperature", 25))
        cell["temp"] = max(15, min(55, current_temp + temp_variation))
        cell["temperature"] = cell["temp"]
        
        current_voltage = cell.get("voltage", 3.6)
        cell["voltage"] = max(cell["min_voltage"], min(cell["max_voltage"], current_voltage + voltage_variation))
        cell["capacity"] = round(cell["voltage"] * abs(cell["current"]), 2)

def update_temp_history():
    current_time = datetime.now()
    
    # Clean up temp history for cells that no longer exist
    cells_to_remove = [cell_key for cell_key in st.session_state.temp_history 
                      if cell_key not in st.session_state.cells_data]
    
    for cell_key in cells_to_remove:
        del st.session_state.temp_history[cell_key]
    
    # Update temperature history for existing cells
    for cell_key, cell_data in st.session_state.cells_data.items():
        if cell_key not in st.session_state.temp_history:
            st.session_state.temp_history[cell_key] = {"time": [], "temp": []}
        
        temp = cell_data.get("temp", cell_data.get("temperature", 25))
        st.session_state.temp_history[cell_key]["time"].append(current_time)
        st.session_state.temp_history[cell_key]["temp"].append(temp)
        
        # Keep only last 30 readings
        if len(st.session_state.temp_history[cell_key]["time"]) > 30:
            st.session_state.temp_history[cell_key]["time"] = st.session_state.temp_history[cell_key]["time"][-30:]
            st.session_state.temp_history[cell_key]["temp"] = st.session_state.temp_history[cell_key]["temp"][-30:]

# Emergency Stop Function - FIXED
def emergency_stop():
    st.session_state.emergency_stop = True
    st.session_state.task_running = False
    st.session_state.stress_test_mode = False
    
    # Reset all cells to safe state
    for cell_name in st.session_state.cells_data:
        cell = st.session_state.cells_data[cell_name]
        cell['current'] = 0.0
        cell['status'] = 'Emergency Stop'
    
    # Clear task queue
    for task in st.session_state.task_queue:
        if task['status'] == 'Running':
            task['status'] = 'Stopped'
    
    st.error("🚨 EMERGENCY STOP ACTIVATED! All operations halted.")
    st.rerun()

# Page Navigation Function - FIXED
def navigate_to_page(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# Sidebar Navigation - FIXED
def render_sidebar():
    with st.sidebar:
        # Logo and Title
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="color: var(--primary-color); font-size: 1.8rem; margin: 0; font-weight: 800;">⚡ BatteryFlow</h1>
            <p style="color: var(--text-secondary); margin: 0.5rem 0 0 0; font-size: 0.9rem;">Professional Management</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Theme Toggle
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌙 Dark" if st.session_state.theme == 'light' else "☀️ Light", 
                        key="theme_toggle", use_container_width=True):
                st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
                st.rerun()
        
        with col2:
            if st.button("🔄 Refresh", key="sidebar_refresh", use_container_width=True):
                if st.session_state.cells_data:
                    for cell_key in st.session_state.cells_data:
                        update_cell_real_time(cell_key)
                    update_temp_history()
                    st.success("Data refreshed!")
                    st.rerun()
        
        st.divider()
        
        # Navigation Menu - FIXED
        nav_items = [
            ("🏠", "Dashboard"),
            ("🔧", "Setup"),
            ("🎛️", "Control Panel"),
            ("⚙️", "Task Processes"),
            ("📊", "Analytics")
        ]
        
        for icon, label in nav_items:
            is_active = st.session_state.current_page == label
            button_class = "nav-button-active" if is_active else "nav-button-container"
            
            st.markdown(f'<div class="{button_class}">', unsafe_allow_html=True)
            if st.button(f"{icon} {label}", 
                        key=f"nav_{label.lower().replace(' ', '_')}", 
                        use_container_width=True):
                navigate_to_page(label)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Emergency Stop - FIXED
        st.markdown("### 🚨 Emergency Controls")
        
        st.markdown('<div class="emergency-button">', unsafe_allow_html=True)
        if st.button("🚨 EMERGENCY STOP", key="emergency_stop_btn", use_container_width=True):
            emergency_stop()
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.emergency_stop:
            st.markdown('<div class="emergency-button">', unsafe_allow_html=True)
            if st.button("✅ Reset Emergency", key="reset_emergency_btn", use_container_width=True):
                st.session_state.emergency_stop = False
                for cell_name in st.session_state.cells_data:
                    st.session_state.cells_data[cell_name]['status'] = 'Idle'
                st.success("✅ Emergency state reset!")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # System Status
        st.markdown("### 📊 System Status")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Cells", len(st.session_state.cells_data))
            st.metric("Tasks", len(st.session_state.task_queue))
        with col2:
            active_warnings = sum(len(get_safety_status(cell)) for cell in st.session_state.cells_data.values())
            st.metric("Warnings", active_warnings)
            st.metric("History", len(st.session_state.history))
        
        # Auto-refresh toggle
        st.session_state.auto_refresh = st.toggle("🔄 Auto Refresh", value=st.session_state.auto_refresh)

# Main Header
def render_header():
    st.markdown(f"""
    <div class="main-header fade-in">
        <h1>⚡ BatteryFlow Pro</h1>
        <p>Advanced Battery Management System • Real-time Monitoring • Intelligent Analytics</p>
    </div>
    """, unsafe_allow_html=True)

# Dashboard Page - FIXED with working Setup button
def render_dashboard():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    if not st.session_state.cells_data:
        st.markdown("""
        <div class="welcome-card bounce-in">
            <h2>🚀 Welcome to BatteryFlow Pro!</h2>
            <p>Get started by setting up your battery cells to begin monitoring and management.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # FIXED Setup Button - Now properly redirects
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔧 Setup Cells", key="dashboard_setup_btn", use_container_width=True):
                navigate_to_page("Setup")
        
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # System Overview Metrics
    total_cells = len(st.session_state.cells_data)
    active_cells = sum(1 for cell in st.session_state.cells_data.values() if cell.get('status', 'Idle') != 'Idle')
    avg_voltage = np.mean([cell["voltage"] for cell in st.session_state.cells_data.values()])
    temps = [cell.get("temp", cell.get("temperature", 25)) for cell in st.session_state.cells_data.values()]
    avg_temp = np.mean(temps)
    warnings_count = sum(len(get_safety_status(cell)) for cell in st.session_state.cells_data.values())
    
    st.markdown("""
    <div class="metrics-grid slide-in-left">
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">🔋 {total_cells}</div>
            <div class="metric-title">Total Cells</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">⚡ {avg_voltage:.2f}V</div>
            <div class="metric-title">Avg Voltage</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">🌡️ {avg_temp:.1f}°C</div>
            <div class="metric-title">Avg Temperature</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        warning_color = "var(--danger-color)" if warnings_count > 0 else "var(--success-color)"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">⚠️ {warnings_count}</div>
            <div class="metric-title">Active Warnings</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Cell Status Grid
    st.markdown("## 📱 Live Cell Monitoring")
    
    cols = st.columns(2)
    for idx, (cell_key, cell_data) in enumerate(st.session_state.cells_data.items()):
        with cols[idx % 2]:
            specs = get_cell_specs(cell_data.get("cell_type", cell_data.get("type", "NMC")))
            charge_pct = calculate_charge_percentage(
                cell_data["voltage"], 
                cell_data["min_voltage"], 
                cell_data["max_voltage"]
            )
            warnings = get_safety_status(cell_data)
            temp = cell_data.get("temp", cell_data.get("temperature", 25))
            
            status_class = "status-normal"
            if warnings:
                status_class = "status-warning" if len(warnings) <= 2 else "status-critical"
            
            favorite_icon = "⭐" if cell_key in st.session_state.favorites else "🤍"
            cell_type_class = cell_data.get('cell_type', 'NMC').lower()
            
            st.markdown(f"""
            <div class="cell-card bounce-in">
                <div class="cell-header {cell_type_class}">
                    <div class="cell-info">
                        <div class="cell-avatar">
                            {cell_data.get('cell_type', 'NMC')[:2]}
                        </div>
                        <div>
                            <div class="cell-name">{cell_key}</div>
                            <div class="cell-type">{cell_data.get('cell_type', 'NMC')} • {cell_data.get('status', 'Idle')}</div>
                        </div>
                        <div style="margin-left: auto; font-size: 1.5rem;">
                            {favorite_icon}
                        </div>
                    </div>
                </div>
                
                <div class="cell-content">
                    <div class="cell-metrics">
                        <div class="metric-item">
                            <div class="metric-value">⚡ {cell_data['voltage']:.2f}V</div>
                            <div class="metric-label">Voltage</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">🔄 {cell_data['current']:.2f}A</div>
                            <div class="metric-label">Current</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">🌡️ {temp:.1f}°C</div>
                            <div class="metric-label">Temperature</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">🔋 {charge_pct:.1f}%</div>
                            <div class="metric-label">Charge</div>
                        </div>
                    </div>
                    
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {charge_pct}%;"></div>
                    </div>
                    
                    <div class="status-indicator {status_class}">
                        {"⚠️ " + ", ".join(warnings) if warnings else "✅ All systems normal"}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"💖 {'Remove from' if cell_key in st.session_state.favorites else 'Add to'} Favorites", 
                        key=f"fav_{cell_key}", use_container_width=True):
                if cell_key in st.session_state.favorites:
                    st.session_state.favorites.remove(cell_key)
                else:
                    st.session_state.favorites.append(cell_key)
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Setup Page
def render_setup():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-card">
        <h2>🔧 Cell Configuration Setup</h2>
        <p>Configure and manage your battery cells (LFP, NMC, LTO)</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="content-card slide-in-left">
            <h3>➕ Add New Cell</h3>
        </div>
        """, unsafe_allow_html=True)
        
        cell_name = st.text_input("Cell Name", placeholder="e.g., Cell_001")
        cell_type = st.selectbox("Cell Type", ["LFP", "NMC", "LTO"])
        
        # Display cell specifications
        if cell_type:
            specs = get_cell_specs(cell_type)
            st.info(f"""
            **{cell_type} Specifications:**
            - Nominal Voltage: {specs['voltage']}V
            - Min Voltage: {specs['min_voltage']}V  
            - Max Voltage: {specs['max_voltage']}V
            """)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🚀 Add Cell", type="primary", use_container_width=True):
                if cell_name and cell_name not in st.session_state.cells_data:
                    st.session_state.cells_data[cell_name] = create_cell(cell_type, cell_name)
                    st.success(f"✅ Cell '{cell_name}' added successfully!")
                    st.rerun()
                elif cell_name in st.session_state.cells_data:
                    st.error("❌ Cell name already exists!")
                else:
                    st.error("❌ Please enter a cell name!")
        
        with col_b:
            if st.button("🗑️ Clear All", use_container_width=True):
                st.session_state.cells_data = {}
                st.session_state.favorites = []
                st.session_state.temp_history = {}
                st.success("🗑️ All cells cleared!")
                st.rerun()
    
    with col2:
        st.markdown("""
        <div class="content-card slide-in-left">
            <h3>🔄 Bulk Operations</h3>
        </div>
        """, unsafe_allow_html=True)
        
        num_cells = st.number_input("Number of Cells", min_value=1, max_value=20, value=3)
        prefix = st.text_input("Cell Prefix", value="Cell")
        bulk_type = st.selectbox("Bulk Cell Type", ["LFP", "NMC", "LTO"], key="bulk")
        
        if st.button("⚡ Create Multiple Cells", use_container_width=True):
            created_count = 0
            for i in range(num_cells):
                cell_name = f"{prefix}_{i+1:03d}"
                if cell_name not in st.session_state.cells_data:
                    st.session_state.cells_data[cell_name] = create_cell(bulk_type, cell_name)
                    created_count += 1
            st.success(f"✅ Created {created_count} cells successfully!")
            st.rerun()
    
    # Current Configuration
    if st.session_state.cells_data:
        st.markdown("## 📱 Current Configuration")
        
        # Create DataFrame for better display
        config_data = []
        for cell_name, cell_data in st.session_state.cells_data.items():
            config_data.append({
                "Cell Name": cell_name,
                "Type": cell_data.get('cell_type', 'Unknown'),
                "Voltage (V)": f"{cell_data['voltage']:.2f}",
                "Min Voltage (V)": f"{cell_data['min_voltage']:.2f}",
                "Max Voltage (V)": f"{cell_data['max_voltage']:.2f}",
                "Temperature (°C)": f"{cell_data.get('temp', 25):.1f}",
                "Status": cell_data.get('status', 'Idle'),
                "Health (%)": f"{cell_data.get('health', 100):.1f}",
                "Favorite": "⭐" if cell_name in st.session_state.favorites else "☆"
            })
        
        config_df = pd.DataFrame(config_data)
        st.dataframe(config_df, use_container_width=True, height=300)
        
        # Bulk operations
        st.markdown("### 🔧 Bulk Operations")
        selected_cells = st.multiselect("Select Cells for Bulk Operations", 
                                      list(st.session_state.cells_data.keys()))
        
        if selected_cells:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🗑️ Remove Selected", use_container_width=True):
                    for cell in selected_cells:
                        if cell in st.session_state.cells_data:
                            del st.session_state.cells_data[cell]
                        if cell in st.session_state.favorites:
                            st.session_state.favorites.remove(cell)
                    st.success(f"Removed {len(selected_cells)} cells")
                    st.rerun()
            
            with col2:
                if st.button("⭐ Add to Favorites", use_container_width=True):
                    for cell in selected_cells:
                        if cell not in st.session_state.favorites:
                            st.session_state.favorites.append(cell)
                    st.success(f"Added {len(selected_cells)} cells to favorites")
                    st.rerun()
            
            with col3:
                if st.button("💔 Remove from Favorites", use_container_width=True):
                    for cell in selected_cells:
                        if cell in st.session_state.favorites:
                            st.session_state.favorites.remove(cell)
                    st.success(f"Removed {len(selected_cells)} cells from favorites")
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Control Panel Page
def render_control_panel():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    if not st.session_state.cells_data:
        st.markdown("""
        <div class="content-card">
            <h3>⚠️ No cells configured</h3>
            <p>Please setup cells first in the Setup section!</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    st.markdown("""
    <div class="content-card">
        <h2>🎛️ Control Panel</h2>
        <p>Advanced Cell Control & System Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # System Controls
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="content-card slide-in-left">
            <h3>🔌 Individual Cell Control</h3>
        </div>
        """, unsafe_allow_html=True)
        
        selected_cell = st.selectbox("Select Cell", list(st.session_state.cells_data.keys()))
        
        if selected_cell:
            cell = st.session_state.cells_data[selected_cell]
            specs = get_cell_specs(cell.get("cell_type", "NMC"))
            
            st.markdown(f"**Current Status:** {cell.get('status', 'Idle')}")
            
            # Parameter controls
            new_voltage = st.slider("Voltage (V)", 
                                   float(cell['min_voltage']), 
                                   float(cell['max_voltage']), 
                                   float(cell['voltage']), 
                                   0.01)
            new_current = st.slider("Current (A)", -10.0, 10.0, float(cell['current']), 0.1)
            temp = cell.get("temp", 25)
            new_temp = st.slider("Temperature (°C)", 0.0, 80.0, float(temp), 0.1)
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("📝 Update Parameters", use_container_width=True):
                    st.session_state.cells_data[selected_cell]['voltage'] = new_voltage
                    st.session_state.cells_data[selected_cell]['current'] = new_current
                    st.session_state.cells_data[selected_cell]['temp'] = new_temp
                    st.session_state.cells_data[selected_cell]['temperature'] = new_temp
                    st.session_state.cells_data[selected_cell]['capacity'] = round(new_voltage * abs(new_current), 2)
                    st.success("✅ Parameters updated!")
                    st.rerun()
            
            with col_b:
                if st.button("🔄 Reset Cell", use_container_width=True):
                    st.session_state.cells_data[selected_cell]['voltage'] = specs['voltage']
                    st.session_state.cells_data[selected_cell]['current'] = 0.0
                    st.session_state.cells_data[selected_cell]['temp'] = 25.0
                    st.session_state.cells_data[selected_cell]['temperature'] = 25.0
                    st.session_state.cells_data[selected_cell]['status'] = 'Idle'
                    st.success("🔄 Cell reset!")
                    st.rerun()
    
    with col2:
        st.markdown("""
        <div class="content-card">
            <h3>🚨 System Control</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Stress test mode
        stress_text = "🛑 Disable Stress Test" if st.session_state.stress_test_mode else "🔥 Enable Stress Test"
        
        if st.button(stress_text, use_container_width=True):
            st.session_state.stress_test_mode = not st.session_state.stress_test_mode
            if st.session_state.stress_test_mode:
                st.warning("⚠️ Stress test mode enabled!")
                for cell_name in st.session_state.cells_data:
                    cell = st.session_state.cells_data[cell_name]
                    cell['current'] = random.uniform(7, 9)
                    temp_val = random.uniform(45, 60)
                    cell['temp'] = temp_val
                    cell['temperature'] = temp_val
                    cell['status'] = 'Stress Testing'
            else:
                st.success("✅ Stress test mode disabled.")
                for cell_name in st.session_state.cells_data:
                    cell = st.session_state.cells_data[cell_name]
                    cell['current'] = 0.0
                    temp_val = random.uniform(25, 35)
                    cell['temp'] = temp_val
                    cell['temperature'] = temp_val
                    cell['status'] = 'Idle'
            st.rerun()
        
        # Emergency controls - FIXED
        st.markdown('<div class="emergency-button">', unsafe_allow_html=True)
        if st.button("🚨 Emergency Shutdown", key="control_emergency", use_container_width=True):
            emergency_stop()
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.emergency_stop:
            st.markdown('<div class="emergency-button">', unsafe_allow_html=True)
            if st.button("🔄 Reset Emergency State", key="control_reset_emergency", use_container_width=True):
                st.session_state.emergency_stop = False
                for cell_name in st.session_state.cells_data:
                    cell = st.session_state.cells_data[cell_name]
                    cell['status'] = 'Idle'
                st.success("✅ Emergency state reset.")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Task Processes Page
def render_task_processes():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    if not st.session_state.cells_data:
        st.markdown("""
        <div class="content-card">
            <h3>⚠️ No cells configured</h3>
            <p>Please setup cells first in the Setup section!</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    st.markdown("""
    <div class="content-card">
        <h2>⚙️ Task Processes</h2>
        <p>Automated Task Management & Execution Timeline</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="content-card slide-in-left">
            <h3>➕ Create New Task</h3>
        </div>
        """, unsafe_allow_html=True)
        
        task_name = st.text_input("Task Name", placeholder="e.g., Charging_Cycle_1")
        target_cells = st.multiselect("Target Cells", list(st.session_state.cells_data.keys()))
        task_type = st.selectbox("Task Type", ["CC_CV", "CC_CD", "IDLE", "BALANCE", "STRESS_TEST"])
        
        # Task parameters based on type
        task_params = {}
        
        if task_type == "CC_CV":
            st.markdown("**Constant Current - Constant Voltage Parameters**")
            task_params['voltage'] = st.number_input("Target Voltage (V)", 0.0, 5.0, 4.0, 0.1)
            task_params['current'] = st.number_input("Charging Current (A)", 0.1, 10.0, 2.0, 0.1)
            task_params['duration'] = st.number_input("Duration (minutes)", 1, 1440, 60)
            
        elif task_type == "CC_CD":
            st.markdown("**Constant Current - Constant Discharge Parameters**")
            task_params['current'] = st.number_input("Discharge Current (A)", 0.1, 10.0, 2.0, 0.1)
            task_params['cutoff_voltage'] = st.number_input("Cutoff Voltage (V)", 2.0, 4.0, 2.5, 0.1)
            task_params['duration'] = st.number_input("Max Duration (minutes)", 1, 1440, 60)
            
        elif task_type == "IDLE":
            st.markdown("**Idle Parameters**")
            task_params['duration'] = st.number_input("Idle Duration (minutes)", 1, 1440, 30)
            
        elif task_type == "BALANCE":
            st.markdown("**Cell Balancing Parameters**")
            task_params['target_voltage'] = st.number_input("Target Voltage (V)", 3.0, 4.2, 3.6, 0.1)
            task_params['balance_current'] = st.number_input("Balance Current (A)", 0.1, 2.0, 0.5, 0.1)
            
        elif task_type == "STRESS_TEST":
            st.markdown("**Stress Test Parameters**")
            task_params['max_current'] = st.number_input("Max Current (A)", 5.0, 15.0, 8.0, 0.1)
            task_params['max_temp'] = st.number_input("Max Temperature (°C)", 45.0, 70.0, 55.0, 1.0)
            task_params['duration'] = st.number_input("Test Duration (minutes)", 1, 60, 10)
        
        # Priority and scheduling
        task_priority = st.selectbox("Priority", ["Low", "Normal", "High", "Critical"])
        
        if st.button("➕ Add Task to Queue", use_container_width=True):
            if task_name and target_cells:
                new_task = {
                    'name': task_name,
                    'type': task_type,
                    'cells': target_cells,
                    'parameters': task_params,
                    'priority': task_priority,
                    'status': 'Queued',
                    'created_at': datetime.now(),
                    'progress': 0,
                    'estimated_duration': task_params.get('duration', 30)
                }
                
                st.session_state.task_queue.append(new_task)
                st.success(f"✅ Task '{task_name}' added to queue!")
                st.rerun()
            else:
                st.error("❌ Please fill in task name and select target cells!")
    
    with col2:
        st.markdown("""
        <div class="content-card">
            <h3>📋 Task Queue & Timeline</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Task execution controls
        col_a, col_b = st.columns(2)
        with col_a:
            auto_execute = st.checkbox("🔄 Auto-execute", value=False)
        with col_b:
            if st.button("⏸️ Pause All" if st.session_state.task_running else "▶️ Resume All", 
                        use_container_width=True):
                st.session_state.task_running = not st.session_state.task_running
                st.rerun()
        
        # Task queue display with timeline
        if st.session_state.task_queue:
            st.markdown('<div class="timeline">', unsafe_allow_html=True)
            
            for idx, task in enumerate(st.session_state.task_queue):
                status_colors = {
                    "Queued": "#ffd43b",
                    "Running": "#51cf66",
                    "Completed": "#00d4ff",
                    "Failed": "#ff6b6b",
                    "Paused": "#868e96"
                }
                
                status_icons = {
                    "Queued": "🟡", 
                    "Running": "🟢", 
                    "Completed": "✅", 
                    "Failed": "❌",
                    "Paused": "⏸️"
                }
                
                # Calculate estimated completion time
                est_completion = task['created_at'] + timedelta(minutes=task.get('estimated_duration', 30))
                
                st.markdown(f"""
                <div class="timeline-item">
                    <div class="timeline-marker" style="background: {status_colors.get(task['status'], '#00d4ff')};"></div>
                    <div class="timeline-content">
                        <h4>{status_icons.get(task['status'], '⚪')} {task['name']}</h4>
                        <p><strong>Type:</strong> {task['type']} | <strong>Priority:</strong> {task['priority']}</p>
                        <p><strong>Cells:</strong> {', '.join(task['cells'])}</p>
                        <p><strong>Status:</strong> {task['status']} | <strong>Progress:</strong> {task['progress']}%</p>
                        <p><strong>Est. Completion:</strong> {est_completion.strftime('%H:%M:%S')}</p>
                        <div class="progress-container">
                            <div class="progress-bar" style="width: {task['progress']}%;"></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Task controls
                if task['status'] == 'Queued':
                    col_x, col_y, col_z = st.columns(3)
                    with col_x:
                        if st.button(f"▶️ Start", key=f"start_{idx}", use_container_width=True):
                            task['status'] = 'Running'
                            task['started_at'] = datetime.now()
                            st.session_state.task_running = True
                            st.rerun()
                    with col_y:
                        if st.button(f"⬆️ Priority", key=f"priority_{idx}", use_container_width=True):
                            # Move task up in queue
                            if idx > 0:
                                st.session_state.task_queue[idx], st.session_state.task_queue[idx-1] = \
                                st.session_state.task_queue[idx-1], st.session_state.task_queue[idx]
                            st.rerun()
                    with col_z:
                        if st.button(f"🗑️ Remove", key=f"remove_task_{idx}", use_container_width=True):
                            st.session_state.task_queue.pop(idx)
                            st.rerun()
                
                elif task['status'] == 'Running':
                    col_x, col_y = st.columns(2)
                    with col_x:
                        if st.button(f"⏸️ Pause", key=f"pause_{idx}", use_container_width=True):
                            task['status'] = 'Paused'
                            st.rerun()
                    with col_y:
                        if st.button(f"🛑 Stop", key=f"stop_{idx}", use_container_width=True):
                            task['status'] = 'Completed'
                            task['progress'] = 100
                            st.session_state.task_running = False
                            st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="content-card">
                <h4>ℹ️ No tasks in queue</h4>
                <p>Create a task to get started with automated processes!</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Task execution simulation
    if st.session_state.task_running and st.session_state.task_queue:
        current_task = None
        for task in st.session_state.task_queue:
            if task['status'] == 'Running':
                current_task = task
                break
        
        if current_task:
            # Simulate progress
            progress_increment = random.randint(2, 5)
            current_task['progress'] = min(100, current_task['progress'] + progress_increment)
            
            # Update cell parameters based on task
            for cell_name in current_task['cells']:
                if cell_name in st.session_state.cells_data:
                    cell = st.session_state.cells_data[cell_name]
                    cell['status'] = f"Running {current_task['type']}"
                    
                    # Simulate task effects
                    if current_task['type'] == 'CC_CV':
                        cell['current'] = current_task['parameters'].get('current', 2.0)
                        cell['voltage'] = min(cell['max_voltage'], 
                                            cell['voltage'] + 0.005 * (current_task['progress'] / 100))
                    elif current_task['type'] == 'CC_CD':
                        cell['current'] = -current_task['parameters'].get('current', 2.0)
                        cell['voltage'] = max(cell['min_voltage'], 
                                            cell['voltage'] - 0.005 * (current_task['progress'] / 100))
                    elif current_task['type'] == 'STRESS_TEST':
                        cell['current'] = random.uniform(6, current_task['parameters'].get('max_current', 8))
                        temp_val = random.uniform(40, current_task['parameters'].get('max_temp', 55))
                        cell['temp'] = temp_val
                        cell['temperature'] = temp_val
                    elif current_task['type'] == 'BALANCE':
                        target_voltage = current_task['parameters'].get('target_voltage', 3.6)
                        if abs(cell['voltage'] - target_voltage) > 0.01:
                            cell['current'] = 0.5 if cell['voltage'] < target_voltage else -0.5
                            cell['voltage'] += 0.002 if cell['voltage'] < target_voltage else -0.002
                        else:
                            cell['current'] = 0.0
                    elif current_task['type'] == 'IDLE':
                        cell['current'] = 0.0
                        # Slight temperature drift towards ambient
                        cell['temp'] = max(20, min(40, cell['temp'] + random.uniform(-0.5, 0.5)))
                        cell['temperature'] = cell['temp']
            
            # Check if task completed
            if current_task['progress'] >= 100:
                current_task['status'] = 'Completed'
                current_task['completed_at'] = datetime.now()
                st.session_state.task_running = False
                
                # Reset cell status
                for cell_name in current_task['cells']:
                    if cell_name in st.session_state.cells_data:
                        st.session_state.cells_data[cell_name]['status'] = 'Idle'
                        st.session_state.cells_data[cell_name]['current'] = 0.0
                
                # Add to process history
                st.session_state.process_history.append({
                    'task': current_task,
                    'completed_at': datetime.now(),
                    'cells_data': dict(st.session_state.cells_data)
                })
                
                st.success(f"✅ Task '{current_task['name']}' completed!")
                
                # Auto-start next task if enabled
                if auto_execute:
                    time.sleep(1)
                    st.rerun()
            else:
                if st.session_state.auto_refresh:
                    time.sleep(2)
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Analytics Page
def render_analytics():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    if not st.session_state.cells_data:
        st.markdown("""
        <div class="content-card">
            <h3>⚠️ No cells configured</h3>
            <p>Please setup cells first in the Setup section!</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    st.markdown("""
    <div class="content-card">
        <h2>📊 Analytics & Data Insights</h2>
        <p>Advanced Visualization & Performance Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Real-time Charts
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Real-time Monitoring", "📊 Performance Analysis", "📋 Process History", "💾 Data Export"])
    
    with tab1:
        # Temperature History Chart
        if st.session_state.temp_history:
            st.markdown("""
            <div class="chart-container">
                <h3>🌡️ Temperature Monitoring</h3>
            </div>
            """, unsafe_allow_html=True)
            
            fig_temp = go.Figure()
            
            for cell_key, history in st.session_state.temp_history.items():
                if cell_key in st.session_state.cells_data and history["time"] and history["temp"]:
                    specs = get_cell_specs(st.session_state.cells_data[cell_key].get("cell_type", "NMC"))
                    fig_temp.add_trace(go.Scatter(
                        x=history["time"],
                        y=history["temp"],
                        mode='lines+markers',
                        name=cell_key,
                        line=dict(width=3, color=specs["color"]),
                        marker=dict(size=6),
                        hovertemplate='<b>%{fullData.name}</b><br>Time: %{x}<br>Temperature: %{y:.1f}°C<extra></extra>'
                    ))
            
            theme_template = "plotly_white" if st.session_state.theme == 'light' else "plotly_dark"
            fig_temp.update_layout(
                title="📈 Real-time Temperature Monitoring",
                xaxis_title="Time",
                yaxis_title="Temperature (°C)",
                template=theme_template,
                height=500,
                hovermode='x unified',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)' if st.session_state.theme == 'dark' else 'rgba(255,255,255,0.8)',
                font=dict(family="Inter, sans-serif")
            )
            
            st.plotly_chart(fig_temp, use_container_width=True)
        
        # Live Voltage and Current Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Voltage Chart
            cells = list(st.session_state.cells_data.keys())
            voltages = [st.session_state.cells_data[cell]["voltage"] for cell in cells]
            
            fig_voltage = go.Figure(data=[
                go.Bar(
                    x=cells,
                    y=voltages,
                    marker_color='#00d4ff',
                    text=[f"{v:.2f}V" for v in voltages],
                    textposition='auto',
                )
            ])
            
            theme_template = "plotly_white" if st.session_state.theme == 'light' else "plotly_dark"
            fig_voltage.update_layout(
                title="⚡ Voltage Comparison",
                xaxis_title="Cells",
                yaxis_title="Voltage (V)",
                template=theme_template,
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)' if st.session_state.theme == 'dark' else 'rgba(255,255,255,0.8)'
            )
            
            st.plotly_chart(fig_voltage, use_container_width=True)
        
        with col2:
            # Current Chart
            currents = [st.session_state.cells_data[cell]["current"] for cell in cells]
            
            fig_current = go.Figure(data=[
                go.Bar(
                    x=cells,
                    y=currents,
                    marker_color='#51cf66',
                    text=[f"{c:.2f}A" for c in currents],
                    textposition='auto',
                )
            ])
            
            fig_current.update_layout(
                title="🔄 Current Comparison",
                xaxis_title="Cells",
                yaxis_title="Current (A)",
                template=theme_template,
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)' if st.session_state.theme == 'dark' else 'rgba(255,255,255,0.8)'
            )
            
            st.plotly_chart(fig_current, use_container_width=True)
        
        # Cell Status Distribution
        status_counts = {}
        for cell_data in st.session_state.cells_data.values():
            status = cell_data.get('status', 'Idle')
            status_counts[status] = status_counts.get(status, 0) + 1
        
        fig_status = go.Figure(data=[
            go.Pie(
                labels=list(status_counts.keys()),
                values=list(status_counts.values()),
                hole=0.3,
                marker_colors=['#00d4ff', '#51cf66', '#ff6b6b', '#ffd43b', '#ff8cc8']
            )
        ])
        
        fig_status.update_layout(
            title="📊 Cell Status Distribution",
            template=theme_template,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif")
        )
        
        st.plotly_chart(fig_status, use_container_width=True)
    
    with tab2:
        # Performance Analytics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔋 Cell Health Analysis")
            
            health_data = [(name, cell.get('health', 100)) for name, cell in st.session_state.cells_data.items()]
            health_df = pd.DataFrame(health_data, columns=['Cell', 'Health'])
            
            fig_health = px.bar(
                health_df, x='Cell', y='Health',
                title="Cell Health Status",
                color='Health',
                color_continuous_scale='RdYlGn',
                range_color=[0, 100]
            )
            theme_template = "plotly_white" if st.session_state.theme == 'light' else "plotly_dark"
            fig_health.update_layout(
                template=theme_template,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)' if st.session_state.theme == 'dark' else 'rgba(255,255,255,0.8)'
            )
            st.plotly_chart(fig_health, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Voltage Distribution")
            
            voltage_data = [cell['voltage'] for cell in st.session_state.cells_data.values()]
            
            fig_voltage_dist = go.Figure(data=[
                go.Histogram(
                    x=voltage_data,
                    nbinsx=15,
                    marker_color='#00d4ff',
                    opacity=0.7
                )
            ])
            fig_voltage_dist.update_layout(
                title="Voltage Distribution",
                xaxis_title="Voltage (V)",
                yaxis_title="Count",
                template=theme_template,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)' if st.session_state.theme == 'dark' else 'rgba(255,255,255,0.8)'
            )
            st.plotly_chart(fig_voltage_dist, use_container_width=True)
        
        # Cell Type Performance Comparison
        st.markdown("### 🔬 Cell Type Performance Comparison")
        
        type_performance = {}
        for cell_name, cell_data in st.session_state.cells_data.items():
            cell_type = cell_data.get('cell_type', 'Unknown')
            if cell_type not in type_performance:
                type_performance[cell_type] = {
                    'count': 0,
                    'avg_voltage': 0,
                    'avg_temp': 0,
                    'avg_health': 0
                }
            
            type_performance[cell_type]['count'] += 1
            type_performance[cell_type]['avg_voltage'] += cell_data['voltage']
            type_performance[cell_type]['avg_temp'] += cell_data.get('temp', 25)
            type_performance[cell_type]['avg_health'] += cell_data.get('health', 100)
        
        # Calculate averages
        for cell_type in type_performance:
            count = type_performance[cell_type]['count']
            if count > 0:
                type_performance[cell_type]['avg_voltage'] /= count
                type_performance[cell_type]['avg_temp'] /= count
                type_performance[cell_type]['avg_health'] /= count
        
        if type_performance:
            perf_data = []
            for cell_type, data in type_performance.items():
                perf_data.append({
                    'Type': cell_type,
                    'Count': data['count'],
                    'Avg Voltage (V)': f"{data['avg_voltage']:.2f}",
                    'Avg Temperature (°C)': f"{data['avg_temp']:.1f}",
                    'Avg Health (%)': f"{data['avg_health']:.1f}"
                })
            
            perf_df = pd.DataFrame(perf_data)
            st.dataframe(perf_df, use_container_width=True)
    
    with tab3:
        st.markdown("### 📋 Process History & Timeline")
        
        if st.session_state.process_history:
            # Process timeline
            timeline_data = []
            for idx, process in enumerate(st.session_state.process_history):
                task = process['task']
                timeline_data.append({
                    'Task': task['name'],
                    'Type': task['type'],
                    'Start': task.get('started_at', task['created_at']),
                    'End': process['completed_at'],
                    'Duration': (process['completed_at'] - task.get('started_at', task['created_at'])).total_seconds() / 60,
                    'Cells': len(task['cells'])
                })
            
            timeline_df = pd.DataFrame(timeline_data)
            
            # Process statistics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_processes = len(st.session_state.process_history)
                st.metric("Total Processes", total_processes)
            
            with col2:
                avg_duration = np.mean(timeline_df['Duration']) if not timeline_df.empty else 0
                st.metric("Avg Duration", f"{avg_duration:.1f} min")
            
            with col3:
                total_cells_processed = sum(timeline_df['Cells']) if not timeline_df.empty else 0
                st.metric("Cells Processed", total_cells_processed)
            
            # Detailed process history
            st.markdown("### 📊 Detailed Process Log")
            
            for idx, process in enumerate(reversed(st.session_state.process_history[-5:])):  # Show last 5
                with st.expander(f"📋 {process['task']['name']} - {process['completed_at'].strftime('%Y-%m-%d %H:%M')}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Task Details:**")
                        st.write(f"**Type:** {process['task']['type']}")
                        st.write(f"**Priority:** {process['task'].get('priority', 'Normal')}")
                        st.write(f"**Target Cells:** {', '.join(process['task']['cells'])}")
                    
                    with col2:
                        st.markdown("**Results:**")
                        st.write(f"**Duration:** {process['task'].get('estimated_duration', 'N/A')} minutes")
                        st.write(f"**Completed:** {process['completed_at'].strftime('%Y-%m-%d %H:%M:%S')}")
                        
                        if 'cells_data' in process:
                            st.markdown("**Final Cell States:**")
                            for cell_name in process['task']['cells']:
                                if cell_name in process['cells_data']:
                                    cell = process['cells_data'][cell_name]
                                    temp = cell.get("temp", cell.get("temperature", 25))
                                    st.write(f"- {cell_name}: {cell['voltage']:.2f}V, {temp:.1f}°C")
        else:
            st.markdown("""
            <div class="content-card">
                <h4>ℹ️ No process history available yet</h4>
                <p>Complete some tasks to see history here!</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 💾 Data Export & Reporting")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📥 Export Current Data")
            
            if st.session_state.cells_data:
                # Current cell data
                export_df = pd.DataFrame.from_dict(st.session_state.cells_data, orient='index')
                export_df['timestamp'] = datetime.now()
                
                csv_data = export_df.to_csv(index=True)
                st.download_button(
                    label="📥 Download Cell Data (CSV)",
                    data=csv_data,
                    file_name=f"cell_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                # JSON export
                json_data = json.dumps(st.session_state.cells_data, indent=2, default=str)
                st.download_button(
                    label="📥 Download Cell Data (JSON)",
                    data=json_data,
                    file_name=f"cell_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            else:
                st.info("No cell data to export.")
        
        with col2:
            st.markdown("#### 📋 Export Process Data")
            
            if st.session_state.process_history:
                # Process history
                history_data = []
                for process in st.session_state.process_history:
                    task = process['task']
                    history_data.append({
                        'Task_Name': task['name'],
                        'Task_Type': task['type'],
                        'Priority': task.get('priority', 'Normal'),
                        'Target_Cells': ', '.join(task['cells']),
                        'Created_At': task['created_at'],
                        'Completed_At': process['completed_at'],
                        'Duration_Minutes': task.get('estimated_duration', 0),
                        'Parameters': json.dumps(task['parameters'])
                    })
                
                history_df = pd.DataFrame(history_data)
                history_csv = history_df.to_csv(index=False)
                
                st.download_button(
                    label="📥 Download Process History (CSV)",
                    data=history_csv,
                    file_name=f"process_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                # Temperature history export
                if st.session_state.temp_history:
                    temp_export_data = []
                    for cell_name, history in st.session_state.temp_history.items():
                        for time_point, temp_value in zip(history['time'], history['temp']):
                            temp_export_data.append({
                                'Cell': cell_name,
                                'Timestamp': time_point,
                                'Temperature': temp_value
                            })
                    
                    temp_df = pd.DataFrame(temp_export_data)
                    temp_csv = temp_df.to_csv(index=False)
                    
                    st.download_button(
                        label="📥 Download Temperature History (CSV)",
                        data=temp_csv,
                        file_name=f"temperature_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            else:
                st.info("No process history to export.")
        
        # System Report Generation
        st.markdown("#### 📊 System Report")
        
        if st.button("📊 Generate System Report", use_container_width=True):
            # Calculate performance metrics
            if st.session_state.cells_data:
                voltages = [cell["voltage"] for cell in st.session_state.cells_data.values()]
                currents = [cell["current"] for cell in st.session_state.cells_data.values()]
                temps = [cell.get("temp", 25) for cell in st.session_state.cells_data.values()]
                healths = [cell.get("health", 100) for cell in st.session_state.cells_data.values()]
                
                report_data = {
                    'system_overview': {
                        'total_cells': len(st.session_state.cells_data),
                        'cell_types': list(set(cell.get('cell_type', 'Unknown') for cell in st.session_state.cells_data.values())),
                        'avg_voltage': f"{np.mean(voltages):.3f}V",
                        'voltage_range': f"{np.min(voltages):.3f}V - {np.max(voltages):.3f}V",
                        'avg_temperature': f"{np.mean(temps):.1f}°C",
                        'temp_range': f"{np.min(temps):.1f}°C - {np.max(temps):.1f}°C",
                        'avg_health': f"{np.mean(healths):.1f}%",
                        'active_warnings': sum(len(get_safety_status(cell)) for cell in st.session_state.cells_data.values()),
                        'report_generated': datetime.now().isoformat()
                    },
                    'task_summary': {
                        'total_tasks_completed': len(st.session_state.process_history),
                        'tasks_in_queue': len(st.session_state.task_queue),
                        'task_types_used': list(set(task['type'] for task in st.session_state.process_history)) if st.session_state.process_history else []
                    },
                    'cells_detail': st.session_state.cells_data,
                    'favorites': st.session_state.favorites
                }
                
                report_json = json.dumps(report_data, indent=2, default=str)
                st.download_button(
                    label="📋 Download System Report",
                    data=report_json,
                    file_name=f"system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
                
                st.success("✅ System report generated successfully!")
                
                # Display summary
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Cells", len(st.session_state.cells_data))
                with col2:
                    st.metric("Avg Voltage", f"{np.mean(voltages):.2f}V")
                with col3:
                    st.metric("Avg Health", f"{np.mean(healths):.1f}%")
                with col4:
                    st.metric("Completed Tasks", len(st.session_state.process_history))
            else:
                st.warning("No data available for report generation.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main Application Logic - FIXED
def main():
    # Initialize the application
    initialize_app()
    
    # Render sidebar navigation
    render_sidebar()
    
    # Render main header
    render_header()
    
    # Auto-refresh logic
    if st.session_state.auto_refresh and st.session_state.cells_data and not st.session_state.emergency_stop:
        for cell_key in st.session_state.cells_data:
            update_cell_real_time(cell_key)
        update_temp_history()
    
    # Page routing - FIXED
    if st.session_state.current_page == "Dashboard":
        render_dashboard()
    elif st.session_state.current_page == "Setup":
        render_setup()
    elif st.session_state.current_page == "Control Panel":
        render_control_panel()
    elif st.session_state.current_page == "Task Processes":
        render_task_processes()
    elif st.session_state.current_page == "Analytics":
        render_analytics()
    
    # Emergency stop overlay - FIXED
    if st.session_state.emergency_stop:
        st.markdown("""
        <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(255, 107, 107, 0.95); 
                    z-index: 9999; display: flex; align-items: center; justify-content: center; 
                    backdrop-filter: blur(10px);">
            <div style="text-align: center; color: white; background: rgba(0,0,0,0.8); 
                        padding: 3rem; border-radius: 20px; border: 2px solid #ff6b6b;">
                <h1 style="font-size: 3rem; margin: 0 0 1rem 0;">🚨 EMERGENCY STOP</h1>
                <h2 style="margin: 0 0 1rem 0;">System Shutdown Activated</h2>
                <p style="font-size: 1.2rem; margin: 0;">All operations have been halted for safety.</p>
                <p style="font-size: 1rem; margin: 1rem 0 0 0; opacity: 0.8;">Use the sidebar to reset the emergency state.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Auto-refresh for real-time updates - FIXED
    if (st.session_state.auto_refresh and 
        not st.session_state.emergency_stop and 
        (st.session_state.current_page == "Dashboard" or 
         (st.session_state.current_page == "Task Processes" and st.session_state.task_running))):
        time.sleep(3)
        st.rerun()

# Run the application
if __name__ == "__main__":
    main()
