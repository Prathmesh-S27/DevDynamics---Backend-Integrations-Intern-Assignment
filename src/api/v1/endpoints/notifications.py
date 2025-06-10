from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.services.notification_service import NotificationService
from src.core.database import get_db
from typing import List

router = APIRouter()

@router.get("/weather-alerts", response_model=List[dict])
async def get_weather_change_alerts(db: Session = Depends(get_db)):
    """Get weather change alerts for upcoming events"""
    notification_service = NotificationService(db)
    return await notification_service.check_weather_changes_for_events()

@router.get("/event-reminders", response_model=List[dict])
async def get_event_reminders(db: Session = Depends(get_db)):
    """Get day-before weather summaries for tomorrow's events"""
    notification_service = NotificationService(db)
    return await notification_service.generate_event_reminders()

@router.post("/send-alerts")
async def send_weather_alerts(db: Session = Depends(get_db)):
    """Manually trigger sending of weather alerts"""
    notification_service = NotificationService(db)
    alerts = await notification_service.check_weather_changes_for_events()
    
    # In a real implementation, this would send actual emails/SMS
    sent_count = 0
    for alert in alerts:
        # Simulate sending notification
        success = await notification_service.send_email_notification(
            "user@example.com",  # Would get actual user email from database
            f"Weather Alert for {alert['event_title']}",
            f"Weather conditions have changed for your event. New suitability: {alert['current_suitability']}"
        )
        if success:
            sent_count += 1
    
    return {"alerts_sent": sent_count, "total_alerts": len(alerts)}
