from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from airport.filters import (
    NameFilter,
    AirportFilter
)

from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    Ticket,
    Order,
    City,
    Country,
)

from airport.serializers import (
    RouteSerializer,
    AirplaneSerializer,
    FlightSerializer,
    CitySerializer,
    CountrySerializer,
    AirplaneTypeSerializer,
    AirportSerializer, TicketSerializer, OrderSerializer
)


class StandardPagePagination(PageNumberPagination):
    page_size = 5
    max_page_size = 100


class SmallPagePagination(PageNumberPagination):
    page_size = 2
    max_page_size = 100


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    pagination_class = StandardPagePagination
    filterset_class = NameFilter


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = StandardPagePagination
    filterset_class = NameFilter


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.select_related()
    serializer_class = AirportSerializer
    pagination_class = StandardPagePagination
    filterset_class = AirportFilter


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related()
    serializer_class = RouteSerializer
    pagination_class = StandardPagePagination


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related()
    serializer_class = AirplaneSerializer
    pagination_class = StandardPagePagination


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.select_related()
    serializer_class = AirplaneTypeSerializer
    pagination_class = StandardPagePagination
    filterset_class = NameFilter


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related().prefetch_related("crew")
    serializer_class = FlightSerializer
    pagination_class = SmallPagePagination


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related(
        'flight__route__source',
        'flight__route__destination',
        'flight__airplane__airplane_type',
    )
    serializer_class = TicketSerializer
    pagination_class = SmallPagePagination


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related(
        "tickets__movie_session__movie", "tickets__movie_session__cinema_hall"
    )
    serializer_class = OrderSerializer
    pagination_class = SmallPagePagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
