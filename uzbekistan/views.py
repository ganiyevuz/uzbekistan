from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from uzbekistan.models import Region, District
from uzbekistan.serializers import RegionModelSerializer, DistrictModelSerializer
from uzbekistan.utils import RegionFilterSet, DistrictFilterSet


class RegionListAPIView(ListAPIView):
    serializer_class = RegionModelSerializer
    queryset = Region.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RegionFilterSet
    pagination_class = None


class DistrictListAPIView(ListAPIView):
    serializer_class = DistrictModelSerializer
    queryset = District.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DistrictFilterSet
    pagination_class = None

    def get_queryset(self):
        return District.objects.filter(region_id=self.kwargs['region_id'])
