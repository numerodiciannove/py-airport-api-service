from rest_framework.viewsets import ModelViewSet

from airport_app.models import (
    Country,
    City,
)
from airport_app.serializers import (
    CountrySerializer,
    CitySerializer,
    CityListSerializer
)


class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityViewSet(ModelViewSet):
    queryset = City.objects.all().select_related()

    def get_serializer_class(self):
        if self.action == "list":
            return CityListSerializer

        return CitySerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            return queryset.select_related()
        return queryset
