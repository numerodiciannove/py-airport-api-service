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
    queryset = City.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CityListSerializer

        return CitySerializer
