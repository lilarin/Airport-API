from django_filters.rest_framework import filters
from django_filters import FilterSet


class NameFilter(FilterSet):
    name = filters.CharFilter(
        field_name="name", lookup_expr="icontains"
    )


class AirportFilter(FilterSet):
    name = filters.CharFilter(
        field_name='name', lookup_expr='icontains'
    )
    city_name = filters.CharFilter(
        field_name='city__name', lookup_expr='icontains'
    )
    country_name = filters.CharFilter(
        field_name='country__name', lookup_expr='icontains'
    )


class FlightFilter(FilterSet):
    name = filters.CharFilter(
        field_name='name', lookup_expr='icontains'
    )
    city_name = filters.CharFilter(
        field_name='city__name', lookup_expr='icontains'
    )
    country_name = filters.CharFilter(
        field_name='country__name', lookup_expr='icontains'
    )


