from rest_framework import serializers

from airport_app.models import (
    Country,
    City,
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name",)


class CountryRetrieveSerializer(CountrySerializer):
    cities = CountrySerializer(
        many=True, read_only=True,
        source="city_country"
    )

    class Meta:
        model = Country
        fields = ("id", "name", "cities")


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name",)


class CityListSerializer(CitySerializer):
    class Meta:
        model = City
        fields = ("id", "name",)


class CityRetrieveSerializer(CitySerializer):
    country = CountrySerializer()

    class Meta:
        model = City
        fields = ("id", "name", "country")


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "country", "city",)

    def validate(self, data):
        country = data.get('country')
        city = data.get('city')
        if city.country != country:
            raise serializers.ValidationError(
                "The selected city does not belong to the selected country."
            )
        return data


class AirportListSerializer(AirportSerializer):
    country = serializers.CharField(source="country.name")
    city = serializers.CharField(source="city.name")


class AirportRetrieveSerializer(AirportSerializer):
    city = CityRetrieveSerializer()

    class Meta:
        model = Airport
        fields = ("id", "name", "city",)


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteListSerializer(RouteSerializer):
    source = serializers.SerializerMethodField()
    destination = serializers.SerializerMethodField()

    @staticmethod
    def get_source(obj):
        return f"{obj.source.city}, {obj.source.country} - '{obj.source.name}'"

    @staticmethod
    def get_destination(obj):
        return (
            f"{obj.destination.city}, {obj.destination.country} - "
            f"'{obj.destination.name}'"
        )


class RouteRetrieveSerializer(RouteSerializer):
    source = AirportRetrieveSerializer()
    destination = AirportRetrieveSerializer()


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = "__all__"


class AirplaneSerializer(serializers.ModelSerializer):
    airplane_image = serializers.ImageField(read_only=True)

    class Meta:
        model = Airplane
        fields = (
            "id",
            "airplane_type",
            "name",
            "rows",
            "seats_in_row",
            "airplane_image",
        )


class AirplaneListSerializer(AirplaneSerializer):
    airplane_type = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "airplane_type",
            "capacity",
            "airplane_image",
        )


class AirplaneRetrieveSerializer(AirplaneSerializer):
    airplane_type = AirplaneTypeSerializer()

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "airplane_type",
            "rows",
            "seats_in_row",
            "capacity",
            "airplane_image",
        )


class AirplaneImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "airplane_image")


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"
