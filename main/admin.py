from django.contrib import admin
from unfold.admin import ModelAdmin
from main.models.base import GeoFence, Device, DeviceStatus, GeoEvent


@admin.register(GeoFence)
class GeoFenceAdmin(ModelAdmin):
    list_display = ['name', 'center_lat', 'center_lon', 'radius_km', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']
    ordering = ['-created_at']


@admin.register(Device)
class DeviceAdmin(ModelAdmin):
    list_display = ['device_id', 'name', 'device_type', 'created_at']
    search_fields = ['device_id', 'name']
    list_filter = ['device_type', 'created_at']
    ordering = ['-created_at']


@admin.register(DeviceStatus)
class DeviceStatusAdmin(ModelAdmin):
    list_display = ['device_id', 'geofence', 'is_inside', 'last_lat', 'last_lon', 'last_checked']
    search_fields = ['device_id', 'geofence__name']
    list_filter = ['is_inside', 'last_checked', 'geofence']
    ordering = ['-last_checked']


@admin.register(GeoEvent)
class GeoEventAdmin(ModelAdmin):
    list_display = ['device_id', 'geofence', 'event_type', 'lat', 'lon', 'timestamp', 'message_sent']
    search_fields = ['device_id', 'geofence__name']
    list_filter = ['event_type', 'message_sent', 'timestamp', 'geofence']
    ordering = ['-timestamp']
    readonly_fields = ['timestamp']