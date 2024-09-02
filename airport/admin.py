from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    Order,
    Ticket, City, Country,
)


@admin.register(User)
class UserAdmin(UserAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
    list_filter = [
        "name",
    ]
    search_fields = [
        "name",
    ]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
    list_filter = [
        "name",
    ]
    search_fields = [
        "name",
    ]


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "city",
        "country",
    ]
    list_filter = [
        "name",
        "city",
        "country",
    ]
    search_fields = [
        "name",
        "city",
        "country",
    ]


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = [
        "source",
        "destination",
        "distance"
    ]


@admin.register(AirplaneType)
class AirplaneTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = [
        "name",
    ]
    search_fields = [
        "name",
    ]


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "rows",
        "seats_in_row",
        "airplane_type"
    ]
    list_filter = [
        "name",
    ]
    search_fields = [
        "name",
    ]


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name"
    ]


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = [
        "route",
        "airplane",
        "display_crew"
    ]

    def display_crew(self, obj):
        return ", ".join([str(crew) for crew in obj.crew.all()])

    display_crew.short_description = "Crew"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "created_at",
        "user"
    ]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        "order",
        "row",
        "seat",
        "flight"
    ]
