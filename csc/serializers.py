from csc.models import (
    City, 
    State,
    Country,
)
from rest_framework.serializers import ModelSerializer

class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class StateSerializer(ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'