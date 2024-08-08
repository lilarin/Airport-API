from django.urls import path, include
from rest_framework import routers

from airport.views import (
    CityViewSet,
    CountryViewSet,
    AirportViewSet,
    RouteViewSet,
    AirplaneViewSet,
    AirplaneTypeViewSet,
    FlightViewSet,
    TicketViewSet,
    OrderViewSet
)

router = routers.DefaultRouter()
router.register("cities", CityViewSet)
router.register("countries", CountryViewSet)
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("flights", FlightViewSet)
router.register("tickets", TicketViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "airport"
