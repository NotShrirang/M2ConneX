from opportunity.models import (
    Opportunity,
    OpportunitySkill
)
from opportunity.serializers import (
    OpportunitySerializer,
    OpportunitySkillSerializer
)
from rest_framework.viewsets import ModelViewSet


class OpportunityViewSet(ModelViewSet):
    serializer_class = OpportunitySerializer
    queryset = Opportunity.objects.all()


class OpportunitySkillViewSet(ModelViewSet):
    serializer_class = OpportunitySkillSerializer
    queryset = OpportunitySkill.objects.all()
