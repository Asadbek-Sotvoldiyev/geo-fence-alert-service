from django.urls import path
from . import views

app_name = 'geofence'

urlpatterns = [
    path('location-check/', views.LocationCheckView.as_view(), name='location-check'),
    
    path('devices/', views.DeviceListCreateView.as_view(), name='device-list-create'),
    path('device/<str:device_id>/status/', views.DeviceStatusView.as_view(), name='device-status'),
    
    path('geofences/', views.GeoFenceListCreateView.as_view(), name='geofence-list-create'),
    path('geofences/<int:pk>/', views.GeoFenceDetailView.as_view(), name='geofence-detail'),
    
    path('events/', views.GeoEventListView.as_view(), name='event-list'),
]