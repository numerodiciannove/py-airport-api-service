from django.db.models import F, ExpressionWrapper, IntegerField, Count
from airport_app.permissions import IsAdminOrIfAuthenticatedReadOnly
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from airport_app.models import (
    Country,
    City,
    Airport,
    Route,
    Airplane,
    AirplaneType,
    Crew,
    Flight,
)

from airport_app.serializers import (
    CountrySerializer,
    CitySerializer,
    CityListSerializer,
    AirportSerializer,
    AirportListSerializer,
    AirportRetrieveSerializer,
    CityRetrieveSerializer,
    RouteSerializer,
    RouteListSerializer,
    RouteRetrieveSerializer,
    AirplaneSerializer,
    AirplaneListSerializer,
    AirplaneImageSerializer,
    AirplaneTypeSerializer,
    AirplaneRetrieveSerializer,
    CountryRetrieveSerializer,
    CrewSerializer,
    FlightListSerializer,
    FlightRetrieveSerializer,
    FlightSerializer,
)


class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CountryRetrieveSerializer

        return CountrySerializer


class CityViewSet(ModelViewSet):
    queryset = City.objects.all().select_related()

    def get_serializer_class(self):
        if self.action == "list":
            return CityListSerializer
        elif self.action == "retrieve":
            return CityRetrieveSerializer

        return CitySerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            return queryset.select_related()
        return queryset


class AirportViewSet(ModelViewSet):
    queryset = Airport.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return AirportListSerializer
        elif self.action == "retrieve":
            return AirportRetrieveSerializer

        return AirportSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            return queryset.select_related()

        return queryset


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        elif self.action == "retrieve":
            return RouteRetrieveSerializer

        return RouteSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            return queryset.select_related("source", "destination")

        return queryset


class AirplaneTypeViewSet(ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(ModelViewSet):
    queryset = Airplane.objects.all()
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        elif self.action == "retrieve":
            return AirplaneRetrieveSerializer
        elif self.action == "upload_image":
            return AirplaneImageSerializer

        return AirplaneSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser, ],
    )
    def upload_image(self, request, pk=None):
        airplane = self.get_object()
        serializer = self.get_serializer(airplane, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """Detail view for the airplanes with filters"""
        queryset = self.queryset
        airplane_type = self.request.query_params.get("airplane_types")
        capacity_gte = self.request.query_params.get("capacity_gte")
        capacity_lte = self.request.query_params.get("capacity_lte")

        if airplane_type:
            airplane_types_ids = [
                int(str_id) for str_id in airplane_type.split(",")
            ]
            queryset = Airplane.objects.filter(
                airplane_type__id__in=airplane_types_ids
            )

        if capacity_gte:
            queryset = queryset.annotate(
                computed_capacity=ExpressionWrapper(
                    F('rows') * F('seats_in_row'),
                    output_field=IntegerField(),
                )
            ).filter(
                computed_capacity__gte=int(capacity_gte)
            )

        if capacity_lte:
            queryset = queryset.annotate(
                computed_capacity=ExpressionWrapper(
                    F('rows') * F('seats_in_row'),
                    output_field=IntegerField(),
                )
            ).filter(
                computed_capacity__lte=int(capacity_lte)
            )

        if self.action in ["list", "retrieve"]:
            queryset = queryset.prefetch_related("airplane_type")

        return queryset


class CrewViewSet(ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class FlightViewSet(ModelViewSet):
    queryset = (
        Flight.objects.all()
        .select_related("route__source",
                        "route__destination",
                        "airplane__airplane_type")
        .annotate(
            tickets_available=(
                    F("airplane__rows") * F("airplane__seats_in_row")
                    - Count("flight_tickets")
            )
        )
    )
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        airplanes = self.request.query_params.get("airplanes")
        routes = self.request.query_params.get("routes")
        date = self.request.query_params.get("date")

        queryset = self.queryset

        if airplanes:
            airplanes_ids = self._params_to_ints(airplanes)
            queryset = queryset.filter(airplane__id__in=airplanes_ids)

        if routes:
            routes_ids = self._params_to_ints(routes)
            queryset = queryset.filter(route__id__in=routes_ids)

        if date:
            queryset = queryset.filter(departure_time__date=date)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer

        if self.action == "retrieve":
            return FlightRetrieveSerializer

        return FlightSerializer
