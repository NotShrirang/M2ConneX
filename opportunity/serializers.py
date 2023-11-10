from opportunity.models import (
    Opportunity,
    OpportunitySkill
)
from rest_framework.serializers import ModelSerializer

class OpportunitySerializer(ModelSerializer):
    class Meta:
        model = Opportunity
        fields = '__all__'

class OpportunitySkillSerializer(ModelSerializer):
    class Meta:
        model = OpportunitySkill
        fields = '__all__'