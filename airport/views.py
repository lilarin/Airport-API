from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser
)
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import (
    JWTAuthentication
)

from airport.filters import (
    NameFilter,
    AirportFilter,
    FlightFilter,
    RouteFilter,
    TicketFilter,
    OrderFilter, OrderAdminFilter
)
from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
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
    AirportSerializer,
    OrderSerializer,
    OrderAdminSerializer,
    FlightAdminSerializer,
    TicketAdminSerializer
)


class StandardPagePagination(PageNumberPagination):
    page_size = 5
    max_page_size = 100


class SmallPagePagination(PageNumberPagination):
    page_size = 2
    max_page_size = 100


class CityViewSet(viewsets.ModelViewSet):
    """Manage cities as admin user"""
    queryset = City.objects.all()
    serializer_class = CitySerializer
    pagination_class = StandardPagePagination
    filterset_class = NameFilter
    permission_classes = (IsAdminUser,)
    authentication_classes = (JWTAuthentication,)


class CountryViewSet(viewsets.ModelViewSet):
    """Manage countries as admin user"""
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = StandardPagePagination
    filterset_class = NameFilter
    permission_classes = (IsAdminUser,)
    authentication_classes = (JWTAuthentication,)


class AirportViewSet(viewsets.ModelViewSet):
    """Manage airports as admin user"""
    queryset = Airport.objects.select_related()
    serializer_class = AirportSerializer
    pagination_class = StandardPagePagination
    filterset_class = AirportFilter
    permission_classes = (IsAdminUser,)
    authentication_classes = (JWTAuthentication,)


class RouteViewSet(viewsets.ModelViewSet):
    """Manage flight routes as admin user"""
    queryset = Route.objects.select_related()
    serializer_class = RouteSerializer
    pagination_class = StandardPagePagination
    filterset_class = RouteFilter
    permission_classes = (IsAdminUser,)
    authentication_classes = (JWTAuthentication,)


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    """Manage airplane types as admin user"""
    queryset = AirplaneType.objects.select_related()
    serializer_class = AirplaneTypeSerializer
    pagination_class = StandardPagePagination
    filterset_class = NameFilter
    permission_classes = (IsAdminUser,)
    authentication_classes = (JWTAuthentication,)


class AirplaneViewSet(viewsets.ModelViewSet):
    """Manage airplanes as admin user"""
    queryset = Airplane.objects.select_related()
    serializer_class = AirplaneSerializer
    pagination_class = StandardPagePagination
    filterset_class = NameFilter
    permission_classes = (IsAdminUser,)
    authentication_classes = (JWTAuthentication,)


class FlightViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    """View flights for everyone"""
    queryset = Flight.objects.select_related()
    serializer_class = FlightSerializer
    pagination_class = SmallPagePagination
    filterset_class = FlightFilter


class FlightAdminViewSet(viewsets.ModelViewSet):
    """Manage flights as admin user"""
    queryset = Flight.objects.select_related(
        "route__destination__city",
        "route__source__city",
        "route__destination__country",
        "route__source__country",
        "airplane__airplane_type",
    ).prefetch_related("crew")
    serializer_class = FlightAdminSerializer
    pagination_class = SmallPagePagination
    filterset_class = FlightFilter
    permission_classes = (IsAdminUser,)
    authentication_classes = (JWTAuthentication,)


class TicketViewSet(viewsets.ModelViewSet):
    """Manage tickets as admin user"""
    queryset = Ticket.objects.select_related(
        "flight__route__destination__city",
        "flight__route__source__city",
        "flight__route__destination__country",
        "flight__route__source__country",
        "flight__airplane__airplane_type",
    ).prefetch_related("flight__crew")
    serializer_class = TicketAdminSerializer
    pagination_class = SmallPagePagination
    filterset_class = TicketFilter
    permission_classes = (IsAdminUser,)
    authentication_classes = (JWTAuthentication,)


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    """Get or create order for authenticated user"""
    queryset = Order.objects.select_related(
        "tickets__flight__route__destination__city",
        "tickets__flight__route__source__city",
        "tickets__flight__route__destination__country",
        "tickets__flight__route__source__country",
        "tickets__flight__airplane__airplane_type",
    )
    serializer_class = OrderSerializer
    pagination_class = SmallPagePagination
    filterset_class = OrderFilter
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderAdminViewSet(viewsets.ModelViewSet,):
    """Manage orders as admin user"""
    queryset = Order.objects.select_related(
        "tickets__flight__route__destination__city",
        "tickets__flight__route__source__city",
        "tickets__flight__route__destination__country",
        "tickets__flight__route__source__country",
        "tickets__flight__airplane__airplane_type",
    ).prefetch_related("tickets__flight__crew")
    serializer_class = OrderAdminSerializer
    pagination_class = SmallPagePagination
    filterset_class = OrderAdminFilter
    permission_classes = (IsAdminUser,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
