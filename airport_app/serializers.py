from rest_framework import serializers

from airport_app.models import (
    Country,
    City,
    Airport,
)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "name")


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name", "country")


class CityListSerializer(CitySerializer):
    country = CountrySerializer()


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "country", "city",)

    def validate(self, data):
        country = data.get('country')
        city = data.get('city')
        if city.country != country:
            raise serializers.ValidationError(
                "The selected city does not belong to the selected country.")
        return data


class AirportListSerializer(AirportSerializer):
    country = CountrySerializer()
    city = CitySerializer()
