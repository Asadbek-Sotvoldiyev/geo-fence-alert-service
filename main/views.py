from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from main.models.base import GeoFence, Device, GeoEvent
from .serializers import (
    LocationCheckSerializer, GeoFenceSerializer, 
    DeviceSerializer, GeoEventSerializer
)
from .services import GeofenceService
from drf_yasg.utils import swagger_auto_schema


class LocationCheckView(APIView):
    
    @swagger_auto_schema(request_body=LocationCheckSerializer)
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