from django.urls import path

from uzbekistan.views import RegionListAPIView, DistrictListAPIView

urlpatterns = [
    path('regions/', RegionListAPIView.as_view(), name='region-list'),
    path('districts/<int:region_id>/', DistrictListAPIView.as_view(), name='district-list'),
]
