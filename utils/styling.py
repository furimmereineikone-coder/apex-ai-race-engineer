"""
Styling and UI Components
Formula 1 aesthetic theming
"""

import streamlit as st

def apply_theme():
    """Apply F1-inspired dark theme to Streamlit app"""
    
    st.markdown("""
    <style>
        /* Main theme colors */
        :root {
            --primary: #FF006E;      /* F1 Red */
            --secondary: #00D9FF;    /* F1 Cyan */
            --accent: #FFB703;       /* F1 Orange */
            --dark-bg: #0A0A19;
            --mid-bg: #14141E;
            --light-text: #FFFFFF;
            --muted-text: #888888;
        }
        
        /* Main background */
        .main {
            background-color: #0A0A19;
            color: #FFFFFF;
        }
        
        /* Sidebar */
        .sidebar .sidebar-content {
            background-color: #14141E;
        }
        
        /* Text and headers */
        h1, h2, h3 {
            color: #FFFFFF !important;
            font-family: 'Arial', sans-serif;
            font-weight: 700;
            letter-spacing: 1px;
        }
        
        /* Metric cards */
        [data-testid="metric-container"] {
            background-color: #14141E;
            border: 1px solid #FF006E;
            border-radius: 8px;
            padding: 16px;
        }
        
        /* Info boxes */
        .stInfo {
            background-color: #1a4d5c;
            border-left: 4px solid #00D9FF;
        }
        
        /* Success messages */
        .stSuccess {
            background-color: #1a5c2a;
            border-left: 4px solid #00FF00;
        }
        
        /* Warning messages */
        .stWarning {
            background-color: #5c4d1a;
            border-left: 4px solid #FFB703;
        }
        
        /* Error messages */
        .stError {
            background-color: #5c1a1a;
            border-left: 4px solid #FF006E;
        }
        
        /* Buttons */
        .stButton > button {
            background-color: #FF006E;
            color: #FFFFFF;
            border: none;
            border-radius: 4px;
            padding: 10px 20px;
            font-weight: bold;
            letter-spacing: 1px;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: #00D9FF;
            color: #0A0A19;
        }
        
        /* Input fields */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select {
            background-color: #14141E !important;
            color: #FFFFFF !important;
            border: 1px solid #FF006E !important;
            border-radius: 4px;
        }
        
        /* Slider */
        .stSlider > div > div > div {
            background-color: #14141E;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #14141E;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #FF006E !important;
        }
        
        /* Horizontal line */
        hr {
            border-color: #FF006E;
            opacity: 0.5;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #14141E;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #FF006E;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #00D9FF;
        }
    </style>
    """, unsafe_allow_html=True)


def render_kpi_card(title: str, value: str, subtitle: str = "", icon: str = "📊"):
    """
    Render a professional KPI card
    
    Args:
        title: KPI title
        value: KPI value
        subtitle: Optional subtitle
        icon: Optional emoji icon
    """
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #14141E 0%, #1a1a2e 100%);
        border: 2px solid #FF006E;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
        text-align: center;
        transition: all 0.3s ease;
    ">
        <div style="font-size: 24px; margin-bottom: 8px;">{icon}</div>
        <div style="
            font-size: 12px;
            color: #00D9FF;
            font-weight: bold;
            letter-spacing: 1px;
            margin-bottom: 8px;
        ">{title}</div>
        <div style="
            font-size: 28px;
            color: #FFFFFF;
            font-weight: 700;
            margin-bottom: 8px;
        ">{value}</div>
        <div style="
            font-size: 11px;
            color: #888888;
        ">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def format_time(seconds: float) -> str:
    """Format seconds to M:SS.SSS"""
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes}:{secs:06.3f}"


def format_speed(kmh: float) -> str:
    """Format speed with unit"""
    return f"{kmh:.0f} km/h"


def format_fuel(kg: float) -> str:
    """Format fuel with unit"""
    return f"{kg:.1f} kg"
