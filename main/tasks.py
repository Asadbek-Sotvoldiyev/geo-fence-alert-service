import json
import logging
from celery import shared_task
from django.utils import timezone
from main.models.base import GeoEvent

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def publish_geo_event(self, event_id):
    try:
        event = GeoEvent.objects.get(id=event_id)
        
        message = {
            'event_id': event.id,
            'device_id': event.device_id,
            'geofence': {
                'id': event.geofence.id,
                'name': event.geofence.name,
                'center_lat': float(event.geofence.center_lat),
                'center_lon': float(event.geofence.center_lon),
                'radius_km': float(event.geofence.radius_km)
            },
            'event_type': event.event_type,
            'location': {
                'lat': float(event.lat),
                'lon': float(event.lon)
            },
            'timestamp': event.timestamp.isoformat(),
            'message_timestamp': timezone.now().isoformat()
        }
        
        logger.info(f"Publishing geo-event message: {json.dumps(message, indent=2)}")
        
        event.message_sent = True
        event.save(update_fields=['message_sent'])
        
        logger.info(f"Successfully published event {event_id}")
        return f"Event {event_id} published successfully"
        
    except GeoEvent.DoesNotExist:
        logger.error(f"GeoEvent {event_id} not found")
        raise
        
    except Exception as exc:
        logger.error(f"Failed to publish event {event_id}: {str(exc)}")
        
        if self.request.retries < self.max_retries:
            countdown = 2 ** self.request.retries
            logger.info(f"Retrying event {event_id} in {countdown} seconds")
            raise self.retry(countdown=countdown, exc=exc)
        else:
            logger.error(f"Max retries exceeded for event {event_id}")
            raise

@shared_task
def cleanup_old_events(days_old=30):
    try:
        cutoff_date = timezone.now() - timezone.timedelta(days=days_old)
        deleted_count = GeoEvent.objects.filter(timestamp__lt=cutoff_date).delete()[0]
        
        logger.info(f"Cleaned up {deleted_count} geo events older than {days_old} days")
        return f"Cleaned up {deleted_count} events"
        
    except Exception as exc:
        logger.error(f"Failed to cleanup old events: {str(exc)}")
        raise

@shared_task
def health_check():
    return {
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'message': 'Celery worker is operational'
    }