from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.utils import timezone
from main.models.base import GeoFence, Device, GeoEvent
from .serializers import (
    LocationCheckSerializer, GeoFenceSerializer, 
    DeviceSerializer, GeoEventSerializer
)
from .services import GeofenceService


@method_decorator(csrf_exempt, name='dispatch')
class LocationCheckView(APIView):
    
    def post(self, request):
        try:
            serializer = LocationCheckSerializer(data=request.data)
            
            if not serializer.is_valid():
                return Response(
                    {'error': 'Invalid input', 'details': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            device_id = serializer.validated_data['device_id']
            lat = float(serializer.validated_data['lat'])
            lon = float(serializer.validated_data['lon'])
            
            result = GeofenceService.check_location(device_id, lat, lon)
            
            return Response(result, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': 'Internal server error', 'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DeviceStatusView(APIView):
    
    def get(self, request, device_id):
        try:
            result = GeofenceService.get_device_status(device_id)
            return Response(result, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': 'Internal server error', 'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GeoFenceListCreateView(generics.ListCreateAPIView):
    queryset = GeoFence.objects.all()
    serializer_class = GeoFenceSerializer


class GeoFenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GeoFence.objects.all()
    serializer_class = GeoFenceSerializer


class DeviceListCreateView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class GeoEventListView(generics.ListAPIView):
    serializer_class = GeoEventSerializer
    
    def get_queryset(self):
        queryset = GeoEvent.objects.select_related('geofence')
        device_id = self.request.query_params.get('device_id', None)
        
        if device_id:
            queryset = queryset.filter(device_id=device_id)
            
        limit = int(self.request.query_params.get('limit', 50))
        return queryset[:limit]


@api_view(['GET'])
def health_check(request):
    return Response({
        'status': 'healthy',
        'service': 'Geo-fence Alert Service',
        'version': '1.0.0'
    })


@api_view(['GET'])
def service_stats(request):
    try:
        stats = {
            'total_geofences': GeoFence.objects.count(),
            'total_devices': Device.objects.count(),
            'total_events': GeoEvent.objects.count(),
            'recent_events_24h': GeoEvent.objects.filter(
                timestamp__gte=timezone.now() - timezone.timedelta(hours=24)
            ).count()
        }
        return Response(stats)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )