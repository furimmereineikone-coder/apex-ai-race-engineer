import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from datetime import datetime
import time

# Import custom modules
from modules.tire_model import TireDegradationModel
from modules.pit_strategy import PitStrategyOptimizer
from modules.monte_carlo import MonteCarloSimulator
from modules.ai_engineer import AIRaceEngineer
from modules.telemetry import TelemetryPanel
from utils.track_data import TRACK_DATA
from utils.styling import apply_theme, render_kpi_card
from utils.calculations import calculate_race_metrics

# Configure Streamlit page
st.set_page_config(
    page_title="APEX AI Race Engineer",
    page_icon="🏁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_theme()

# Initialize session state
if 'simulation_run' not in st.session_state:
    st.session_state.simulation_run = False
if 'current_lap' not in st.session_state:
    st.session_state.current_lap = 1

# ============================================================================
# SIDEBAR: RACE CONFIGURATION PANEL
# ============================================================================

st.sidebar.markdown("## 🏁 RACE CONFIGURATION")
st.sidebar.markdown("---")

tire_compound = st.sidebar.selectbox(
    "Tire Compound",
    options=["Soft", "Medium", "Hard"],
    index=0,
    help="Tire compound selection affects degradation and pit strategy"
)

fuel_load = st.sidebar.slider(
    "Fuel Load (kg)",
    min_value=50,
    max_value=110,
    value=80,
    step=1,
    help="Initial fuel load affects pace and pit stop timing"
)

weather = st.sidebar.selectbox(
    "Weather Conditions",
    options=["Dry", "Light Rain", "Heavy Rain"],
    index=0,
    help="Weather impacts tire grip and race dynamics"
)

driver_aggression = st.sidebar.slider(
    "Driver Aggression (%)",
    min_value=0,
    max_value=100,
    value=75,
    step=5,
    help="Higher aggression increases pace but tire wear"
)

track = st.sidebar.selectbox(
    "Track Selection",
    options=list(TRACK_DATA.keys()),
    index=0,
    help="Select the racing circuit"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Session Info")
st.sidebar.metric("Track", track)
st.sidebar.metric("Compound", tire_compound)
st.sidebar.metric("Fuel (kg)", fuel_load)

# ============================================================================
# INSTANTIATE CORE MODELS
# ============================================================================

tire_model = TireDegradationModel(tire_compound, weather, driver_aggression)
pit_optimizer = PitStrategyOptimizer(tire_compound, fuel_load, track, weather)
ai_engineer = AIRaceEngineer()
telemetry = TelemetryPanel()
simulator = MonteCarloSimulator(tire_compound, fuel_load, track, weather, driver_aggression)

# ============================================================================
# EXECUTIVE SUMMARY PANEL (TOP)
# ============================================================================

st.markdown("# 🏁 APEX AI RACE ENGINEER")
st.markdown("*Advanced Predictive Engine for eXcellence in Motorsport Strategy*")
st.markdown("---")

# Calculate optimal strategy
tire_life = tire_model.predict_tire_life()
optimal_pit_lap = pit_optimizer.find_optimal_pit_lap()
predicted_race_time = pit_optimizer.calculate_race_time(optimal_pit_lap)
win_probability = simulator.estimate_win_probability()

col1, col2, col3, col4 = st.columns(4)

with col1:
    render_kpi_card(
        title="RECOMMENDED STRATEGY",
        value=f"{tire_compound} → {tire_compound}",
        subtitle="Primary Strategy",
        icon="🎯"
    )

with col2:
    render_kpi_card(
        title="OPTIMAL PIT LAP",
        value=f"Lap {optimal_pit_lap}",
        subtitle="One-Stop Window",
        icon="🏁"
    )

with col3:
    render_kpi_card(
        title="PREDICTED RACE TIME",
        value=f"{predicted_race_time:.2f}s",
        subtitle="Estimated Duration",
        icon="⏱️"
    )

with col4:
    render_kpi_card(
        title="WIN PROBABILITY",
        value=f"{win_probability:.1f}%",
        subtitle="Monte Carlo Estimate",
        icon="🏆"
    )

st.markdown("---")

# ============================================================================
# MAIN DASHBOARD: TWO COLUMN LAYOUT
# ============================================================================

# LEFT COLUMN: Tire Degradation & Strategy
left_col, right_col = st.columns([1.2, 1])

with left_col:
    # TIRE DEGRADATION MODEL
    st.markdown("### 🔧 TIRE DEGRADATION MODEL")
    
    tire_data = tire_model.calculate_degradation(laps=50)
    current_lap = st.session_state.current_lap
    current_grip = tire_data[current_lap - 1] if current_lap <= len(tire_data) else tire_data[-1]
    
    fig_tire = go.Figure()
    
    # Compound comparison
    soft_model = TireDegradationModel("Soft", weather, driver_aggression)
    medium_model = TireDegradationModel("Medium", weather, driver_aggression)
    hard_model = TireDegradationModel("Hard", weather, driver_aggression)
    
    soft_data = soft_model.calculate_degradation(laps=50)
    medium_data = medium_model.calculate_degradation(laps=50)
    hard_data = hard_model.calculate_degradation(laps=50)
    
    laps = np.arange(1, 51)
    
    fig_tire.add_trace(go.Scatter(
        x=laps, y=soft_data,
        mode='lines',
        name='Soft',
        line=dict(color='#FF006E', width=3),
        hovertemplate='<b>Soft Tire</b><br>Lap %{x}<br>Grip: %{y:.1f}%<extra></extra>'
    ))
    
    fig_tire.add_trace(go.Scatter(
        x=laps, y=medium_data,
        mode='lines',
        name='Medium',
        line=dict(color='#FFB703', width=3),
        hovertemplate='<b>Medium Tire</b><br>Lap %{x}<br>Grip: %{y:.1f}%<extra></extra>'
    ))
    
    fig_tire.add_trace(go.Scatter(
        x=laps, y=hard_data,
        mode='lines',
        name='Hard',
        line=dict(color='#00D9FF', width=3),
        hovertemplate='<b>Hard Tire</b><br>Lap %{x}<br>Grip: %{y:.1f}%<extra></extra>'
    ))
    
    fig_tire.update_layout(
        title=f"Tire Degradation Over Race Distance | {weather} Conditions",
        xaxis_title="Lap Number",
        yaxis_title="Grip Level (%)",
        hovermode='x unified',
        template='plotly_dark',
        plot_bgcolor='rgba(20,20,40,0.5)',
        paper_bgcolor='rgba(10,10,25,0.8)',
        font=dict(color='#FFFFFF', family='Arial, sans-serif'),
        height=450,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    st.plotly_chart(fig_tire, use_container_width=True)
    
    # Tire metrics
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        render_kpi_card("CURRENT GRIP", f"{current_grip:.1f}%", "Lap " + str(current_lap), "📊")
    with col_b:
        render_kpi_card("TIRE LIFE", f"{tire_life:.0f} laps", f"{tire_compound} Compound", "⌛")
    with col_c:
        if current_grip > 80:
            rec = "✅ Fresh"
        elif current_grip > 60:
            rec = "⚠️ Monitor"
        else:
            rec = "🔴 Box Soon"
        render_kpi_card("RECOMMENDATION", rec, "Tire Status", "🎯")

with right_col:
    # PIT STOP STRATEGY OPTIMIZER
    st.markdown("### 🏁 PIT STOP STRATEGY")
    
    pit_data = pit_optimizer.optimize_pit_windows()
    
    fig_pit = go.Figure()
    
    fig_pit.add_trace(go.Scatter(
        x=pit_data['pit_lap'],
        y=pit_data['race_time'],
        mode='lines+markers',
        name='Race Time',
        line=dict(color='#00D9FF', width=2),
        marker=dict(size=6),
        hovertemplate='<b>Pit Strategy</b><br>Pit Lap: %{x}<br>Race Time: %{y:.2f}s<extra></extra>'
    ))
    
    # Highlight optimal
    optimal_idx = pit_data['race_time'].argmin()
    fig_pit.add_trace(go.Scatter(
        x=[pit_data['pit_lap'].iloc[optimal_idx]],
        y=[pit_data['race_time'].iloc[optimal_idx]],
        mode='markers',
        name='Optimal',
        marker=dict(size=12, color='#FFB703', symbol='star'),
        hovertemplate='<b>OPTIMAL STRATEGY</b><br>Pit Lap: %{x}<br>Race Time: %{y:.2f}s<extra></extra>'
    ))
    
    fig_pit.update_layout(
        title="Pit Window Optimization",
        xaxis_title="Pit Lap Number",
        yaxis_title="Total Race Time (s)",
        template='plotly_dark',
        plot_bgcolor='rgba(20,20,40,0.5)',
        paper_bgcolor='rgba(10,10,25,0.8)',
        font=dict(color='#FFFFFF', family='Arial, sans-serif'),
        height=450,
        margin=dict(l=50, r=50, t=50, b=50),
        hovermode='closest'
    )
    
    st.plotly_chart(fig_pit, use_container_width=True)

# ============================================================================
# STRATEGY HEAT MAP
# ============================================================================

st.markdown("---")
st.markdown("### 🔥 STRATEGY HEAT MAP")
st.markdown("*Optimal pit lap × tire compound × predicted race time*")

compounds = ["Soft", "Medium", "Hard"]
pit_laps = np.arange(10, 50, 3)
heatmap_data = []

for compound in compounds:
    compound_row = []
    for pit_lap in pit_laps:
        # Calculate race time for this combination
        opt = PitStrategyOptimizer(compound, fuel_load, track, weather)
        race_time = opt.calculate_race_time(int(pit_lap))
        compound_row.append(race_time)
    heatmap_data.append(compound_row)

fig_heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_data,
    x=pit_laps,
    y=compounds,
    colorscale='Viridis',
    hovertemplate='<b>Strategy</b><br>Compound: %{y}<br>Pit Lap: %{x}<br>Race Time: %{z:.2f}s<extra></extra>'
))

fig_heatmap.update_layout(
    title=f"Strategy Optimization Heat Map | Track: {track}",
    xaxis_title="Pit Lap Number",
    yaxis_title="Tire Compound",
    template='plotly_dark',
    plot_bgcolor='rgba(20,20,40,0.5)',
    paper_bgcolor='rgba(10,10,25,0.8)',
    font=dict(color='#FFFFFF', family='Arial, sans-serif'),
    height=350,
    coloraxis_colorbar=dict(title="Race Time (s)")
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# ============================================================================
# MONTE CARLO RACE SIMULATOR
# ============================================================================

st.markdown("---")
st.markdown("### 🎲 MONTE CARLO RACE SIMULATOR")
st.markdown("*10,000 simulated race outcomes*")

if st.button("▶️ Run Race Simulation (10,000 iterations)", key="monte_carlo_btn"):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    with st.spinner("Running simulations..."):
        results = simulator.run_simulations(num_simulations=10000)
        progress_bar.progress(100)
        status_text.success("✅ Simulation complete!")
    
    st.session_state.simulation_run = True
    st.session_state.simulation_results = results

if st.session_state.simulation_run:
    results = st.session_state.simulation_results
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_position = results['finishing_positions'].mean()
        render_kpi_card(
            "AVG FINISH POS",
            f"{avg_position:.1f}",
            f"Out of {len(TRACK_DATA[track]['grid_positions'])} drivers",
            "📊"
        )
    
    with col2:
        win_prob = (results['finishing_positions'] == 1).sum() / len(results['finishing_positions']) * 100
        render_kpi_card("WIN PROBABILITY", f"{win_prob:.1f}%", "P1 Finish", "🏆")
    
    with col3:
        podium_prob = (results['finishing_positions'] <= 3).sum() / len(results['finishing_positions']) * 100
        render_kpi_card("PODIUM PROB", f"{podium_prob:.1f}%", "Top 3 Finish", "🥇")
    
    with col4:
        points_prob = (results['finishing_positions'] <= 10).sum() / len(results['finishing_positions']) * 100
        render_kpi_card("POINTS PROB", f"{points_prob:.1f}%", "Top 10 Finish", "📈")
    
    # Histogram
    col_hist1, col_hist2 = st.columns(2)
    
    with col_hist1:
        fig_dist = go.Figure()
        fig_dist.add_trace(go.Histogram(
            x=results['finishing_positions'],
            nbinsx=20,
            name='Finishing Position',
            marker_color='#00D9FF',
            hovertemplate='<b>Position Range</b><br>Frequency: %{y}<extra></extra>'
        ))
        
        fig_dist.update_layout(
            title="Distribution of Finishing Positions",
            xaxis_title="Grid Position",
            yaxis_title="Frequency (out of 10,000)",
            template='plotly_dark',
            plot_bgcolor='rgba(20,20,40,0.5)',
            paper_bgcolor='rgba(10,10,25,0.8)',
            font=dict(color='#FFFFFF', family='Arial, sans-serif'),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with col_hist2:
        fig_times = go.Figure()
        fig_times.add_trace(go.Histogram(
            x=results['race_times'],
            nbinsx=30,
            name='Race Time',
            marker_color='#FFB703',
            hovertemplate='<b>Time Range</b><br>Frequency: %{y}<extra></extra>'
        ))
        
        fig_times.update_layout(
            title="Distribution of Race Times",
            xaxis_title="Total Race Time (s)",
            yaxis_title="Frequency (out of 10,000)",
            template='plotly_dark',
            plot_bgcolor='rgba(20,20,40,0.5)',
            paper_bgcolor='rgba(10,10,25,0.8)',
            font=dict(color='#FFFFFF', family='Arial, sans-serif'),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig_times, use_container_width=True)

# ============================================================================
# TELEMETRY PANEL
# ============================================================================

st.markdown("---")
st.markdown("### 📡 LIVE TELEMETRY")

col_telem1, col_telem2, col_telem3, col_telem4, col_telem5 = st.columns(5)

current_speed = telemetry.get_current_speed(driver_aggression, weather)
fuel_remaining = telemetry.get_fuel_remaining(st.session_state.current_lap, fuel_load)
tire_grip = tire_data[st.session_state.current_lap - 1]
track_status = "🟢 DRY" if weather == "Dry" else ("🟡 WET" if weather == "Light Rain" else "🔴 FLOODING")

with col_telem1:
    render_kpi_card("SPEED", f"{current_speed:.0f}", "km/h", "🏎️")

with col_telem2:
    render_kpi_card("FUEL", f"{fuel_remaining:.1f}", "kg", "⛽")

with col_telem3:
    render_kpi_card("TIRE GRIP", f"{tire_grip:.1f}%", "Condition", "🛞")

with col_telem4:
    render_kpi_card("LAP", f"{st.session_state.current_lap}", "Current", "🔄")

with col_telem5:
    render_kpi_card("TRACK", track_status, "Status", "🌧️")

# ============================================================================
# AI RACE ENGINEER
# ============================================================================

st.markdown("---")
st.markdown("### 🤖 AI RACE ENGINEER")
st.markdown("*Advanced Strategy Assistant*")

ai_analysis = ai_engineer.generate_strategy(
    tire_compound=tire_compound,
    fuel_load=fuel_load,
    weather=weather,
    driver_aggression=driver_aggression,
    track=track,
    current_lap=st.session_state.current_lap,
    tire_grip=tire_grip,
    optimal_pit_lap=optimal_pit_lap,
    predicted_race_time=predicted_race_time,
    win_probability=win_probability
)

st.info(f"**ENGINEER**: {ai_analysis}")

# ============================================================================
# TRACK VISUALIZATION
# ============================================================================

st.markdown("---")
st.markdown("### 🏁 TRACK VISUALIZATION")

fig_track = go.Figure()

# Get track data
track_info = TRACK_DATA[track]
track_points = track_info['circuit_points']

# Draw track outline
fig_track.add_trace(go.Scatter(
    x=track_points[:, 0],
    y=track_points[:, 1],
    mode='lines',
    name='Track',
    line=dict(color='#00FF00', width=3),
    fill='toself',
    fillcolor='rgba(0, 255, 0, 0.1)',
    hoverinfo='skip'
))

# Current car position
current_pos_idx = int((st.session_state.current_lap / 50) * len(track_points))
current_pos_idx = min(current_pos_idx, len(track_points) - 1)
car_x = track_points[current_pos_idx, 0]
car_y = track_points[current_pos_idx, 1]

fig_track.add_trace(go.Scatter(
    x=[car_x],
    y=[car_y],
    mode='markers+text',
    name='Car',
    marker=dict(size=20, color='#FF006E', symbol='diamond'),
    text=['🏎️'],
    textposition='top center',
    hovertemplate='<b>Car Position</b><br>Lap: ' + str(st.session_state.current_lap) + '<extra></extra>'
))

fig_track.update_layout(
    title=f"Track Map: {track}",
    xaxis_title="Track Coordinates (m)",
    yaxis_title="Track Coordinates (m)",
    template='plotly_dark',
    plot_bgcolor='rgba(20,20,40,0.5)',
    paper_bgcolor='rgba(10,10,25,0.8)',
    font=dict(color='#FFFFFF', family='Arial, sans-serif'),
    height=450,
    hovermode='closest',
    xaxis=dict(scaleanchor="y", scaleratio=1),
    yaxis=dict(scaleanchor="x", scaleratio=1)
)

st.plotly_chart(fig_track, use_container_width=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888; font-size: 12px;'>
    🏁 <b>APEX AI Race Engineer</b> | Advanced Predictive Engine for Excellence in Motorsport Strategy<br>
    Powered by Streamlit • Plotly • NumPy • Pandas<br>
    <i>Simulation data for demonstration purposes only</i>
    </div>
    """,
    unsafe_allow_html=True
)
