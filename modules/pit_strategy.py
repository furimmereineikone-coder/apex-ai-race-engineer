"""
Pit Stop Strategy Optimizer
Calculates optimal pit window and total race times
"""

import numpy as np
import pandas as pd
from typing import Dict, List

class PitStrategyOptimizer:
    """
    Optimizes pit stop strategy based on track, fuel, and tire compound
    """
    
    # Pit stop duration in seconds (constant, realistic F1 data)
    PIT_STOP_TIME = 23  # seconds
    
    # Fuel consumption per lap (kg/lap)
    FUEL_CONSUMPTION = {
        "Soft": 2.5,
        "Medium": 2.3,
        "Hard": 2.1
    }
    
    # Track lap times (seconds, baseline dry)
    TRACK_LAP_TIMES = {
        "Monaco": 78,
        "Silverstone": 88,
        "Yas Marina": 105,
        "Monza": 82
    }
    
    # Lap count for races
    RACE_DISTANCES = {
        "Monaco": 78,
        "Silverstone": 52,
        "Yas Marina": 58,
        "Monza": 53
    }
    
    # Weather multipliers on lap time
    WEATHER_LAP_MULTIPLIERS = {
        "Dry": 1.0,
        "Light Rain": 1.08,
        "Heavy Rain": 1.15
    }
    
    def __init__(self, compound: str, fuel_load: float, track: str, weather: str):
        """
        Initialize pit strategy optimizer
        
        Args:
            compound: Tire compound
            fuel_load: Initial fuel load (kg)
            track: Track name
            weather: Weather condition
        """
        self.compound = compound
        self.fuel_load = fuel_load
        self.track = track
        self.weather = weather
        
        self.base_lap_time = self.TRACK_LAP_TIMES[track]
        self.race_distance = self.RACE_DISTANCES[track]
        self.fuel_consumption = self.FUEL_CONSUMPTION[compound]
        self.weather_multiplier = self.WEATHER_LAP_MULTIPLIERS[weather]
    
    def calculate_lap_time(self, lap: int, has_pitted: bool = False) -> float:
        """
        Calculate lap time for a specific lap
        
        Args:
            lap: Lap number
            has_pitted: Whether car has pitted
            
        Returns:
            Lap time in seconds
        """
        # Base lap time with weather multiplier
        lap_time = self.base_lap_time * self.weather_multiplier
        
        # Fuel load affects lap time (heavier = slower)
        # Remove fuel consumption impact post-pit
        if has_pitted:
            fuel_effect = 0
        else:
            remaining_fuel = max(self.fuel_load - (lap - 1) * self.fuel_consumption, 0)
            fuel_effect = (remaining_fuel / 100) * 0.03  # Max 3% impact
        
        lap_time = lap_time * (1 + fuel_effect)
        
        # Tire degradation (simplified)
        tire_wear_effect = (lap / self.race_distance) * 0.05  # Max 5% slower
        lap_time = lap_time * (1 + tire_wear_effect)
        
        return lap_time
    
    def calculate_race_time(self, pit_lap: int) -> float:
        """
        Calculate total race time for a given pit lap
        
        Args:
            pit_lap: Lap number to pit
            
        Returns:
            Total race time in seconds
        """
        total_time = 0.0
        
        # Laps before pit stop
        for lap in range(1, pit_lap):
            total_time += self.calculate_lap_time(lap, has_pitted=False)
        
        # Pit stop lap
        pit_lap_time = self.calculate_lap_time(pit_lap, has_pitted=False)
        total_time += pit_lap_time
        total_time += self.PIT_STOP_TIME  # Add pit stop duration
        
        # Laps after pit stop (with fresh tires)
        for lap in range(pit_lap + 1, self.race_distance + 1):
            total_time += self.calculate_lap_time(lap, has_pitted=True)
        
        return total_time
    
    def find_optimal_pit_lap(self) -> int:
        """
        Find the optimal pit lap by testing all windows
        
        Returns:
            Optimal pit lap number
        """
        times = []
        pit_laps = range(10, self.race_distance - 5)
        
        for pit_lap in pit_laps:
            race_time = self.calculate_race_time(pit_lap)
            times.append(race_time)
        
        # Find minimum
        optimal_idx = np.argmin(times)
        optimal_pit_lap = list(pit_laps)[optimal_idx]
        
        return optimal_pit_lap
    
    def optimize_pit_windows(self, window_size: int = 3) -> pd.DataFrame:
        """
        Generate pit window optimization data
        
        Args:
            window_size: Step size for pit lap testing
            
        Returns:
            DataFrame with pit lap and race time
        """
        pit_laps = list(range(10, self.race_distance - 5, window_size))
        race_times = [self.calculate_race_time(lap) for lap in pit_laps]
        
        return pd.DataFrame({
            'pit_lap': pit_laps,
            'race_time': race_times
        })
    
    def get_fuel_requirement(self, pit_lap: int) -> float:
        """
        Calculate fuel requirement until pit
        
        Args:
            pit_lap: Pit lap number
            
        Returns:
            Required fuel (kg)
        """
        return pit_lap * self.fuel_consumption
    
    def strategy_recommendation(self) -> str:
        """
        Generate strategy recommendation
        
        Returns:
            Recommendation string
        """
        optimal_pit = self.find_optimal_pit_lap()
        required_fuel = self.get_fuel_requirement(optimal_pit)
        
        if required_fuel > self.fuel_load:
            return f"⚠️ INSUFFICIENT FUEL - Need {required_fuel:.1f}kg, have {self.fuel_load}kg"
        else:
            return f"✅ STRATEGY OK - Pit lap {optimal_pit} with {self.fuel_load - required_fuel:.1f}kg reserve"
