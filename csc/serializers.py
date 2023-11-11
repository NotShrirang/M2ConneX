from rest_framework import serializers
from .models import Country, State, City


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            "id",
            "createdAt",
            "updatedAt",
            "name",
        )
        get_fields = (
            "id",
            "createdAt",
            "updatedAt",
            "name",
        )
        list_fields = (
            "id",
            "createdAt",
            "updatedAt",
            "name",
        )


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = (
            "id",
            "createdAt",
            "updatedAt",
            "name",
            "country",
        )
        list_fields = fields
        get_fields = fields


class CitySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = (
            "id",
            "createdAt",
            "updatedAt",
            "name",
            "state",
            "latitude",
            "longitude",
        )
        list_fields = fields
        get_fields = fields

    def get_name(self, instance):
        return instance.name + " | " + instance.state.name + " | " + instance.state.country.name
