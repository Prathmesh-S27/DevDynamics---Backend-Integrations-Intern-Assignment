import httpx
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from src.core.config import settings
import asyncio

class WeatherService:
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.onecall_url = "https://api.openweathermap.org/data/3.0/onecall"
    
    async def get_current_weather(self, location: str) -> Dict:
        """Get current weather for a location"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/weather",
                    params={
                        "q": location,
                        "appid": self.api_key,
                        "units": "metric"
                    }
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError:
                return {"error": "Failed to fetch weather data"}
    
    async def get_forecast(self, location: str) -> Dict:
        """Get 5-day forecast for a location"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/forecast",
                    params={
                        "q": location,
                        "appid": self.api_key,
                        "units": "metric"
                    }
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError:
                return {"error": "Failed to fetch forecast data"}
    
    async def get_historical_weather(self, lat: float, lon: float, dt: int) -> Dict:
        """Get historical weather data for a specific date"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.onecall_url}/timemachine",
                    params={
                        "lat": lat,
                        "lon": lon,
                        "dt": dt,
                        "appid": self.api_key,
                        "units": "metric"
                    }
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError:
                return {"error": "Failed to fetch historical weather data"}
    
    async def get_hourly_forecast(self, location: str) -> Dict:
        """Get detailed hourly forecast for next 48 hours"""
        # First get coordinates
        coord_data = await self.get_coordinates(location)
        if "error" in coord_data:
            return coord_data
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.onecall_url}",
                    params={
                        "lat": coord_data["lat"],
                        "lon": coord_data["lon"],
                        "appid": self.api_key,
                        "units": "metric",
                        "exclude": "minutely,alerts"
                    }
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError:
                return {"error": "Failed to fetch hourly forecast"}
    
    async def get_coordinates(self, location: str) -> Dict:
        """Get coordinates for a location"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"http://api.openweathermap.org/geo/1.0/direct",
                    params={
                        "q": location,
                        "limit": 1,
                        "appid": self.api_key
                    }
                )
                response.raise_for_status()
                data = response.json()
                if data:
                    return {"lat": data[0]["lat"], "lon": data[0]["lon"]}
                return {"error": "Location not found"}
            except httpx.HTTPError:
                return {"error": "Failed to get coordinates"}
    
    async def get_weather_for_event_duration(self, location: str, start_time: datetime, end_time: datetime) -> Dict:
        """Get hour-by-hour weather for event duration"""
        hourly_data = await self.get_hourly_forecast(location)
        if "error" in hourly_data:
            return hourly_data
        
        event_weather = []
        for hour_data in hourly_data.get("hourly", []):
            hour_time = datetime.fromtimestamp(hour_data["dt"])
            if start_time <= hour_time <= end_time:
                event_weather.append({
                    "time": hour_time.isoformat(),
                    "temperature": hour_data["temp"],
                    "feels_like": hour_data["feels_like"],
                    "humidity": hour_data["humidity"],
                    "weather": hour_data["weather"][0]["description"],
                    "precipitation_probability": hour_data.get("pop", 0) * 100,
                    "wind_speed": hour_data["wind_speed"]
                })
        
        return {
            "location": location,
            "event_duration": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat()
            },
            "hourly_weather": event_weather
        }
    
    async def analyze_weather_trends(self, location: str, target_date: datetime) -> Dict:
        """Analyze if weather is improving or worsening"""
        forecast_data = await self.get_forecast(location)
        if "error" in forecast_data:
            return forecast_data
        
        trend_analysis = []
        scores = []
        
        for item in forecast_data.get("list", [])[:8]:  # Next 24 hours (8 x 3-hour intervals)
            forecast_time = datetime.fromtimestamp(item["dt"])
            analysis = self.analyze_weather_suitability(item, "outdoor")
            scores.append(analysis["score"])
            trend_analysis.append({
                "time": forecast_time.isoformat(),
                "score": analysis["score"],
                "conditions": analysis["weather_summary"]
            })
        
        # Calculate trend
        if len(scores) >= 3:
            early_avg = sum(scores[:3]) / 3
            late_avg = sum(scores[-3:]) / 3
            trend = "improving" if late_avg > early_avg else "worsening" if late_avg < early_avg else "stable"
        else:
            trend = "insufficient_data"
        
        return {
            "location": location,
            "trend": trend,
            "score_change": scores[-1] - scores[0] if len(scores) >= 2 else 0,
            "detailed_forecast": trend_analysis
        }
    
    async def compare_nearby_locations(self, base_location: str, radius_km: int = 50) -> Dict:
        """Compare weather across nearby cities within reasonable distance"""
        # Updated nearby cities mapping with realistic distances (within ~100-200km)
        nearby_cities = {
            # Maharashtra, India
            "mumbai": ["Pune", "Nashik", "Thane", "Navi Mumbai"],
            "pune": ["Mumbai", "Nashik", "Satara", "Kolhapur"],
            "nashik": ["Mumbai", "Pune", "Aurangabad", "Ahmednagar"],
            
            # Delhi NCR, India
            "delhi": ["Gurgaon", "Noida", "Faridabad", "Ghaziabad"],
            "gurgaon": ["Delhi", "Noida", "Faridabad", "Manesar"],
            "noida": ["Delhi", "Gurgaon", "Ghaziabad", "Greater Noida"],
            
            # Karnataka, India
            "bangalore": ["Mysore", "Tumkur", "Kolar", "Mandya"],
            "mysore": ["Bangalore", "Mandya", "Hassan", "Chamarajanagar"],
            
            # Tamil Nadu, India
            "chennai": ["Vellore", "Kanchipuram", "Tiruvallur", "Chengalpattu"],
            "coimbatore": ["Tirupur", "Salem", "Erode", "Pollachi"],
            
            # Telangana & Andhra Pradesh, India
            "hyderabad": ["Secunderabad", "Warangal", "Nizamabad", "Karimnagar"],
            "vijayawada": ["Guntur", "Eluru", "Machilipatnam", "Tenali"],
            
            # West Bengal, India
            "kolkata": ["Howrah", "Durgapur", "Asansol", "Siliguri"],
            
            # Gujarat, India
            "ahmedabad": ["Gandhinagar", "Vadodara", "Anand", "Mehsana"],
            "surat": ["Vadodara", "Bharuch", "Navsari", "Valsad"],
            
            # Rajasthan, India
            "jaipur": ["Ajmer", "Alwar", "Sikar", "Tonk"],
            "udaipur": ["Chittorgarh", "Rajsamand", "Bhilwara", "Banswara"],
            
            # UK
            "london": ["Oxford", "Cambridge", "Reading", "Brighton"],
            "manchester": ["Liverpool", "Preston", "Bolton", "Stockport"],
            "birmingham": ["Coventry", "Wolverhampton", "Worcester", "Warwick"],
            
            # USA - East Coast
            "new york": ["Newark", "Jersey City", "Stamford", "White Plains"],
            "boston": ["Cambridge", "Worcester", "Providence", "Lowell"],
            "philadelphia": ["Camden", "Wilmington", "Trenton", "Reading"],
            
            # USA - West Coast
            "los angeles": ["Santa Monica", "Pasadena", "Long Beach", "Anaheim"],
            "san francisco": ["Oakland", "San Jose", "Berkeley", "Fremont"],
            "seattle": ["Tacoma", "Bellevue", "Everett", "Renton"],
            
            # Canada
            "toronto": ["Mississauga", "Brampton", "Markham", "Vaughan"],
            "vancouver": ["Burnaby", "Richmond", "Surrey", "Coquitlam"],
            "montreal": ["Laval", "Longueuil", "Gatineau", "Sherbrooke"],
            
            # Australia
            "sydney": ["Parramatta", "Newcastle", "Wollongong", "Penrith"],
            "melbourne": ["Geelong", "Ballarat", "Bendigo", "Frankston"],
            
            # Europe
            "paris": ["Versailles", "Meaux", "Melun", "Pontoise"],
            "berlin": ["Potsdam", "Brandenburg", "Cottbus", "Frankfurt Oder"],
            "madrid": ["Toledo", "Segovia", "Guadalajara", "Alcala de Henares"],
            
            # Asia
            "tokyo": ["Yokohama", "Kawasaki", "Saitama", "Chiba"],
            "osaka": ["Kyoto", "Kobe", "Nara", "Wakayama"],
            "singapore": ["Johor Bahru", "Malacca", "Batam", "Seremban"],
            
            # Middle East
            "dubai": ["Sharjah", "Ajman", "Abu Dhabi", "Al Ain"],
            "riyadh": ["Jeddah", "Dammam", "Mecca", "Medina"]
        }
        
        base_location_lower = base_location.lower().strip()
        cities_to_check = []
        
        # Find nearby cities for the base location
        for city, nearby in nearby_cities.items():
            if city in base_location_lower or base_location_lower in city:
                # Filter out the base location itself from nearby cities
                filtered_nearby = [c for c in nearby if c.lower() not in base_location_lower and base_location_lower not in c.lower()]
                cities_to_check.extend(filtered_nearby[:3])  # Limit to 3 nearby cities
                break
        
        # If no exact match, try partial matching for major cities
        if not cities_to_check:
            for city, nearby in nearby_cities.items():
                if any(word in base_location_lower for word in city.split()) or any(word in city for word in base_location_lower.split()):
                    filtered_nearby = [c for c in nearby if c.lower() not in base_location_lower and base_location_lower not in c.lower()]
                    cities_to_check.extend(filtered_nearby[:3])
                    break
        
        # If still no cities found, return just the base location
        if not cities_to_check:
            weather_data = await self.get_current_weather(base_location)
            if "error" not in weather_data:
                analysis = self.analyze_weather_suitability(weather_data, "outdoor")
                return {
                    "base_location": base_location,
                    "comparison": [{
                        "city": base_location,
                        "score": analysis["score"],
                        "suitability": analysis["suitability"],
                        "temperature": weather_data.get("main", {}).get("temp", 0),
                        "conditions": weather_data.get("weather", [{}])[0].get("description", ""),
                        "is_base": True
                    }],
                    "best_alternative": None,
                    "message": f"No nearby cities found within reasonable distance of {base_location}"
                }
        
        weather_comparison = []
        
        # Add base location first
        base_weather = await self.get_current_weather(base_location)
        if "error" not in base_weather:
            base_analysis = self.analyze_weather_suitability(base_weather, "outdoor")
            weather_comparison.append({
                "city": base_location,
                "score": base_analysis["score"],
                "suitability": base_analysis["suitability"],
                "temperature": base_weather.get("main", {}).get("temp", 0),
                "conditions": base_weather.get("weather", [{}])[0].get("description", ""),
                "is_base": True,
                "distance": "0 km"
            })
        
        # Check nearby cities
        for city in cities_to_check:
            weather_data = await self.get_current_weather(city)
            if "error" not in weather_data:
                analysis = self.analyze_weather_suitability(weather_data, "outdoor")
                weather_comparison.append({
                    "city": city,
                    "score": analysis["score"],
                    "suitability": analysis["suitability"],
                    "temperature": weather_data.get("main", {}).get("temp", 0),
                    "conditions": weather_data.get("weather", [{}])[0].get("description", ""),
                    "is_base": False,
                    "distance": "~50-150 km"  # Approximate distance range
                })
        
        # Sort by weather score (best first)
        weather_comparison.sort(key=lambda x: x["score"], reverse=True)
        
        # Find best alternative (not the base location)
        best_alternative = None
        for location in weather_comparison:
            if not location.get("is_base", False):
                best_alternative = location
                break
        
        return {
            "base_location": base_location,
            "comparison": weather_comparison,
            "best_alternative": best_alternative,
            "note": "Showing weather for nearby cities within 50-150 km radius"
        }

    def analyze_weather_suitability(self, weather_data: Dict, event_type: str) -> Dict:
        """Analyze weather suitability for event type"""
        if "error" in weather_data:
            return {"suitability": "Unknown", "score": 0, "reasons": ["Weather data unavailable"]}
        
        temp = weather_data.get("main", {}).get("temp", 0)
        precipitation = weather_data.get("rain", {}).get("1h", 0) + weather_data.get("snow", {}).get("1h", 0)
        wind_speed = weather_data.get("wind", {}).get("speed", 0)
        weather_condition = weather_data.get("weather", [{}])[0].get("main", "").lower()
        
        score = 100
        reasons = []
        
        # Temperature scoring
        if event_type.lower() in ["outdoor", "sports", "festival"]:
            if temp < 0 or temp > 35:
                score -= 30
                reasons.append(f"Extreme temperature: {temp}°C")
            elif temp < 10 or temp > 30:
                score -= 15
                reasons.append(f"Uncomfortable temperature: {temp}°C")
        
        # Precipitation scoring
        if precipitation > 0:
            if event_type.lower() in ["outdoor", "sports", "festival"]:
                score -= 40
                reasons.append(f"Precipitation expected: {precipitation}mm")
            else:
                score -= 10
                reasons.append(f"Light precipitation: {precipitation}mm")
        
        # Wind scoring
        if wind_speed > 10:
            score -= 20
            reasons.append(f"High wind speed: {wind_speed} m/s")
        
        # Weather condition scoring
        if weather_condition in ["thunderstorm", "snow"]:
            score -= 50
            reasons.append(f"Severe weather: {weather_condition}")
        elif weather_condition in ["rain", "drizzle"]:
            score -= 25
            reasons.append(f"Wet conditions: {weather_condition}")
        
        # Determine suitability level
        if score >= 80:
            suitability = "Good"
        elif score >= 60:
            suitability = "Okay"
        else:
            suitability = "Poor"
        
        return {
            "suitability": suitability,
            "score": max(0, score),
            "reasons": reasons,
            "weather_summary": {
                "temperature": temp,
                "precipitation": precipitation,
                "wind_speed": wind_speed,
                "condition": weather_condition
            }
        }
    
    async def get_alternative_dates(self, location: str, target_date: datetime, event_type: str) -> List[Dict]:
        """Get alternative dates with better weather within a week"""
        alternatives = []
        forecast_data = await self.get_forecast(location)
        
        if "error" in forecast_data:
            return alternatives
        
        for item in forecast_data.get("list", []):
            forecast_date = datetime.fromtimestamp(item["dt"])
            if forecast_date.date() != target_date.date():
                analysis = self.analyze_weather_suitability(item, event_type)
                if analysis["score"] > 70:  # Only suggest good weather days
                    alternatives.append({
                        "date": forecast_date.isoformat(),
                        "suitability": analysis["suitability"],
                        "score": analysis["score"],
                        "weather_summary": analysis["weather_summary"]
                    })
        
        return sorted(alternatives, key=lambda x: x["score"], reverse=True)[:3]
