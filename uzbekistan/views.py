from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from uzbekistan.dynamic_importer import get_cache_settings
from uzbekistan.filters import RegionFilterSet, DistrictFilterSet, VillageFilterSet
from uzbekistan.models import Region, District, Village, check_model
from uzbekistan.serializers import (
    RegionModelSerializer,
    DistrictModelSerializer,
    VillageModelSerializer,
)


class BaseLocationView(ListAPIView):
    """Base view for all location-based views with common functionality."""

    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    model: type[Region | District | Village] | None = None
    select_related_fields: list[str] = []

    # URL configuration
    url_path = ""
    url_name = ""
    url_relation = ""

    def get_queryset(self):
        check_model(self.model)
        queryset = self.model.objects.all()

        if hasattr(self, "url_relation") and self.url_relation:
            filter_kwargs = {self.url_relation: self.kwargs[self.url_relation]}
            queryset = queryset.filter(**filter_kwargs)

        return queryset.select_related(*self.select_related_fields)

    def list(self, request, *args, **kwargs):
        cache_settings = get_cache_settings()

        if not cache_settings["enabled"]:
            return super().list(request, *args, **kwargs)

        cache_key = f"{self.__class__.__name__}_{request.query_params}"
        cached_response = cache.get(cache_key)

        if cached_response:
            return Response(cached_response)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=cache_settings["timeout"])
        return response


class RegionListAPIView(BaseLocationView):
    serializer_class = RegionModelSerializer
    filterset_class = RegionFilterSet
    url_path = "regions"
    url_name = "region-list"
    url_relation = None
    model = Region
    select_related_fields = []


class DistrictListAPIView(BaseLocationView):
    serializer_class = DistrictModelSerializer
    filterset_class = DistrictFilterSet
    url_path = "districts"
    url_name = "district-list"
    url_relation = "region_id"
    model = District
    select_related_fields = ["region"]


class VillageListAPIView(BaseLocationView):
    serializer_class = VillageModelSerializer
    filterset_class = VillageFilterSet
    url_path = "villages"
    url_name = "village-list"
    url_relation = "district_id"
    model = Village
    select_related_fields = ["district", "district__region"]
