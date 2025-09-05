from rest_framework import serializers
from main.models.base import GeoFence, Device, GeoEvent


class LocationCheckSerializer(serializers.Serializer):
    device_id = serializers.CharField(max_length=100)
    lat = serializers.DecimalField(max_digits=10, decimal_places=7)
    lon = serializers.DecimalField(max_digits=10, decimal_places=7)


class GeoFenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoFence
        fields = ['id', 'name', 'center_lat', 'center_lon', 'radius_km', 'created_at']


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'device_id', 'name', 'device_type', 'created_at']


class GeoEventSerializer(serializers.ModelSerializer):
    geofence_name = serializers.CharField(source='geofence.name', read_only=True)
    
    class Meta:
        model = GeoEvent
        fields = ['id', 'device_id', 'geofence', 'geofence_name', 'event_type', 
                 'lat', 'lon', 'timestamp', 'message_sent']
