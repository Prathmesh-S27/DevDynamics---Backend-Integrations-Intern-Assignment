from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.models.event import Event
from src.models.user import User
from src.services.weather_service import WeatherService
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.core.config import settings

class NotificationService:
    def __init__(self, db: Session):
        self.db = db
        self.weather_service = WeatherService()
    
    async def check_weather_changes_for_events(self) -> List[Dict]:
        """Check for significant weather changes for upcoming events"""
        # Get events in the next 7 days
        upcoming_events = self.db.query(Event).filter(
            Event.start_time >= datetime.utcnow(),
            Event.start_time <= datetime.utcnow() + timedelta(days=7)
        ).all()
        
        notifications = []
        
        for event in upcoming_events:
            # Get current weather analysis
            current_weather = await self.weather_service.get_current_weather(event.location)
            current_analysis = self.weather_service.analyze_weather_suitability(current_weather, event.event_type)
            
            # Compare with stored weather data if available
            if event.weather_data and "analysis" in event.weather_data:
                stored_analysis = event.weather_data["analysis"]
                score_change = current_analysis["score"] - stored_analysis["score"]
                
                # Significant change threshold (20 points)
                if abs(score_change) >= 20:
                    notifications.append({
                        "event_id": event.id,
                        "event_title": event.title,
                        "location": event.location,
                        "start_time": event.start_time.isoformat(),
                        "change_type": "improvement" if score_change > 0 else "deterioration",
                        "score_change": score_change,
                        "current_suitability": current_analysis["suitability"],
                        "previous_suitability": stored_analysis["suitability"],
                        "notification_type": "weather_change_alert"
                    })
        
        return notifications
    
    async def generate_event_reminders(self) -> List[Dict]:
        """Generate day-before weather summaries for upcoming events"""
        # Get events happening tomorrow
        tomorrow_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        tomorrow_end = tomorrow_start + timedelta(days=1)
        
        tomorrow_events = self.db.query(Event).filter(
            Event.start_time >= tomorrow_start,
            Event.start_time < tomorrow_end
        ).all()
        
        reminders = []
        
        for event in tomorrow_events:
            weather_data = await self.weather_service.get_current_weather(event.location)
            analysis = self.weather_service.analyze_weather_suitability(weather_data, event.event_type)
            
            # Get hourly forecast for event duration
            hourly_forecast = await self.weather_service.get_weather_for_event_duration(
                event.location, event.start_time, event.end_time
            )
            
            reminders.append({
                "event_id": event.id,
                "event_title": event.title,
                "location": event.location,
                "start_time": event.start_time.isoformat(),
                "end_time": event.end_time.isoformat(),
                "weather_summary": analysis,
                "hourly_forecast": hourly_forecast.get("hourly_weather", []),
                "notification_type": "event_reminder"
            })
        
        return reminders
    
    async def get_rescheduling_recommendations(self, event_id: int) -> Dict:
        """Get automatic rescheduling recommendations for poor weather events"""
        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return {"error": "Event not found"}
        
        # Check current weather suitability
        weather_data = await self.weather_service.get_current_weather(event.location)
        analysis = self.weather_service.analyze_weather_suitability(weather_data, event.event_type)
        
        if analysis["score"] >= 70:  # Weather is acceptable
            return {"message": "Current weather is suitable for the event"}
        
        # Get alternative dates
        alternatives = await self.weather_service.get_alternative_dates(
            event.location, event.start_time, event.event_type
        )
        
        # Get nearby location alternatives
        nearby_comparison = await self.weather_service.compare_nearby_locations(event.location)
        
        return {
            "event_id": event_id,
            "current_suitability": analysis,
            "recommendations": {
                "alternative_dates": alternatives,
                "alternative_locations": nearby_comparison.get("comparison", [])[:3],
                "best_date_alternative": alternatives[0] if alternatives else None,
                "best_location_alternative": nearby_comparison.get("best_alternative")
            },
            "notification_type": "rescheduling_recommendation"
        }
    
    def check_threshold_alerts(self, event_id: int, custom_thresholds: Dict) -> Dict:
        """Check if weather conditions meet custom threshold alerts"""
        # Implementation for custom threshold checking
        # This would be expanded based on user-defined thresholds
        pass
    
    async def send_email_notification(self, to_email: str, subject: str, content: str) -> bool:
        """Send email notification (basic implementation)"""
        try:
            # This is a basic implementation - in production, use a proper email service
            msg = MIMEMultipart()
            msg['From'] = settings.SMTP_EMAIL
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(content, 'plain'))
            
            # Note: This requires SMTP configuration in settings
            # For now, we'll just log the notification
            print(f"Email notification: {subject} to {to_email}")
            print(f"Content: {content}")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
