from __future__ import annotations

import os
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
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
        null=False,
    )

    class Meta:
        unique_together = (
            "country",
            "name",
        )
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
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="airport_city",
    )

    def __str__(self):
        return f"{self.city} - {self.country} 🟢 '{self.name}'"


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="source_routes",
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
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


def airplane_image_file_path(instance, filename) -> str:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/airplanes/", filename)


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    airplane_type = models.ForeignKey(
        AirplaneType,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_image = models.ImageField(
        null=True,
        upload_to=airplane_image_file_path,
    )

    @property
    def capacity(self) -> int | str:
        capacity = self.rows * self.seats_in_row

        if capacity > 0:
            return capacity
        return "cargo_airplane"

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
        related_name="flight_tickets",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_tickets",
    )

    @staticmethod
    def validate_ticket(row, seat, airplane, error_to_raise):
        for ticket_attr_value, ticket_attr_name, airplane_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(airplane, airplane_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                        f"number must be in available range: "
                        f"(1, {airplane_attr_name}): "
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

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return f"{str(self.flight)} (row: {self.row}, seat: {self.seat})"

    class Meta:
        unique_together = ("flight", "row", "seat")
        ordering = ["flight", "row", "seat"]
