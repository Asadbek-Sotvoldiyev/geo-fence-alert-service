from django.db import models
import math

class GeoFence(models.Model):
    name = models.CharField(max_length=255)
    center_lat = models.DecimalField(max_digits=10, decimal_places=7)
    center_lon = models.DecimalField(max_digits=10, decimal_places=7)
    radius_km = models.DecimalField(max_digits=8, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Radius: {self.radius_km}km)"

    def is_point_inside(self, lat, lon):
        return self.calculate_distance(lat, lon) <= float(self.radius_km)

    def calculate_distance(self, lat, lon):
        R = 6371.0

        lat1_rad = math.radians(float(self.center_lat))
        lon1_rad = math.radians(float(self.center_lon))
        lat2_rad = math.radians(lat)
        lon2_rad = math.radians(lon)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        distance = R * c
        return distance


class Device(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    device_type = models.CharField(max_length=100, choices=[
        ('tractor', 'Tractor'),
        ('plough', 'Plough'),
        ('harvester', 'Harvester'),
        ('seeder', 'Seeder'),
        ('other', 'Other'),
    ], default='other')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.device_id})"


class DeviceStatus(models.Model):
    device_id = models.CharField(max_length=100, db_index=True)
    geofence = models.ForeignKey(GeoFence, on_delete=models.CASCADE, null=True, blank=True)
    is_inside = models.BooleanField(default=False)
    last_lat = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    last_lon = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    last_checked = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['device_id', 'geofence']

    def __str__(self):
        status = "Inside" if self.is_inside else "Outside"
        geofence_name = self.geofence.name if self.geofence else "No Geofence"
        return f"{self.device_id} - {geofence_name}: {status}"


class GeoEvent(models.Model):
    device_id = models.CharField(max_length=100, db_index=True)
    geofence = models.ForeignKey(GeoFence, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=20, choices=[
        ('entry', 'Entry'),
        ('exit', 'Exit'),
    ])
    lat = models.DecimalField(max_digits=10, decimal_places=7)
    lon = models.DecimalField(max_digits=10, decimal_places=7)
    timestamp = models.DateTimeField(auto_now_add=True)
    message_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.device_id} {self.event_type} {self.geofence.name} at {self.timestamp}"