from django.db.models import F, ExpressionWrapper, IntegerField
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from airport_app.models import (
    Country,
    City,
    Airport,
    Route,
    Airplane,
    AirplaneType,
)
from airport_app.permissions import IsAdminOrIfAuthenticatedReadOnly
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
