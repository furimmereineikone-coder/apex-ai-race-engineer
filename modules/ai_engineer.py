"""
AI Race Engineer
Provides strategic recommendations in race engineer tone
"""

class AIRaceEngineer:
    """
    AI-powered race strategy advisor
    """
    
    STRATEGIES = {
        "aggressive": "Push hard mate! Soft tires are hot right now. We're hunting P1.",
        "balanced": "Steady pace. We're in a good window. Keep managing the tires.",
        "conservative": "Play it safe. Fuel situation is tight. No heroics needed.",
        "fuel_critical": "Fuel level critical! Lift and coast into the pit. We need to box NOW.",
        "tire_critical": "Tires are gone! Box this lap! Get those hards on and we'll hunt them down.",
        "weather_wet": "Conditions are wet. Back off slightly, but stay in the fight.",
        "weather_rain": "Heavy rain incoming. Boxes will be chaos. Time to capitalize.",
    }
    
    PIT_WINDOWS = {
        "early": "Early pit window (Lap 15-20) could give us track position advantage.",
        "middle": "Middle of the race pit window (Lap 25-30) for strategic balance.",
        "late": "Late pit (Lap 35+) to maximize tire performance in final phase.",
    }
    
    def __init__(self):
        """Initialize AI race engineer"""
        pass
    
    def generate_strategy(
        self,
        tire_compound: str,
        fuel_load: float,
        weather: str,
        driver_aggression: float,
        track: str,
        current_lap: int,
        tire_grip: float,
        optimal_pit_lap: int,
        predicted_race_time: float,
        win_probability: float
    ) -> str:
        """
        Generate strategic recommendation
        
        Args:
            tire_compound: Current tire compound
            fuel_load: Current fuel load (kg)
            weather: Current weather
            driver_aggression: Driver aggression level
            track: Track name
            current_lap: Current lap number
            tire_grip: Current tire grip (%)
            optimal_pit_lap: Optimal pit lap number
            predicted_race_time: Predicted race time
            win_probability: Win probability (%)
            
        Returns:
            Strategy recommendation string
        """
        
        # Determine urgency levels
        fuel_ratio = fuel_load / 110
        grip_critical = tire_grip < 50
        fuel_critical = fuel_load < 20
        
        # Build recommendation
        recommendations = []
        
        # Main strategy statement
        if win_probability > 30:
            recommendations.append("We've got a strong car today - let's go for the win.")
        elif win_probability > 15:
            recommendations.append("Solid setup. Let's execute a clean race and target the podium.")
        else:
            recommendations.append("We're in the fight. Smart driving wins races.")
        
        # Tire analysis
        if tire_grip > 85:
            recommendations.append(f"Tires are fresh and hot. {tire_compound}s are performing - push the pace.")
        elif tire_grip > 70:
            recommendations.append(f"Tires working well. {tire_compound} degradation is predictable - maintain focus.")
        elif tire_grip > 55:
            recommendations.append(f"Tires fading but still got pace. Window for pit stop is opening soon.")
        else:
            recommendations.append(f"⚠️ TIRES CRITICAL - We need to pit THIS LAP. Get on the box NOW.")
        
        # Pit strategy
        recommendations.append(
            f"Target pit window is Lap {optimal_pit_lap}. We'll have {predicted_race_time/60:.1f} min race time."
        )
        
        # Fuel management
        if fuel_critical:
            recommendations.append("🔴 FUEL CRITICAL - Lift and coast. No more pushing.")
        elif fuel_ratio < 0.35:
            recommendations.append("Fuel getting tight. Start managing consumption now.")
        else:
            recommendations.append(f"Fuel level good ({fuel_load:.1f}kg). No issues.")
        
        # Weather adaptation
        if weather == "Light Rain":
            recommendations.append("Light rain - smooth inputs. Traction is key. Stay smooth.")
        elif weather == "Heavy Rain":
            recommendations.append("HEAVY RAIN - Conditions are treacherous. Safety first, pace second.")
        
        # Aggression feedback
        if driver_aggression > 85:
            recommendations.append("You're pushing hard - I like it. Just manage those tires.")
        elif driver_aggression < 40:
            recommendations.append("Let's turn up the aggression a bit. We've got pace in hand.")
        
        # Final call
        if current_lap < 10:
            recommendations.append("Race is young. Focus on a clean first stint and execute the plan.")
        elif current_lap < (optimal_pit_lap - 2):
            recommendations.append("Settling in nicely. Getting close to our pit window.")
        elif current_lap == optimal_pit_lap:
            recommendations.append("🏁 PIT THIS LAP - Box, box. Fresh tires, let's finish strong.")
        else:
            recommendations.append("Final push incoming. Maximize the tires. Bring it home.")
        
        # Combine all recommendations
        full_strategy = " ".join(recommendations)
        return full_strategy
    
    def analyze_competitor(self, position_ahead: int, gap_seconds: float, pace_delta: float) -> str:
        """
        Analyze competitor ahead
        
        Args:
            position_ahead: Position of car ahead
            gap_seconds: Gap in seconds
            pace_delta: Our pace advantage/disadvantage
            
        Returns:
            Competitor analysis
        """
        if gap_seconds < 2:
            return f"P{position_ahead} is within DRS range. Get a tow and we can fight."
        elif gap_seconds < 5:
            return f"P{position_ahead} is close. Couple of good laps and we're in contact."
        else:
            return f"P{position_ahead} has some gap. We'll need consistent execution to close it."
    
    def emergency_protocol(self, issue: str) -> str:
        """
        Generate emergency guidance
        
        Args:
            issue: Type of emergency
            
        Returns:
            Emergency protocol
        """
        protocols = {
            "engine_failure": "🔴 ENGINE FAILURE - Park the car NOW. Box immediately, we're done.",
            "brake_failure": "🔴 BRAKE FAILURE - Downshift, manage. Get into the pit carefully.",
            "puncture": "🔴 PUNCTURE - Gently to the pit. We can recover with a stop.",
            "temperature": "🟡 TEMPS HIGH - Cool it down. Ease off the power, manage water.",
            "fuel_pump": "🔴 FUEL PUMP - We're out of fuel. Cruise to finish line.",
        }
        return protocols.get(issue, "Contact the pit immediately for guidance.")
