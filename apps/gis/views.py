# gis/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .adress_processor import AddressProcessor
from .models import GISMasterClass
from .serializer import GISMasterClassSerializer


class GISMasterClassViewSet(viewsets.ModelViewSet):
    queryset = GISMasterClass.objects.all()
    serializer_class = GISMasterClassSerializer

    @action(detail=False, methods=['post'])
    def update_coordinates(self, request, *args, **kwargs):
        processor = AddressProcessor()
        updated_count = 0

        for gis_masterclass in self.get_queryset().filter(latitude__isnull=True, longitude__isnull=True).exclude(
                location_name__iexact='Address not specified'):
            lat, lon = processor.process_address(gis_masterclass.location_name)
            if lat and lon:
                gis_masterclass.latitude = lat
                gis_masterclass.longitude = lon
                gis_masterclass.save()
                updated_count += 1

        return Response({
            'message': 'Updated coordinates for GIS Master Classes',
            'updated_count': updated_count
        }, status=status.HTTP_200_OK)
