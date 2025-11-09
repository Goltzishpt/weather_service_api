from rest_framework import serializers

from cities.models import City, CityTemperature


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name", "description"]


class CityTemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityTemperature
        fields = ["id", "city", "value", "created_at"]
        read_only_fields = ["id", "city", "created_at"]