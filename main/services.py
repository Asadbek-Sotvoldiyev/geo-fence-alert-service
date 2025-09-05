import logging
from typing import List, Dict, Any, Optional
from django.utils import timezone
from main.models.base import GeoFence, DeviceStatus, GeoEvent
from .tasks import publish_geo_event


class GeofenceService:
    
    @staticmethod
    def check_location(device_id: str, lat: float, lon: float) -> Dict[str, Any]:
        try:
            geofences = GeoFence.objects.all()
            
            current_inside_fences = []
            events_triggered = []
            
            for geofence in geofences:
                is_inside = geofence.is_point_inside(lat, lon)
                
                if is_inside:
                    current_inside_fences.append(geofence)
                
                device_status, created = DeviceStatus.objects.get_or_create(
                    device_id=device_id,
                    geofence=geofence,
                    defaults={
                        'is_inside': is_inside,
                        'last_lat': lat,
                        'last_lon': lon
                    }
                )
                
                if created:
                    if is_inside:
                        event = GeofenceService._create_geo_event(
                            device_id, geofence, 'entry', lat, lon
                        )
                        events_triggered.append(event)
                        GeofenceService._publish_event_async(event)
                        
                elif device_status.is_inside != is_inside:
                    event_type = 'entry' if is_inside else 'exit'
                    event = GeofenceService._create_geo_event(
                        device_id, geofence, event_type, lat, lon
                    )
                    events_triggered.append(event)
                    GeofenceService._publish_event_async(event)
                
                device_status.is_inside = is_inside
                device_status.last_lat = lat
                device_status.last_lon = lon
                device_status.save()
            
            return {
                'device_id': device_id,
                'location': {'lat': lat, 'lon': lon},
                'inside_geofences': [
                    {
                        'id': gf.id,
                        'name': gf.name,
                        'distance_from_center': round(gf.calculate_distance(lat, lon), 3)
                    }
                    for gf in current_inside_fences
                ],
                'events_triggered': len(events_triggered),
                'timestamp': timezone.now().isoformat()
            }
            
        except Exception as e:
            pass
    
    @staticmethod
    def _create_geo_event(device_id: str, geofence: GeoFence, event_type: str, 
                         lat: float, lon: float) -> GeoEvent:
        event = GeoEvent.objects.create(
            device_id=device_id,
            geofence=geofence,
            event_type=event_type,
            lat=lat,
            lon=lon
        )
        return event
    
    @staticmethod
    def _publish_event_async(event: GeoEvent):
        try:
            publish_geo_event.delay(event.id)
        except Exception as e:
            pass
        
    @staticmethod
    def get_device_status(device_id: str) -> Dict[str, Any]:
        statuses = DeviceStatus.objects.filter(device_id=device_id).select_related('geofence')
        
        return {
            'device_id': device_id,
            'geofence_statuses': [
                {
                    'geofence_id': status.geofence.id,
                    'geofence_name': status.geofence.name,
                    'is_inside': status.is_inside,
                    'last_position': {
                        'lat': float(status.last_lat) if status.last_lat else None,
                        'lon': float(status.last_lon) if status.last_lon else None
                    },
                    'last_checked': status.last_checked.isoformat() if status.last_checked else None
                }
                for status in statuses
            ]
        }
    
    @staticmethod
    def get_recent_events(device_id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        events_query = GeoEvent.objects.select_related('geofence')
        
        if device_id:
            events_query = events_query.filter(device_id=device_id)
            
        events = events_query[:limit]
        
        return [
            {
                'id': event.id,
                'device_id': event.device_id,
                'geofence_name': event.geofence.name,
                'event_type': event.event_type,
                'location': {
                    'lat': float(event.lat),
                    'lon': float(event.lon)
                },
                'timestamp': event.timestamp.isoformat(),
                'message_sent': event.message_sent
            }
            for event in events
        ]