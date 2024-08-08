from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"


class Airport(models.Model):
    name = models.CharField(max_length=255, unique=True)
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="airports"
    )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="airports"
    )

    def __str__(self):
        return f"{self.name} ({self.city}, {self.country})"


class Route(models.Model):
    source = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="routes_from"
    )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="routes_to"
    )
    distance = models.IntegerField()

    class Meta:
        unique_together = (
            "source", "destination"
        )

    def __str__(self):
        return f"{self.source} - {self.destination}"


class AirplaneType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"


class Airplane(models.Model):
    name = models.CharField(max_length=255, unique=True)
    airplane_type = models.ForeignKey(
        AirplaneType, on_delete=models.CASCADE, related_name="airplanes"
    )
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return f"{self.name} ({self.airplane_type})"


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Flight(models.Model):
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name="flights"
    )
    airplane = models.ForeignKey(
        Airplane, on_delete=models.CASCADE, related_name="flights"
    )
    crew = models.ManyToManyField(Crew, blank=True)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"{self.route} - {self.airplane}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )

    def __str__(self):
        return f"{self.user} ({self.created_at})"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="tickets"
    )

    class Meta:
        unique_together = (
            "row", "seat", "flight"
        )

    @staticmethod
    def validate_ticket(row, seat, cinema_hall, error_to_raise):
        for ticket_attr_value, ticket_attr_name, flight_airplane_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(cinema_hall, flight_airplane_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                        f"number must be in available range: "
                        f"(1, {flight_airplane_attr_name}): "
                        f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.flight.airplane,
            ValidationError,
        )

    def __str__(self):
        return f"{self.order} (flight: {self.flight})"
