"""
Monte Carlo Race Simulator
Simulates 10,000 race outcomes with probability distributions
"""

import numpy as np
import pandas as pd
from typing import Dict

class MonteCarloSimulator:
    """
    Runs Monte Carlo simulations of race outcomes
    """
    
    # Number of competitors
    NUM_DRIVERS = 20
    
    # Base performance variance
    PERFORMANCE_VARIANCE = 0.08
    
    # Tire compound performance factors
    COMPOUND_FACTORS = {
        "Soft": 1.02,
        "Medium": 1.00,
        "Hard": 0.98
    }
    
    # Weather impact on variability
    WEATHER_VARIABILITY = {
        "Dry": 0.05,
        "Light Rain": 0.12,
        "Heavy Rain": 0.18
    }
    
    def __init__(self, compound: str, fuel_load: float, track: str, weather: str, aggression: float):
        """
        Initialize Monte Carlo simulator
        
        Args:
            compound: Tire compound
            fuel_load: Initial fuel (kg)
            track: Track name
            weather: Weather condition
            aggression: Driver aggression (0-100)
        """
        self.compound = compound
        self.fuel_load = fuel_load
        self.track = track
        self.weather = weather
        self.aggression = aggression
        
        self.compound_factor = self.COMPOUND_FACTORS[compound]
        self.variability = self.WEATHER_VARIABILITY[weather]
    
    def simulate_race(self) -> tuple:
        """
        Simulate a single race
        
        Returns:
            Tuple of (finishing_position, race_time)
        """
        # Generate random performance factors for all drivers
        driver_performances = np.random.normal(1.0, self.PERFORMANCE_VARIANCE, self.NUM_DRIVERS)
        
        # Our driver's baseline performance
        our_base_performance = self.compound_factor * (1 + (self.aggression / 100) * 0.05)
        our_base_performance += np.random.normal(0, self.variability)
        
        # Adjust for fuel load impact
        fuel_penalty = (110 - self.fuel_load) / 110 * 0.02  # Better pace with less fuel
        our_performance = our_base_performance + fuel_penalty
        
        # Compare with other drivers
        finishing_positions = np.argsort(driver_performances)
        
        # Find our position
        our_position = 1
        for pos, driver_idx in enumerate(finishing_positions):
            if driver_performances[driver_idx] < our_performance:
                our_position = pos + 1
        
        # Generate realistic race time
        base_race_time = np.random.normal(5400, 200)  # 90 minutes +/- variance
        our_race_time = base_race_time * (1 - (our_performance - 1) * 0.1)
        
        return int(our_position), our_race_time
    
    def run_simulations(self, num_simulations: int = 10000) -> Dict:
        """
        Run multiple race simulations
        
        Args:
            num_simulations: Number of simulations to run
            
        Returns:
            Dictionary with results
        """
        finishing_positions = []
        race_times = []
        
        for _ in range(num_simulations):
            position, race_time = self.simulate_race()
            finishing_positions.append(position)
            race_times.append(race_time)
        
        return {
            'finishing_positions': np.array(finishing_positions),
            'race_times': np.array(race_times)
        }
    
    def estimate_win_probability(self) -> float:
        """
        Estimate probability of winning
        
        Returns:
            Win probability (%)
        """
        # Base probability varies with setup
        base_win_prob = (self.compound_factor - 0.98) * 100
        base_win_prob += (self.aggression - 50) / 50 * 5
        base_win_prob += (self.fuel_load - 80) / 30 * 2
        
        # Clamp to reasonable range
        return max(5, min(45, base_win_prob))
    
    def estimate_podium_probability(self) -> float:
        """
        Estimate probability of podium finish
        
        Returns:
            Podium probability (%)
        """
        base_prob = self.estimate_win_probability() * 3.5  # Rough multiplier
        return max(20, min(85, base_prob))
    
    def estimate_points_probability(self) -> float:
        """
        Estimate probability of scoring points (top 10)
        
        Returns:
            Points probability (%)
        """
        base_prob = self.estimate_win_probability() * 8
        return max(50, min(98, base_prob))
