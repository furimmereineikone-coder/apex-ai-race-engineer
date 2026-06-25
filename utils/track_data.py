"""
Track Data and Circuit Information
"""

import numpy as np

# Generate circuit point clouds for track visualization
def generate_circuit(circuit_type: str, num_points: int = 200) -> np.ndarray:
    """Generate track circuit as 2D array of coordinates"""
    t = np.linspace(0, 2 * np.pi, num_points)
    
    if circuit_type == "Monaco":
        # Tight, winding circuit
        x = 100 * np.cos(t) + 50 * np.sin(3 * t)
        y = 100 * np.sin(t) + 50 * np.cos(3 * t)
    elif circuit_type == "Silverstone":
        # Fast, flowing circuit
        x = 150 * np.cos(t) + 40 * np.sin(2 * t)
        y = 150 * np.sin(t) + 40 * np.cos(2 * t)
    elif circuit_type == "Yas Marina":
        # Long, technical circuit
        x = 200 * np.cos(t) + 60 * np.sin(2.5 * t)
        y = 200 * np.sin(t) + 60 * np.cos(2.5 * t)
    elif circuit_type == "Monza":
        # High-speed circuit
        x = 180 * np.cos(t) + 30 * np.sin(t)
        y = 180 * np.sin(t) + 30 * np.cos(t)
    else:
        x = 100 * np.cos(t)
        y = 100 * np.sin(t)
    
    return np.column_stack([x, y])


TRACK_DATA = {
    "Monaco": {
        "length_km": 3.337,
        "lap_record": 76.095,
        "drs_zones": 0,
        "grip_level": "low",
        "circuit_points": generate_circuit("Monaco"),
        "grid_positions": list(range(1, 21)),
        "characteristics": "Tight, technical, low-grip street circuit"
    },
    "Silverstone": {
        "length_km": 5.891,
        "lap_record": 82.519,
        "drs_zones": 2,
        "grip_level": "high",
        "circuit_points": generate_circuit("Silverstone"),
        "grid_positions": list(range(1, 21)),
        "characteristics": "Fast, flowing, high-grip permanent circuit"
    },
    "Yas Marina": {
        "length_km": 5.554,
        "lap_record": 103.561,
        "drs_zones": 3,
        "grip_level": "medium",
        "circuit_points": generate_circuit("Yas Marina"),
        "grid_positions": list(range(1, 21)),
        "characteristics": "Long, technical, multi-sector circuit"
    },
    "Monza": {
        "length_km": 5.793,
        "lap_record": 81.738,
        "drs_zones": 2,
        "grip_level": "high",
        "circuit_points": generate_circuit("Monza"),
        "grid_positions": list(range(1, 21)),
        "characteristics": "High-speed, slipstream-dependent circuit"
    }
}
