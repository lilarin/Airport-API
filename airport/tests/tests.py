from django.contrib.auth import get_user_model
from django.test import TestCase

from airport.models import (
    City,
    Country,
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    Order,
    Ticket,
)

from airport.serializers import (
    CitySerializer,
    CountrySerializer,
    AirportSerializer,
    RouteSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    CrewSerializer,
    FlightSerializer,
    TicketSerializer,
)


class SerializerTests(TestCase):
    def setUp(self):
        self.city = City.objects.create(name="Test City")
        self.country = Country.objects.create(name="Test Country")
        self.airport1 = Airport.objects.create(
            name="Airport 1", city=self.city, country=self.country
        )
        self.airport2 = Airport.objects.create(
            name="Airport 2", city=self.city, country=self.country
        )
        self.route = Route.objects.create(
            source=self.airport1, destination=self.airport2, distance=1000
        )
        self.airplane_type = AirplaneType.objects.create(name="Boeing 747")
        self.airplane = Airplane.objects.create(
            name="Airplane 1", airplane_type=self.airplane_type, rows=30, seats_in_row=6
        )
        self.crew = Crew.objects.create(first_name="John", last_name="Doe")
        self.flight = Flight.objects.create(
            route=self.route, airplane=self.airplane, departure_time="2024-08-07 14:51:07.000",
            arrival_time="2024-08-07 14:51:07.000"
        )
        User = get_user_model()
        self.user = User.objects.create_user(email='testuser@mail.com', password='testpassword')
        self.order = Order.objects.create(user=self.user)
        self.ticket = Ticket.objects.create(
            row=10, seat=4, flight=self.flight, order=self.order
        )

    def test_city_serializer(self):
        serializer = CitySerializer(self.city)
        self.assertEqual(serializer.data, {"id": self.city.id, "name": self.city.name})

    def test_country_serializer(self):
        serializer = CountrySerializer(self.country)
        self.assertEqual(serializer.data, {"id": self.country.id, "name": self.country.name})

    def test_airport_serializer(self):
        serializer = AirportSerializer(self.airport1)
        self.assertEqual(
            serializer.data,
            {
                "id": self.airport1.id,
                "name": self.airport1.name,
                "city": self.city.name,
                "country": self.country.name,
            },
        )

    def test_route_serializer(self):
        serializer = RouteSerializer(self.route)
        self.assertEqual(
            serializer.data,
            {
                "id": self.route.id,
                "source": AirportSerializer(self.airport1).data,
                "destination": AirportSerializer(self.airport2).data,
                "distance": self.route.distance,
            },
        )

    def test_airplane_type_serializer(self):
        serializer = AirplaneTypeSerializer(self.airplane_type)
        self.assertEqual(serializer.data, {"id": self.airplane_type.id, "name": self.airplane_type.name})

    def test_airplane_serializer(self):
        serializer = AirplaneSerializer(self.airplane)
        self.assertEqual(
            serializer.data,
            {
                'id': self.airplane.id,
                'name': self.airplane.name,
                'model': self.airplane_type.name,
            }
        )

    def test_crew_serializer(self):
        serializer = CrewSerializer(self.crew)
        self.assertEqual(
            serializer.data,
            {"id": self.crew.id, "first_name": self.crew.first_name, "last_name": self.crew.last_name},
        )

    def test_ticket_serializer(self):
        serializer = TicketSerializer(self.ticket)
        self.assertEqual(
            serializer.data,
            {
                "id": self.ticket.id,
                "row": self.ticket.row,
                "seat": self.ticket.seat,
                "flight": FlightSerializer(self.flight).data,
                "order": self.ticket.order.id,
            },
        )
