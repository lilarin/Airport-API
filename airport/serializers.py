from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    City,
    Country,
    Ticket,
    Order,
)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            "id",
            "name",
        )


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            "id",
            "name",
        )


class AirportSerializer(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(
        queryset=City.objects.all(),
        slug_field="name"
    )
    country = serializers.SlugRelatedField(
        queryset=Country.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = Airport
        fields = (
            "id",
            "name",
            "city",
            "country"
        )


class RouteSerializer(serializers.ModelSerializer):
    source = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all()
    )
    destination = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all()
    )

    class Meta:
        model = Route
        fields = (
            "id",
            "source",
            "destination",
            "distance"
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["source"] = AirportSerializer(
            instance.source
        ).data
        representation["destination"] = AirportSerializer(
            instance.destination
        ).data
        return representation

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        source_data = data.get("source")
        destination_data = data.get("destination")

        if isinstance(source_data, dict):
            internal_value["source"] = Airport.objects.get(
                id=source_data["id"]
            )
        elif isinstance(source_data, int):
            internal_value["source"] = Airport.objects.get(
                id=source_data
            )

        if isinstance(destination_data, dict):
            internal_value["destination"] = Airport.objects.get(
                id=destination_data["id"]
            )
        elif isinstance(destination_data, int):
            internal_value["destination"] = Airport.objects.get(
                id=destination_data
            )

        return internal_value


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = (
            "id",
            "name"
        )


class AirplaneSerializer(serializers.ModelSerializer):
    model = serializers.SlugRelatedField(
        read_only=True, slug_field="name", source="airplane_type"
    )
    available_seats = serializers.IntegerField(read_only=True)

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "model",
            "airplane_type",
            "available_seats"
        )
        extra_kwargs = {
            "airplane_type": {"write_only": True}
        }


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = (
            "id",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "first_name": {"read_only": True},
            "last_name": {"read_only": True},
        }


class FlightSerializer(serializers.ModelSerializer):
    departure_time = serializers.DateTimeField(
        format="%H:%M:%S %d.%m.%Y"
    )
    arrival_time = serializers.DateTimeField(
        format="%H:%M:%S %d.%m.%Y"
    )
    airplane = serializers.PrimaryKeyRelatedField(
        queryset=Airplane.objects.all()
    )
    route = serializers.PrimaryKeyRelatedField(
        queryset=Route.objects.all()
    )
    available_seats = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "available_seats",
            "departure_time",
            "arrival_time",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["airplane"] = AirplaneSerializer(
            instance.airplane
        ).data
        representation["route"] = RouteSerializer(
            instance.route
        ).data
        return representation


class FlightAdminSerializer(FlightSerializer):
    crew = serializers.PrimaryKeyRelatedField(
        queryset=Crew.objects.all(), many=True
    )

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "crew",
            "departure_time",
            "arrival_time",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["crew"] = CrewSerializer(
            instance.crew.all(), many=True
        ).data
        return representation

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        airplane_data = data.get("airplane")
        route_data = data.get("route")
        crew_data = data.get("crew")

        if isinstance(airplane_data, dict):
            internal_value["airplane"] = Airplane.objects.get(
                id=airplane_data["id"]
            )
        elif isinstance(airplane_data, int):
            internal_value["airplane"] = Airplane.objects.get(
                id=airplane_data
            )

        if isinstance(route_data, dict):
            internal_value["route"] = Route.objects.get(
                id=route_data["id"]
            )
        elif isinstance(route_data, int):
            internal_value["route"] = Route.objects.get(
                id=route_data
            )

        if isinstance(crew_data, list):
            internal_value["crew"] = Crew.objects.filter(
                id__in=[c["id"] for c in crew_data]
            )
        elif isinstance(crew_data, int):
            internal_value["crew"] = Crew.objects.get(
                id=crew_data
            )

        return internal_value


class TicketSerializer(serializers.ModelSerializer):
    flight = serializers.PrimaryKeyRelatedField(
        queryset=Flight.objects.all()
    )

    def validate(self, attrs):
        data = super().validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["flight"].airplane,
            ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "flight",
            "order"
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["flight"] = FlightSerializer(
            instance.flight
        ).data
        return representation

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        flight_data = data.get("flight")

        if isinstance(flight_data, dict):
            internal_value["flight"] = Flight.objects.get(
                id=flight_data["id"]
            )
        elif isinstance(flight_data, int):
            internal_value["flight"] = Flight.objects.get(
                id=flight_data
            )

        return internal_value


class TicketAdminSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "flight",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["flight"] = FlightAdminSerializer(
            instance.flight
        ).data
        return representation


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(
        many=True, read_only=False, allow_empty=False
    )
    created_at = serializers.DateTimeField(
        format="%H:%M:%S %d.%m.%Y", read_only=True
    )

    class Meta:
        model = Order
        fields = (
            "id",
            "tickets",
            "created_at"
        )

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(
                    order=order, **ticket_data
                )
            return order


class OrderAdminSerializer(OrderSerializer):
    tickets = TicketAdminSerializer(
        many=True, read_only=False, allow_empty=False
    )

    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "tickets",
            "created_at"
        )
