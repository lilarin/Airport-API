from django_filters.rest_framework import filters
from django_filters import FilterSet


class NameFilter(FilterSet):
    name = filters.CharFilter(
        field_name="name", lookup_expr="icontains"
    )


class AirportFilter(FilterSet):
    name = filters.CharFilter(
        field_name="name", lookup_expr="icontains"
    )
    city_name = filters.CharFilter(
        field_name="city__name", lookup_expr="icontains"
    )
    country_name = filters.CharFilter(
        field_name="country__name", lookup_expr="icontains"
    )


class FlightFilter(FilterSet):
    country = filters.CharFilter(
        field_name="route__destination__country__name",
        lookup_expr="icontains"
    )
    city = filters.CharFilter(
        field_name="route__destination__city__name",
        lookup_expr="icontains"
    )
    departure_time = filters.DateFilter(
        field_name="departure_time", lookup_expr="date"
    )
    arrival_time = filters.DateFilter(
        field_name="arrival_time", lookup_expr="date"
    )


class TicketFilter(FilterSet):
    country = filters.CharFilter(
        field_name="flight__route__destination__country__name",
        lookup_expr="icontains"
    )
    city = filters.CharFilter(
        field_name="flight__route__destination__city__name",
        lookup_expr="icontains"
    )
    departure_time = filters.DateFilter(
        field_name="flight__departure_time", lookup_expr="date"
    )
    arrival_time = filters.DateFilter(
        field_name="flight__arrival_time", lookup_expr="date"
    )
    name = filters.CharFilter(
        field_name="flight__airplane__name", lookup_expr="icontains"
    )


class OrderFilter(FilterSet):
    country = filters.CharFilter(
        field_name="tickets__flight__route__destination__country__name",
        lookup_expr="icontains"
    )
    city = filters.CharFilter(
        field_name="tickets__flight__route__destination__city__name",
        lookup_expr="icontains"
    )
    departure_time = filters.DateFilter(
        field_name="tickets__flight__departure_time", lookup_expr="date"
    )
    arrival_time = filters.DateFilter(
        field_name="tickets__flight__arrival_time", lookup_expr="date"
    )
    name = filters.CharFilter(
        field_name="tickets__flight__airplane__name", lookup_expr="icontains"
    )


class RouteFilter(FilterSet):
    source_country = filters.CharFilter(
        field_name="source__country__name",
        lookup_expr="icontains"
    )
    source_city = filters.CharFilter(
        field_name="source__city__name",
        lookup_expr="icontains"
    )
    destination_country = filters.CharFilter(
        field_name="destination__country__name",
        lookup_expr="icontains"
    )
    destination_city = filters.CharFilter(
        field_name="destination__city__name",
        lookup_expr="icontains"
    )
