from django.core.exceptions import ValidationError
from django.db import models
from smart_selects.db_fields import ChainedForeignKey

from airport_service import settings


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "countries"

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="city_country",
        blank=False,
        null=False
    )

    class Meta:
        unique_together = ("country", "name",)
        verbose_name_plural = "cities"

    def __str__(self):
        return self.name


class Airport(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="airport_country",
    )
    city = ChainedForeignKey(
        City,
        chained_field="country",
        chained_model_field="country",
        show_all=False,
        auto_choose=True,
        sort=True,
        related_name="city_airports"
    )

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Airport, on_delete=models.CASCADE,
        related_name="source_routes",
    )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE,
        related_name="destination_routes",
    )
    distance = models.IntegerField(null=True)

    def clean(self):
        if self.source == self.destination:
            raise ValidationError(
                "The source and destination airports must be different."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super(Route, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.source} -> {self.destination}"


# TODO - add image field to airplane
class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return (
            f"Airplane: {self.name} - "
            f"(rows: {self.rows}, seats_in_row: {self.seats_in_row})"
        )


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Flight(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="route_flights",
    )
    airplane = models.ForeignKey(
        Airplane,
        on_delete=models.CASCADE,
        related_name="airplane_flights",
    )
    crew = models.ManyToManyField(Crew, related_name="flights")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return (
            f"Flight from {self.route.source} to "
            f"{self.route.destination} - Aircraft: {self.airplane}"
        )


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return (
            f"Order #{self.pk} - User: {self.user.email}, "
            f"Created at: {self.created_at}"
        )


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="flight_tickets"
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_tickets"
    )

    def __str__(self):
        return (
            f"{str(self.flight)} - (row: {self.row}, seat: {self.seat})"
        )

    class Meta:
        unique_together = ("flight", "seat", "row")
        ordering = [
            "flight",
            "row",
            "seat",
        ]
