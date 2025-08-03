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

# MUST be the first Streamlit command
st.set_page_config(
    page_title="⚡ BatteryFlow Pro",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_modern_css(theme_mode="dark"):
    if theme_mode == "light":
        css_vars = """
        :root {
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
        """
    else:
        css_vars = """
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
        }
        """
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    {css_vars}
    
    :root {{
        --primary-color: #00d4ff;
        --secondary-color: #0099cc;
        --accent-color: #ff6b6b;
        --success-color: #51cf66;
        --warning-color: #ffd43b;
        --danger-color: #ff6b6b;
        --gradient-primary: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        --gradient-danger: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        --gradient-success: linear-gradient(135deg, #51cf66 0%, #40c057 100%);
        --border-radius: 12px;
        --border-radius-lg: 16px;
    }}
    
    .stApp {{
        background: var(--bg-primary);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stDeployButton {{display: none;}}
    
    /* Main sidebar container */
    .css-1d391kg {{
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-color) !important;
        transition: all 0.3s ease !important;
    }}
    
    /* Sidebar content area */
    .css-1cypcdb {{
        background: var(--bg-secondary) !important;
        padding: 1rem !important;
    }}
    
    /* Sidebar inner content */
    .css-1lcbmhc {{
        background: transparent !important;
        padding: 0 !important;
    }}
    
    /* Ensure sidebar is always accessible */
    .stSidebar {{
        min-width: 21rem !important;
        max-width: 21rem !important;
        background: var(--bg-secondary) !important;
        z-index: 999 !important;
    }}
    
    /* When sidebar is expanded */
    .stSidebar[data-testid="stSidebar"] {{
        width: 21rem !important;
        min-width: 21rem !important;
    }}
    
    /* Sidebar content wrapper */
    .stSidebar .css-1d391kg {{
        width: 100% !important;
        min-width: 100% !important;
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-color) !important;
        height: 100vh !important;
        overflow-y: auto !important;
        position: relative !important;
        z-index: 999 !important;
    }}
    
    /* Sidebar toggle button */
    .css-1rs6os {{
        background: var(--bg-tertiary) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
        border-radius: var(--border-radius) !important;
    }}
        .css-1rs6os::before {{
        content: "››" !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
    }}
    
    .stSidebar[data-testid="stSidebar"] ~ * .css-1rs6os::before {{
        content: "‹‹" !important;
    }}
    
    .css-1rs6os:hover {{
        background: var(--primary-color) !important;
        color: var(--bg-primary) !important;
    }}
    
    /* Main content adjustment when sidebar is visible */
    .main .block-container {{
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: none !important;
        transition: all 0.3s ease !important;
    }}
    
    /* Force sidebar to be accessible even when collapsed */
    .css-1544g2n {{
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-color) !important;
    }}
    
    /* Responsive sidebar for mobile */
    @media (max-width: 768px) {{
        .stSidebar {{
            min-width: 16rem !important;
            max-width: 16rem !important;
        }}
        
        .stSidebar[data-testid="stSidebar"] {{
            width: 16rem !important;
            min-width: 16rem !important;
        }}
    }}
    
    .emergency-button {{
        position: relative;
        margin: 1rem 0;
        animation: pulse-emergency 2s infinite;
    }}
    
    .emergency-button button {{
        background: var(--gradient-danger) !important;
        color: white !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.8rem 1.5rem !important;
    }}
    
    .emergency-button:hover button {{
        animation: none !important;
        transform: scale(1.05) !important;
    }}
    
    @keyframes pulse-emergency {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.8; }}
    }}
    
    .nav-button-container {{
        margin: 0.5rem 0;
    }}
    
    .nav-button-container button {{
        background: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        transition: all 0.3s ease !important;
    }}
    
    .nav-button-container button:hover {{
        background: var(--primary-color) !important;
        color: var(--bg-primary) !important;
        border-color: var(--primary-color) !important;
    }}
    
    .nav-button-active button {{
        background: var(--gradient-primary) !important;
        color: var(--bg-primary) !important;
        border-color: var(--primary-color) !important;
    }}
    
    .stSelectbox > div > div,
    .stNumberInput > div > div,
    .stTextInput > div > div,
    .stSlider > div {{
        background: var(--bg-input);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        color: var(--text-primary);
    }}
    
    .stSelectbox > div > div:focus-within,
    .stNumberInput > div > div:focus-within,
    .stTextInput > div > div:focus-within {{
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(0, 212, 255, 0.2);
    }}
    
    .main-header {{
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-lg);
        padding: 2rem;
        margin: 1rem 0 2rem 0;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow-light);
    }}
    
    .main-header::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-primary);
        border-radius: var(--border-radius-lg) var(--border-radius-lg) 0 0;
    }}
    
    .main-header h1 {{
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        font-size: 2.5rem;
        margin: 0;
        letter-spacing: -1px;
    }}
    
    .main-header p {{
        color: var(--text-secondary);
        font-weight: 400;
        margin: 1rem 0 0 0;
        font-size: 1rem;
    }}
    
    .content-card {{
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-lg);
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-light);
    }}
    
    .content-card:hover {{
        border-color: var(--border-hover);
        box-shadow: var(--shadow-medium);
    }}
    
    .content-card h2, .content-card h3 {{
        color: var(--text-primary);
        margin-top: 0;
        font-weight: 600;
    }}
    
    .welcome-card {{
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-lg);
        padding: 3rem;
        margin: 2rem 0;
        text-align: center;
        box-shadow: var(--shadow-medium);
    }}
    
    .welcome-card h2 {{
        color: var(--text-primary);
        margin-bottom: 1rem;
        font-size: 2rem;
    }}
    
    .welcome-card p {{
        color: var(--text-secondary);
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }}
    
    .cell-card {{
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-lg);
        margin: 1rem 0;
        overflow: hidden;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-light);
    }}
    
    .cell-card:hover {{
        border-color: var(--primary-color);
        box-shadow: var(--shadow-medium);
        transform: translateY(-2px);
    }}
    
    .cell-header {{
        background: var(--gradient-primary);
        color: var(--bg-primary);
        padding: 1.25rem;
        position: relative;
    }}
    
    .cell-header.lfp {{
        background: linear-gradient(135deg, #51cf66 0%, #40c057 100%);
    }}
    
    .cell-header.nmc {{
        background: linear-gradient(135deg, #339af0 0%, #228be6 100%);
    }}
    
    .cell-header.lto {{
        background: linear-gradient(135deg, #ff8cc8 0%, #ff6b6b 100%);
    }}
    
    .cell-status-charging {{
        animation: charging-pulse 2s infinite ease-in-out;
    }}
    
    @keyframes charging-pulse {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.7; transform: scale(1.05); }}
    }}
    
    .cell-status-discharging {{
        animation: discharging-fade 3s infinite ease-in-out;
    }}
    
    @keyframes discharging-fade {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.5; }}
    }}
    
    .cell-status-balancing {{
        animation: balancing-rotate 4s infinite linear;
    }}
    
    @keyframes balancing-rotate {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    .cell-status-stress {{
        animation: stress-shake 0.5s infinite ease-in-out;
    }}
    
    @keyframes stress-shake {{
        0%, 100% {{ transform: translateX(0); }}
        25% {{ transform: translateX(-2px); }}
        75% {{ transform: translateX(2px); }}
    }}
    
    .cell-info {{
        display: flex;
        align-items: center;
        gap: 1rem;
    }}
    
    .cell-avatar {{
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
    }}
    
    .cell-name {{
        font-size: 1.2rem;
        font-weight: 700;
        margin: 0;
    }}
    
    .cell-type {{
        font-size: 0.85rem;
        opacity: 0.9;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    .cell-content {{
        padding: 1.25rem;
    }}
    
    .cell-metrics {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }}
    
    .metric-item {{
        text-align: center;
        padding: 0.75rem;
        background: var(--bg-tertiary);
        border-radius: var(--border-radius);
        border: 1px solid var(--border-color);
    }}
    
    .metric-value {{
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin: 0;
        font-family: 'JetBrains Mono', monospace;
    }}
    
    .metric-label {{
        font-size: 0.75rem;
        color: var(--text-muted);
        margin: 0.25rem 0 0 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .status-indicator {{
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 500;
        font-size: 0.85rem;
        margin: 0.5rem 0;
    }}
    
    .status-normal {{
        background: var(--gradient-success);
        color: var(--bg-primary);
    }}
    
    .status-warning {{
        background: linear-gradient(135deg, var(--warning-color), #fcc419);
        color: var(--bg-primary);
    }}
    
    .status-critical {{
        background: var(--gradient-danger);
        color: var(--text-primary);
    }}
    
    .progress-container {{
        background: var(--bg-tertiary);
        border-radius: 6px;
        height: 6px;
        margin: 1rem 0;
        overflow: hidden;
    }}
    
    .progress-bar {{
        height: 100%;
        background: var(--gradient-primary);
        border-radius: 6px;
        transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .metrics-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }}
    
    .metric-card {{
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-lg);
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow-light);
    }}
    
    .metric-card:hover {{
        border-color: var(--primary-color);
        box-shadow: var(--shadow-medium);
        transform: translateY(-2px);
    }}
    
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-primary);
    }}
    
    .metric-number {{
        font-size: 2rem;
        font-weight: 800;
        color: var(--primary-color);
        margin: 0;
        font-family: 'JetBrains Mono', monospace;
    }}
    
    .metric-title {{
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin: 0.5rem 0 0 0;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 500;
    }}
    
    .timeline {{
        position: relative;
        padding: 2rem 0;
    }}
    
    .timeline::before {{
        content: '';
        position: absolute;
        left: 20px;
        top: 0;
        bottom: 0;
        width: 2px;
        background: var(--gradient-primary);
    }}
    
    .timeline-item {{
        position: relative;
        margin: 2rem 0;
        padding-left: 3rem;
    }}
    
    .timeline-marker {{
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
    }}
    
    .timeline-content {{
        background: var(--bg-card);
        padding: 1.25rem;
        border-radius: var(--border-radius);
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-light);
    }}
    
    .chart-container {{
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-lg);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-light);
    }}
    
    .fade-in {{
        animation: fadeIn 0.6s ease-in-out;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .slide-in-left {{
        animation: slideInLeft 0.6s ease-in-out;
    }}
    
    @keyframes slideInLeft {{
        from {{ opacity: 0; transform: translateX(-30px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    
    .bounce-in {{
        animation: bounceIn 0.8s ease-in-out;
    }}
    
    @keyframes bounceIn {{
        0% {{ opacity: 0; transform: scale(0.3); }}
        50% {{ opacity: 1; transform: scale(1.05); }}
        70% {{ transform: scale(0.9); }}
        100% {{ transform: scale(1); }}
    }}
    
    @media (max-width: 768px) {{
        .main-header h1 {{
            font-size: 2rem;
        }}
        .cell-metrics {{
            grid-template-columns: repeat(2, 1fr);
        }}
        .metrics-grid {{
            grid-template-columns: 1fr;
        }}
    }}
    
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: var(--bg-secondary);
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: var(--primary-color);
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: var(--secondary-color);
    }}
    
    .stApp > div:first-child {{
        background: var(--bg-primary);
    }}
    
    .js-plotly-plot {{
        background: var(--bg-card) !important;
        border-radius: var(--border-radius-lg);
    }}
    </style>
    """, unsafe_allow_html=True)
    
def ensure_sidebar_accessibility():
    """Ensure sidebar remains accessible and properly styled"""
    st.markdown("""
    <script>
    setInterval(() => {
    const btn = document.querySelector('.css-1rs6os');
    const sidebar = document.querySelector('[data-testid="stSidebar"]');
    if (btn && sidebar) {
        btn.innerHTML = sidebar.offsetWidth > 100 ? '‹‹' : '››';
    }
}, 500);
    document.addEventListener('DOMContentLoaded', function() {
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        const toggleButton = document.querySelector('.css-1rs6os');
        
        if (sidebar) {
            sidebar.style.minWidth = '21rem';
            sidebar.style.maxWidth = '21rem';
            sidebar.style.zIndex = '999';
        }
        
        if (toggleButton) {
            toggleButton.style.display = 'block';
            toggleButton.style.visibility = 'visible';
        }
    });
    </script>
    """, unsafe_allow_html=True)    

def init_session_state():
    defaults = {
        'cells_data': {},
        'task_queue': [],
        'current_task_index': 0,
        'task_running': False,
        'all_tasks_paused': False,
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
        'sidebar_visible': True,
        'sidebar_collapsed': False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def initialize_app():
    init_session_state()
    current_theme = st.session_state.get('theme', 'dark')
    apply_modern_css(current_theme)

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

def get_cell_animation_class(cell_status):
    animation_map = {
        'Charging': 'cell-status-charging',
        'Running CC_CV': 'cell-status-charging',
        'Running CC_CD': 'cell-status-discharging',
        'Running BALANCE': 'cell-status-balancing',
        'Running STRESS_TEST': 'cell-status-stress',
        'Stress Testing': 'cell-status-stress',
        'Idle': '',
        'Emergency Stop': ''
    }
    return animation_map.get(cell_status, '')

def get_status_icon(cell_status):
    status_map = {
        'Idle': ('⚪', 'Cell is idle'),
        'Charging': ('🔋', 'Cell is charging'),
        'Running CC_CV': ('⚡', 'Constant Current/Voltage charging'),
        'Running CC_CD': ('🔄', 'Constant Current discharge'),
        'Running BALANCE': ('⚖️', 'Cell balancing in progress'),
        'Running STRESS_TEST': ('🔥', 'Stress testing active'),
        'Stress Testing': ('🚨', 'Under stress test'),
        'Emergency Stop': ('🛑', 'Emergency stop activated'),
        'Paused': ('⏸️', 'Process paused')
    }
    return status_map.get(cell_status, ('❓', 'Unknown status'))

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
    
    cells_to_remove = [cell_key for cell_key in st.session_state.temp_history
                      if cell_key not in st.session_state.cells_data]
    for cell_key in cells_to_remove:
        del st.session_state.temp_history[cell_key]
    
    for cell_key, cell_data in st.session_state.cells_data.items():
        if cell_key not in st.session_state.temp_history:
            st.session_state.temp_history[cell_key] = {"time": [], "temp": []}
        
        temp = cell_data.get("temp", cell_data.get("temperature", 25))
        st.session_state.temp_history[cell_key]["time"].append(current_time)
        st.session_state.temp_history[cell_key]["temp"].append(temp)
        
        if len(st.session_state.temp_history[cell_key]["time"]) > 30:
            st.session_state.temp_history[cell_key]["time"] = st.session_state.temp_history[cell_key]["time"][-30:]
            st.session_state.temp_history[cell_key]["temp"] = st.session_state.temp_history[cell_key]["temp"][-30:]

def emergency_stop():
    st.session_state.emergency_stop = True
    st.session_state.task_running = False
    st.session_state.all_tasks_paused = False
    st.session_state.stress_test_mode = False
    
    for cell_name in st.session_state.cells_data:
        cell = st.session_state.cells_data[cell_name]
        cell['current'] = 0.0
        cell['status'] = 'Emergency Stop'
    
    for task in st.session_state.task_queue:
        if task['status'] == 'Running':
            task['status'] = 'Stopped'
    
    st.error("🚨 EMERGENCY STOP ACTIVATED! All operations halted.")
    st.rerun()

def navigate_to_page(page_name):
    st.session_state.current_page = page_name
    st.rerun()

def pause_all_tasks():
    st.session_state.all_tasks_paused = True
    st.session_state.task_running = False
    
    for task in st.session_state.task_queue:
        if task['status'] == 'Running':
            task['status'] = 'Paused'
    
    for cell_name in st.session_state.cells_data:
        cell = st.session_state.cells_data[cell_name]
        if 'Running' in cell.get('status', ''):
            cell['status'] = 'Paused'
            cell['current'] = 0.0

def resume_all_tasks():
    st.session_state.all_tasks_paused = False
    has_resumed_tasks = False
    
    for task in st.session_state.task_queue:
        if task['status'] == 'Paused':
            task['status'] = 'Running'
            has_resumed_tasks = True
    
    if has_resumed_tasks:
        st.session_state.task_running = True
    
    for cell_name in st.session_state.cells_data:
        cell = st.session_state.cells_data[cell_name]
        if cell.get('status') == 'Paused':
            cell['status'] = 'Idle'

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="color: var(--primary-color); font-size: 1.8rem; margin: 0; font-weight: 800;">⚡ BatteryFlow</h1>
            <p style="color: var(--text-secondary); margin: 0.5rem 0 0 0; font-size: 0.9rem;">Professional Management</p>
        </div>
        """, unsafe_allow_html=True)
        
           # NEW CODE (ADD):
        st.markdown("### 🎨 Theme Settings")

# Get current theme state
        current_theme_is_dark = st.session_state.get('theme', 'dark') == 'dark'

        # FIXED: Dynamic label based on current theme
        theme_label = "🌙 Dark Mode" if current_theme_is_dark else "☀️ Light Mode"
        theme_help = "Switch to light theme" if current_theme_is_dark else "Switch to dark theme"

        # Theme toggle with improved labeling
        theme_toggle = st.toggle(
            theme_label,
            value=current_theme_is_dark,
            key="theme_toggle_main",
            help=theme_help
        )

        # Update theme if toggled
        if theme_toggle != current_theme_is_dark:
            if theme_toggle:
                st.session_state.theme = 'dark'
            else:
                st.session_state.theme = 'light'
            st.rerun()

        
        st.divider()
        
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
        
        st.markdown("### 📊 System Status")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Cells", len(st.session_state.cells_data))
            st.metric("Tasks", len(st.session_state.task_queue))
        with col2:
            active_warnings = sum(len(get_safety_status(cell)) for cell in st.session_state.cells_data.values())
            st.metric("Warnings", active_warnings)
            st.metric("History", len(st.session_state.history))

def render_header():
    st.markdown(f"""
    <div class="main-header fade-in">
        <h1>⚡ BatteryFlow Pro</h1>
        <p>Advanced Battery Management System • Real-time Monitoring • Intelligent Analytics</p>
    </div>
    """, unsafe_allow_html=True)

def render_dashboard():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    if not st.session_state.cells_data:
        st.markdown("""
        <div class="welcome-card bounce-in">
            <h2>🚀 Welcome to BatteryFlow Pro!</h2>
            <p>Get started by setting up your battery cells to begin monitoring and management.</p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔧 Setup Cells", key="dashboard_setup_btn", use_container_width=True):
                navigate_to_page("Setup")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
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
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">⚠️ {warnings_count}</div>
            <div class="metric-title">Active Warnings</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
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
            
            animation_class = get_cell_animation_class(cell_data.get('status', 'Idle'))
            status_icon, status_desc = get_status_icon(cell_data.get('status', 'Idle'))
            
            st.markdown(f"""
            <div class="cell-card bounce-in {animation_class}">
                <div class="cell-header {cell_type_class}">
                    <div class="cell-info">
                        <div class="cell-avatar">
                            {cell_data.get('cell_type', 'NMC')[:2]}
                        </div>
                        <div>
                            <div class="cell-name">{cell_key}</div>
                            <div class="cell-type">{cell_data.get('cell_type', 'NMC')} • {status_icon} {cell_data.get('status', 'Idle')}</div>
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
                    <div style="margin-top: 0.5rem; font-size: 0.8rem; color: var(--text-muted);">
                        {status_desc}
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
    
    if st.session_state.cells_data:
        st.markdown("## 📱 Current Configuration")
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
        <p>Direct Cell Control & Manual Operations</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="content-card slide-in-left">
            <h3>⚡ Individual Cell Control</h3>
        </div>
        """, unsafe_allow_html=True)
        
        selected_cell = st.selectbox("Select Cell", list(st.session_state.cells_data.keys()))
        
        if selected_cell:
            cell = st.session_state.cells_data[selected_cell]
            
            st.markdown(f"**Current Status:** {cell.get('status', 'Idle')}")
            st.markdown(f"**Voltage:** {cell['voltage']:.2f}V")
            st.markdown(f"**Current:** {cell['current']:.2f}A")
            st.markdown(f"**Temperature:** {cell.get('temp', 25):.1f}°C")
            
            st.markdown("### 🔧 Manual Controls")
            
            new_voltage = st.slider("Set Voltage (V)", 
                                   cell['min_voltage'], 
                                   cell['max_voltage'], 
                                   cell['voltage'], 
                                   0.01)
            
            new_current = st.slider("Set Current (A)", -10.0, 10.0, cell['current'], 0.1)
            
            new_temp = st.slider("Set Temperature (°C)", 10.0, 60.0, cell.get('temp', 25), 0.1)
            
            col_x, col_y = st.columns(2)
            with col_x:
                if st.button("✅ Apply Changes", key="apply_changes", use_container_width=True):
                    cell['voltage'] = new_voltage
                    cell['current'] = new_current
                    cell['temp'] = new_temp
                    cell['temperature'] = new_temp
                    st.success(f"✅ Updated {selected_cell}")
                    st.rerun()
            
            with col_y:
                if st.button("🔄 Reset Cell", key="reset_cell", use_container_width=True):
                    specs = get_cell_specs(cell['cell_type'])
                    cell['voltage'] = specs['voltage']
                    cell['current'] = 0.0
                    cell['temp'] = random.uniform(25, 35)
                    cell['temperature'] = cell['temp']
                    cell['status'] = 'Idle'
                    st.success(f"🔄 Reset {selected_cell}")
                    st.rerun()
    
    with col2:
        st.markdown("""
        <div class="content-card">
            <h3>🔄 Quick Actions</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🚀 Bulk Operations")
        
        if st.button("⚡ Start All Charging", use_container_width=True):
            for cell_name in st.session_state.cells_data:
                cell = st.session_state.cells_data[cell_name]
                cell['current'] = 2.0
                cell['status'] = 'Charging'
            st.success("⚡ All cells started charging")
            st.rerun()
        
        if st.button("🔄 Start All Discharging", use_container_width=True):
            for cell_name in st.session_state.cells_data:
                cell = st.session_state.cells_data[cell_name]
                cell['current'] = -2.0
                cell['status'] = 'Discharging'
            st.success("🔄 All cells started discharging")
            st.rerun()
        
        if st.button("⏹️ Stop All Operations", use_container_width=True):
            for cell_name in st.session_state.cells_data:
                cell = st.session_state.cells_data[cell_name]
                cell['current'] = 0.0
                temp_val = random.uniform(25, 35)
                cell['temp'] = temp_val
                cell['temperature'] = temp_val
                cell['status'] = 'Idle'
            st.rerun()
        
        st.markdown("### 🧪 Stress Testing")
        
        if st.button("🔥 Enable Stress Test Mode", use_container_width=True):
            st.session_state.stress_test_mode = True
            for cell_name in st.session_state.cells_data:
                cell = st.session_state.cells_data[cell_name]
                cell['current'] = random.uniform(5, 8)
                cell['temp'] = random.uniform(45, 60)
                cell['temperature'] = cell['temp']
                cell['status'] = 'Stress Testing'
            st.warning("🔥 Stress test mode activated!")
            st.rerun()
        
        if st.session_state.stress_test_mode:
            if st.button("⏹️ Stop Stress Test", use_container_width=True):
                st.session_state.stress_test_mode = False
                for cell_name in st.session_state.cells_data:
                    cell = st.session_state.cells_data[cell_name]
                    cell['current'] = 0.0
                    cell['temp'] = random.uniform(25, 35)
                    cell['temperature'] = cell['temp']
                    cell['status'] = 'Idle'
                st.success("⏹️ Stress test stopped")
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

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
        
        if st.session_state.task_queue:
            for idx, task in enumerate(st.session_state.task_queue):
                status_colors = {
                    "Queued": "#ffd43b",
                    "Running": "#51cf66",
                    "Completed": "#00d4ff",
                    "Failed": "#ff6b6b",
                    "Paused": "#868e96",
                    "Stopped": "#ff6b6b"
                }
                status_icons = {
                    "Queued": "🟡",
                    "Running": "🟢",
                    "Completed": "✅",
                    "Failed": "❌",
                    "Paused": "⏸️",
                    "Stopped": "🛑"
                }
                
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
                
                if task['status'] == 'Queued':
                    col_x, col_y, col_z = st.columns(3)
                    with col_x:
                        if st.button(f"▶️ Start", key=f"start_{idx}", use_container_width=True):
                            task['status'] = 'Running'
                            task['started_at'] = datetime.now()
                            st.session_state.task_running = True
                            st.session_state.all_tasks_paused = False
                            st.rerun()
                    with col_y:
                        if st.button(f"⬆️ Priority", key=f"priority_{idx}", use_container_width=True):
                            if idx > 0:
                                st.session_state.task_queue[idx], st.session_state.task_queue[idx-1] = \
                                st.session_state.task_queue[idx-1], st.session_state.task_queue[idx]
                            st.rerun()
                    with col_z:
                        if st.button(f"🗑️ Remove", key=f"remove_task_{idx}", use_container_width=True):
                            st.session_state.task_queue.pop(idx)
                            st.rerun()
        else:
            st.markdown("""
            <div class="content-card">
                <h4>ℹ️ No tasks in queue</h4>
                <p>Create a task to get started with automated processes!</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

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
    
    # Analytics tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Real-time Monitoring", 
        "🔬 Performance Analysis", 
        "📚 Process History", 
        "💾 Data Export"
    ])
    
    with tab1:
        render_realtime_monitoring()
    
    with tab2:
        render_performance_analysis()
    
    with tab3:
        render_process_history()
    
    with tab4:
        render_data_export()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_realtime_monitoring():
    """Real-time monitoring charts"""
    # Temperature monitoring chart
    if st.session_state.temp_history:
        st.markdown("### 🌡️ Real-time Temperature Monitoring")
        
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
    
    # Voltage and current comparison charts
    col1, col2 = st.columns(2)
    with col1:
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
    
    if status_counts:
        fig_status = go.Figure(data=[
            go.Pie(
                labels=list(status_counts.keys()),
                values=list(status_counts.values()),
                hole=0.4,
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

def render_performance_analysis():
    """Performance analysis charts and metrics"""
    st.markdown("### 🔬 Cell Health Analysis")
    
    # Cell health status chart
    col1, col2 = st.columns(2)
    
    with col1:
        cells = list(st.session_state.cells_data.keys())
        health_values = [st.session_state.cells_data[cell].get("health", 100) for cell in cells]
        
        fig_health = go.Figure(data=[
            go.Bar(
                x=cells,
                y=health_values,
                marker_color='#51cf66',
                text=[f"{h:.1f}%" for h in health_values],
                textposition='auto',
            )
        ])
        
        theme_template = "plotly_white" if st.session_state.theme == 'light' else "plotly_dark"
        fig_health.update_layout(
            title="🔋 Cell Health Status",
            xaxis_title="Cell",
            yaxis_title="Health (%)",
            template=theme_template,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)' if st.session_state.theme == 'dark' else 'rgba(255,255,255,0.8)'
        )
        st.plotly_chart(fig_health, use_container_width=True)
    
    with col2:
        # Voltage distribution histogram
        voltages = [cell["voltage"] for cell in st.session_state.cells_data.values()]
        fig_voltage_dist = go.Figure(data=[
            go.Histogram(
                x=voltages,
                nbinsx=10,
                marker_color='#00d4ff',
                opacity=0.7
            )
        ])
        fig_voltage_dist.update_layout(
            title="📊 Voltage Distribution",
            xaxis_title="Voltage (V)",
            yaxis_title="Count",
            template=theme_template,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)' if st.session_state.theme == 'dark' else 'rgba(255,255,255,0.8)'
        )
        st.plotly_chart(fig_voltage_dist, use_container_width=True)
    
    # Cell type performance comparison
    st.markdown("### ⚡ Cell Type Performance Comparison")
    
    cell_type_data = {}
    for cell_data in st.session_state.cells_data.values():
        cell_type = cell_data.get('cell_type', 'Unknown')
        if cell_type not in cell_type_data:
            cell_type_data[cell_type] = {
                'count': 0,
                'avg_voltage': 0,
                'avg_temp': 0,
                'avg_health': 0,
                'voltages': [],
                'temps': [],
                'healths': []
            }
        
        cell_type_data[cell_type]['count'] += 1
        cell_type_data[cell_type]['voltages'].append(cell_data['voltage'])
        cell_type_data[cell_type]['temps'].append(cell_data.get('temp', 25))
        cell_type_data[cell_type]['healths'].append(cell_data.get('health', 100))
    
    # Calculate averages
    for cell_type in cell_type_data:
        data = cell_type_data[cell_type]
        data['avg_voltage'] = np.mean(data['voltages'])
        data['avg_temp'] = np.mean(data['temps'])
        data['avg_health'] = np.mean(data['healths'])
    
    if cell_type_data:
        comparison_data = []
        for cell_type, data in cell_type_data.items():
            comparison_data.append({
                'Type': cell_type,
                'Count': data['count'],
                'Avg Voltage (V)': f"{data['avg_voltage']:.2f}",
                'Avg Temperature (°C)': f"{data['avg_temp']:.1f}",
                'Avg Health (%)': f"{data['avg_health']:.1f}"
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True)

def render_process_history():
    """Process history and timeline view"""
    st.markdown("### 📚 Process History & Timeline")
    
    if not st.session_state.process_history:
        st.markdown("""
        <div class="content-card">
            <h4>ℹ️ No process history available yet</h4>
            <p>Complete some tasks to see history here!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Process timeline
    st.markdown("#### 🕒 Process Timeline")
    
    timeline_data = []
    for idx, process in enumerate(st.session_state.process_history):
        timeline_data.append({
            'Process': process.get('name', f'Process_{idx}'),
            'Type': process.get('type', 'Unknown'),
            'Cells': ', '.join(process.get('cells', [])),
            'Start Time': process.get('start_time', 'Unknown'),
            'End Time': process.get('end_time', 'Unknown'),
            'Duration': process.get('duration', 'Unknown'),
            'Status': process.get('status', 'Unknown')
        })
    
    if timeline_data:
        timeline_df = pd.DataFrame(timeline_data)
        st.dataframe(timeline_df, use_container_width=True)
    
    # Process statistics
    if st.session_state.process_history:
        completed_processes = [p for p in st.session_state.process_history if p.get('status') == 'Completed']
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Processes", len(st.session_state.process_history))
        with col2:
            st.metric("Completed", len(completed_processes))
        with col3:
            success_rate = (len(completed_processes) / len(st.session_state.process_history)) * 100 if st.session_state.process_history else 0
            st.metric("Success Rate", f"{success_rate:.1f}%")
        with col4:
            avg_duration = np.mean([p.get('duration_minutes', 0) for p in completed_processes]) if completed_processes else 0
            st.metric("Avg Duration", f"{avg_duration:.1f} min")

def render_data_export():
    """Data export and reporting functionality"""
    st.markdown("### 💾 Data Export & Reporting")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Export Current Data")
        
        if st.button("📄 Download Cell Data (CSV)", use_container_width=True):
            # Create CSV data
            export_data = []
            for cell_name, cell_data in st.session_state.cells_data.items():
                export_data.append({
                    'Cell Name': cell_name,
                    'Type': cell_data.get('cell_type', 'Unknown'),
                    'Voltage (V)': cell_data['voltage'],
                    'Current (A)': cell_data['current'],
                    'Temperature (°C)': cell_data.get('temp', 25),
                    'Health (%)': cell_data.get('health', 100),
                    'Status': cell_data.get('status', 'Idle'),
                    'Cycles': cell_data.get('cycles', 0),
                    'Min Voltage (V)': cell_data['min_voltage'],
                    'Max Voltage (V)': cell_data['max_voltage']
                })
            
            export_df = pd.DataFrame(export_data)
            csv = export_df.to_csv(index=False)
            st.download_button(
                label="💾 Download CSV",
                data=csv,
                file_name=f"battery_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        if st.button("📋 Download Cell Data (JSON)", use_container_width=True):
            # Create JSON data
            export_data = {
                'export_time': datetime.now().isoformat(),
                'total_cells': len(st.session_state.cells_data),
                'cells': st.session_state.cells_data
            }
            
            json_data = json.dumps(export_data, indent=2, default=str)
            st.download_button(
                label="💾 Download JSON",
                data=json_data,
                file_name=f"battery_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
    
    with col2:
        st.markdown("#### 📈 Export Process Data")
        
        if st.session_state.process_history:
            if st.button("📊 Export Process History", use_container_width=True):
                process_export = pd.DataFrame(st.session_state.process_history)
                csv = process_export.to_csv(index=False)
                st.download_button(
                    label="💾 Download Process CSV",
                    data=csv,
                    file_name=f"process_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.info("No process history to export.")
    
    # System Report
    st.markdown("#### 📋 System Report")
    
    if st.button("📊 Generate System Report", use_container_width=True):
        # Generate comprehensive system report
        total_cells = len(st.session_state.cells_data)
        avg_voltage = np.mean([cell["voltage"] for cell in st.session_state.cells_data.values()]) if st.session_state.cells_data else 0
        avg_health = np.mean([cell.get("health", 100) for cell in st.session_state.cells_data.values()]) if st.session_state.cells_data else 0
        completed_tasks = len([task for task in st.session_state.task_queue if task.get('status') == 'Completed'])
        
        report_data = {
            'report_generated': datetime.now().isoformat(),
            'system_overview': {
                'total_cells': total_cells,
                'avg_voltage': round(avg_voltage, 2),
                'avg_health': round(avg_health, 1),
                'completed_tasks': completed_tasks,
                'active_warnings': sum(len(get_safety_status(cell)) for cell in st.session_state.cells_data.values())
            },
            'cell_details': st.session_state.cells_data,
            'task_queue': st.session_state.task_queue,
            'process_history': st.session_state.process_history
        }
        
        # Display summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Cells", total_cells)
        with col2:
            st.metric("Avg Voltage", f"{avg_voltage:.2f}V")
        with col3:
            st.metric("Avg Health", f"{avg_health:.1f}%")
        with col4:
            st.metric("Completed Tasks", completed_tasks)
        
        st.success("📊 System report generated successfully!")
        
        if st.button("💾 Download System Report", use_container_width=True):
            json_report = json.dumps(report_data, indent=2, default=str)
            st.download_button(
                label="📄 Download Report JSON",
                data=json_report,
                file_name=f"system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )

def main():
    initialize_app()
    ensure_sidebar_accessibility()
    render_sidebar()
    render_header()
    
    if st.session_state.auto_refresh and st.session_state.cells_data and not st.session_state.emergency_stop:
        for cell_key in st.session_state.cells_data:
            update_cell_real_time(cell_key)
        update_temp_history()
    
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
    
    if (st.session_state.auto_refresh and
        not st.session_state.emergency_stop and
        (st.session_state.current_page == "Dashboard" or
         (st.session_state.current_page == "Task Processes" and st.session_state.task_running))):
        time.sleep(3)
        st.rerun()

if __name__ == "__main__":
    main()
