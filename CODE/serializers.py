from CODE.models import CODEBaseModel
from rest_framework.serializers import ModelSerializer


class CODEBaseModelSerializer(ModelSerializer):
    class Meta:
        model = CODEBaseModel
        fields = '__all__'
        db_table = 'CODEBaseModel'
        managed = True
        verbose_name = 'CODEBaseModel'
        verbose_name_plural = 'CODEBaseModels'
