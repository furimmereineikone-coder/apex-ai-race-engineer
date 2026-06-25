# 🏁 APEX AI Race Engineer

**Advanced Predictive Engine for eXcellence in Motorsport Strategy**

A professional Formula 1 strategy engineering dashboard built with Streamlit, featuring real-time race simulation, AI-powered strategy recommendations, and comprehensive telemetry analysis.

## Features

### 🎯 Core Modules

1. **Race Configuration Panel** (Sidebar)
   - Tire compound selection (Soft, Medium, Hard)
   - Fuel load management (50-110 kg)
   - Weather conditions (Dry, Light Rain, Heavy Rain)
   - Driver aggression slider (0-100%)
   - Track selection (Monaco, Silverstone, Yas Marina, Monza)

2. **Tire Degradation Model**
   - Exponential decay model: `Grip = G0 × e^(-k × lap)`
   - Real-time grip visualization
   - Compound comparison
   - Tire life prediction
   - Condition recommendations

3. **Pit Stop Strategy Optimizer**
   - Optimal pit lap calculation
   - Race time prediction
   - Multi-window analysis
   - Strategic recommendations

4. **Strategy Heat Map**
   - Compound × Pit Lap × Race Time visualization
   - Optimal region highlighting
   - Color-coded performance zones

5. **Monte Carlo Race Simulator**
   - 10,000 race simulations
   - Probabilistic outcome analysis
   - Win/podium/points probability
   - Distribution visualization

6. **AI Race Engineer**
   - Intelligent strategy recommendations
   - Real-time guidance
   - Emergency protocols
   - Competitor analysis

7. **Live Telemetry Panel**
   - Current speed tracking
   - Fuel monitoring
   - Tire grip display
   - Lap counter
   - Track status indicator

8. **Track Visualization**
   - Top-down circuit map
   - Car position animation
   - Real-time movement

9. **Executive Summary**
   - Recommended strategy KPI
   - Optimal pit lap
   - Predicted race time
   - Win probability

## Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Setup

```bash
# Clone repository
git clone https://github.com/furimmereineikone-coder/apex-ai-race-engineer.git
cd apex-ai-race-engineer

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

```bash
streamlit run main.py
```

The dashboard will open at `http://localhost:8501`

## Project Structure

```
apex-ai-race-engineer/
├── main.py                          # Main Streamlit application
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
├── modules/
│   ├── tire_model.py               # Tire degradation calculations
│   ├── pit_strategy.py             # Pit optimization engine
│   ├── monte_carlo.py              # Race simulation
│   ├── ai_engineer.py              # AI strategy advisor
│   └── telemetry.py                # Telemetry data management
│
└── utils/
    ├── track_data.py               # Circuit information
    ├── styling.py                  # UI components and theming
    └── calculations.py             # Utility calculations
```

## Technical Stack

- **Frontend**: Streamlit 1.28.1
- **Visualizations**: Plotly 5.17.0
- **Scientific Computing**: NumPy 1.24.3, Pandas 2.0.3
- **Statistics**: SciPy 1.11.2

## Mathematical Models

### Tire Degradation
```
Grip(lap) = G₀ × e^(-k × lap)

Where:
- G₀ = Base grip (100% for Soft, 95% for Medium, 88% for Hard)
- k = Degradation rate (varies by compound)
- lap = Lap number
```

### Race Time Calculation
```
Race Time = Σ(Lap Time_i) + Pit Stop Time + Fuel Penalty

Lap Time includes:
- Base track lap time
- Weather multiplier
- Tire degradation effect
- Fuel load impact
```

### Monte Carlo Simulation
- 10,000 independent race simulations
- Probabilistic driver performance factors
- Normal distribution: μ=1.0, σ=0.08
- Weather-dependent variability

## Strategy Recommendations

The AI engineer analyzes:
- Current tire condition and grip level
- Fuel consumption and remaining fuel
- Weather impact on performance
- Track characteristics
- Driver aggression level
- Historical pace data

And recommends:
- **Optimal pit timing** (lap number)
- **Tire strategy** (compound and number of stops)
- **Pace management** (aggressive, balanced, conservative)
- **Risk assessment** (fuel/tire margins)
- **Finishing position** (predicted outcome)

## F1-Inspired Aesthetic

- Dark mode throughout (minimizes eye strain)
- Formula 1 color scheme:
  - Primary: #FF006E (F1 Red)
  - Secondary: #00D9FF (F1 Cyan)
  - Accent: #FFB703 (F1 Orange)
- Professional typography
- Responsive grid layout
- Custom KPI cards with gradients

## Example Use Cases

1. **Pre-Race Planning**: Configure your setup and run simulations to identify optimal strategy
2. **Live Strategy**: Use telemetry and AI recommendations during a race
3. **Post-Race Analysis**: Review race metrics and compare against predictions
4. **Driver Development**: Understand how aggression and fuel management affect outcomes

## Notes

- All data is simulated for demonstration purposes
- Real F1 data can be integrated via external APIs
- Strategy recommendations are based on simplified models
- For serious racing applications, integrate with real telemetry systems

## Future Enhancements

- Real-time data integration with F1 APIs
- Multi-driver strategy coordination
- Safety car scenario modeling
- DRS and overtaking probability analysis
- Machine learning-based strategy optimization
- Multiplayer competitive mode

## License

This project is provided for educational and demonstration purposes.

## Contact & Support

For questions or feedback, please open an issue in the repository.

---

**Built with ❤️ for motorsport engineering enthusiasts**

*🏁 APEX AI Race Engineer - Where Strategy Meets Speed*
