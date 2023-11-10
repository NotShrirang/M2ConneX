from connection.models import (
   Connection
)
from rest_framework.serializers import ModelSerializer

class ConnectionSerializer(ModelSerializer):
   class Meta:
       model = Connection
       fields = '__all__'   
