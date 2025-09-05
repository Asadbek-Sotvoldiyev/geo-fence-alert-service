import json
from celery import shared_task
from django.utils import timezone
from main.models.base import GeoEvent


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
        
        print(f"Publishing geo-event message: {json.dumps(message, indent=2)}")
        
        event.message_sent = True
        event.save(update_fields=['message_sent'])
        
        print(f"Successfully published event {event_id}")
        return f"Event {event_id} published successfully"
        
        
    except Exception as exc:
        print("Error: ", exc)
