"""
Tire Degradation Model
Implements exponential decay model for tire grip over race distance
"""

import numpy as np
from typing import List, Tuple

class TireDegradationModel:
    """
    Models tire degradation using exponential decay:
    Grip = G0 × e^(-k × lap)
    """
    
    # Base grip values for each compound (%)
    GRIP_BASELINE = {
        "Soft": 100,
        "Medium": 95,
        "Hard": 88
    }
    
    # Degradation rates (k parameter)
    DEGRADATION_RATES = {
        "Soft": 0.08,
        "Medium": 0.05,
        "Hard": 0.03
    }
    
    # Weather impact multipliers
    WEATHER_MULTIPLIERS = {
        "Dry": 1.0,
        "Light Rain": 0.85,
        "Heavy Rain": 0.70
    }
    
    # Aggression impact on wear
    AGGRESSION_MULTIPLIER = 0.002
    
    def __init__(self, compound: str, weather: str, driver_aggression: float):
        """
        Initialize tire model
        
        Args:
            compound: Tire compound ("Soft", "Medium", "Hard")
            weather: Weather condition ("Dry", "Light Rain", "Heavy Rain")
            driver_aggression: Driver aggression level (0-100%)
        """
        self.compound = compound
        self.weather = weather
        self.driver_aggression = driver_aggression
        
        # Calculate effective degradation rate
        self.base_grip = self.GRIP_BASELINE[compound]
        self.degradation_rate = self.DEGRADATION_RATES[compound]
        self.weather_multiplier = self.WEATHER_MULTIPLIERS[weather]
        
        # Aggression increases wear
        self.effective_degradation = self.degradation_rate * (
            1 + (driver_aggression / 100) * self.AGGRESSION_MULTIPLIER
        )
    
    def calculate_grip(self, lap: int) -> float:
        """
        Calculate tire grip at a given lap using exponential decay
        
        Args:
            lap: Lap number (starting from 1)
            
        Returns:
            Grip percentage (0-100%)
        """
        grip = self.base_grip * np.exp(-self.effective_degradation * (lap - 1))
        
        # Apply weather multiplier
        grip = grip * self.weather_multiplier
        
        # Minimum grip (tires don't go below 30%)
        grip = max(grip, 30)
        
        return float(grip)
    
    def calculate_degradation(self, laps: int = 50) -> np.ndarray:
        """
        Calculate grip degradation over multiple laps
        
        Args:
            laps: Number of laps to simulate
            
        Returns:
            Array of grip percentages for each lap
        """
        return np.array([self.calculate_grip(lap) for lap in range(1, laps + 1)])
    
    def predict_tire_life(self, minimum_grip: float = 50.0) -> int:
        """
        Predict useful tire life (until grip drops below threshold)
        
        Args:
            minimum_grip: Minimum acceptable grip level (%)
            
        Returns:
            Number of laps tire remains usable
        """
        for lap in range(1, 100):
            if self.calculate_grip(lap) < minimum_grip:
                return lap
        return 100  # Default to 100 if still above minimum
    
    def get_recommendation(self, current_lap: int) -> str:
        """
        Generate tire condition recommendation
        
        Args:
            current_lap: Current lap number
            
        Returns:
            Recommendation string
        """
        grip = self.calculate_grip(current_lap)
        
        if grip > 85:
            return "✅ TIRES FRESH - Push hard"
        elif grip > 70:
            return "🟢 TIRES GOOD - Maintain pace"
        elif grip > 55:
            return "🟡 TIRES FADING - Monitor closely"
        elif grip > 40:
            return "🔴 CRITICAL - Pit window open"
        else:
            return "⚠️ DANGER - Box immediately"
    
    def estimate_lap_time_delta(self, lap: int, baseline_time: float = 90.0) -> float:
        """
        Estimate lap time delta due to tire degradation
        
        Args:
            lap: Lap number
            baseline_time: Baseline lap time with fresh tires (seconds)
            
        Returns:
            Lap time in seconds
        """
        grip = self.calculate_grip(lap)
        # Grip loss increases lap time non-linearly
        grip_loss = (100 - grip) / 100
        time_delta = baseline_time * (1 + grip_loss * 0.15)  # 15% max degradation
        return time_delta
