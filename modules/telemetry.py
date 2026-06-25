"""
Live Telemetry Panel
Real-time vehicle data and status
"""

import numpy as np

class TelemetryPanel:
    """
    Manages and displays live telemetry data
    """
    
    # Track speed profiles (km/h, baseline)
    TRACK_TOP_SPEEDS = {
        "Monaco": 280,
        "Silverstone": 330,
        "Yas Marina": 310,
        "Monza": 340
    }
    
    # Fuel consumption (kg per lap)
    BASE_FUEL_CONSUMPTION = 2.3
    
    def __init__(self):
        """Initialize telemetry panel"""
        self.current_speed = 280
        self.current_fuel = 100
        self.tire_temperature = 90
        self.brake_temperature = 750
    
    def get_current_speed(self, aggression: float, weather: str) -> float:
        """
        Calculate current speed based on conditions
        
        Args:
            aggression: Driver aggression (0-100)
            weather: Weather condition
            
        Returns:
            Current speed in km/h
        """
        # Base speed varies with aggression
        base_speed = 280 + (aggression - 50) / 50 * 30
        
        # Weather impact
        weather_factors = {
            "Dry": 1.0,
            "Light Rain": 0.92,
            "Heavy Rain": 0.80
        }
        
        current_speed = base_speed * weather_factors.get(weather, 1.0)
        
        # Add realistic variation
        variation = np.random.normal(0, 10)
        return max(100, min(350, current_speed + variation))
    
    def get_fuel_remaining(self, current_lap: int, initial_fuel: float) -> float:
        """
        Calculate fuel remaining
        
        Args:
            current_lap: Current lap number
            initial_fuel: Initial fuel load (kg)
            
        Returns:
            Remaining fuel in kg
        """
        consumed = current_lap * self.BASE_FUEL_CONSUMPTION
        remaining = initial_fuel - consumed
        return max(0, remaining)
    
    def get_tire_temperature(self, current_speed: float, weather: str) -> float:
        """
        Estimate tire temperature
        
        Args:
            current_speed: Current speed (km/h)
            weather: Weather condition
            
        Returns:
            Tire temperature in Celsius
        """
        # Temperature increases with speed
        base_temp = 60 + (current_speed / 350) * 100
        
        # Weather impact
        weather_temps = {
            "Dry": 0,
            "Light Rain": -10,
            "Heavy Rain": -20
        }
        
        temp = base_temp + weather_temps.get(weather, 0)
        temp += np.random.normal(0, 5)  # Variation
        
        return max(30, min(120, temp))
    
    def get_brake_temperature(self, current_speed: float) -> float:
        """
        Estimate brake temperature
        
        Args:
            current_speed: Current speed (km/h)
            
        Returns:
            Brake temperature in Celsius
        """
        # More speed = more braking = hotter brakes
        base_temp = 400 + (current_speed / 350) * 400
        base_temp += np.random.normal(0, 30)
        
        return max(200, min(900, base_temp))
    
    def get_drs_available(self, gap_ahead: float) -> bool:
        """
        Check if DRS is available
        
        Args:
            gap_ahead: Gap to car ahead (seconds)
            
        Returns:
            Whether DRS is available
        """
        # DRS available if within 1.0 second of car ahead
        return gap_ahead <= 1.0
    
    def format_telemetry_display(self, speed: float, fuel: float, grip: float, lap: int) -> str:
        """
        Format telemetry for display
        
        Args:
            speed: Current speed
            fuel: Fuel remaining
            grip: Tire grip
            lap: Current lap
            
        Returns:
            Formatted telemetry string
        """
        return f"SPD: {speed:.0f}km/h | FUEL: {fuel:.1f}kg | GRIP: {grip:.0f}% | LAP: {lap}"
