"""
Race Calculation Utilities
"""

import numpy as np
from typing import Tuple

def calculate_race_metrics(
    tire_compound: str,
    fuel_load: float,
    weather: str,
    track: str
) -> dict:
    """
    Calculate comprehensive race metrics
    
    Args:
        tire_compound: Tire compound
        fuel_load: Initial fuel
        weather: Weather condition
        track: Track name
        
    Returns:
        Dictionary of metrics
    """
    
    base_lap_time = {
        "Monaco": 78,
        "Silverstone": 88,
        "Yas Marina": 105,
        "Monza": 82
    }
    
    weather_multiplier = {
        "Dry": 1.0,
        "Light Rain": 1.08,
        "Heavy Rain": 1.15
    }
    
    tire_advantage = {
        "Soft": 1.02,
        "Medium": 1.00,
        "Hard": 0.98
    }
    
    lap_time = base_lap_time[track]
    lap_time *= weather_multiplier[weather]
    lap_time *= tire_advantage[tire_compound]
    
    # Estimate race distance
    race_laps = {
        "Monaco": 78,
        "Silverstone": 52,
        "Yas Marina": 58,
        "Monza": 53
    }
    
    total_race_time = lap_time * race_laps[track]
    
    return {
        "lap_time": lap_time,
        "total_race_time": total_race_time,
        "race_laps": race_laps[track],
        "fuel_consumption": 2.3,
        "pit_stop_time": 23
    }


def calculate_tire_life(
    compound: str,
    driver_aggression: float,
    weather: str
) -> int:
    """
    Calculate estimated tire life in laps
    
    Args:
        compound: Tire compound
        driver_aggression: Aggression level (0-100)
        weather: Weather condition
        
    Returns:
        Estimated tire life in laps
    """
    
    base_life = {
        "Soft": 25,
        "Medium": 35,
        "Hard": 45
    }
    
    life = base_life[compound]
    
    # Aggression reduces life
    life = life * (1 - (driver_aggression / 100) * 0.3)
    
    # Weather affects life
    weather_factors = {
        "Dry": 1.0,
        "Light Rain": 1.1,
        "Heavy Rain": 1.2
    }
    
    life = life * weather_factors[weather]
    
    return int(life)


def estimate_gap_ahead(
    our_pace: float,
    competitor_pace: float,
    laps_remaining: int
) -> float:
    """
    Estimate gap to car ahead
    
    Args:
        our_pace: Our lap time (seconds)
        competitor_pace: Competitor lap time (seconds)
        laps_remaining: Laps until finish
        
    Returns:
        Estimated gap in seconds
    """
    pace_delta_per_lap = our_pace - competitor_pace
    total_gap = pace_delta_per_lap * laps_remaining
    return total_gap


def calculate_pit_strategy_window(
    fuel_load: float,
    fuel_consumption: float,
    pit_lap: int
) -> Tuple[float, float, float]:
    """
    Calculate pit strategy window
    
    Args:
        fuel_load: Initial fuel
        fuel_consumption: Fuel per lap
        pit_lap: Target pit lap
        
    Returns:
        Tuple of (fuel_needed, fuel_remaining, pit_window_risk)
    """
    fuel_needed = pit_lap * fuel_consumption
    fuel_remaining = fuel_load - fuel_needed
    
    # Calculate risk (0-1, where 1 is risky)
    if fuel_needed > fuel_load:
        risk = 1.0  # Not feasible
    else:
        risk = fuel_needed / fuel_load  # Higher risk with tighter margins
    
    return fuel_needed, fuel_remaining, risk
