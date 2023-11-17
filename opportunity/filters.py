from .models import (
    Opportunity,
    OpportunityApplication,
    OpportunitySkill
)

from CODE.filters import CODEDateFilter


class OpportunityFilter(CODEDateFilter):
    class Meta:
        model = Opportunity
        fields = {
            'name': ['exact', 'icontains'],
            'description': ['exact', 'icontains', 'contains'],
            'type': ['exact'],
            'companyName': ['exact', 'icontains'],
            'location': ['exact', 'icontains'],
            'locationType': ['exact'],
            'skills__skill__name': ['exact', 'icontains'],
        }


class OpportunityApplicationFilter(CODEDateFilter):
    class Meta:
        model = OpportunityApplication
        fields = {
            'opportunity__name': ['exact'],
            'opportunity__companyName': ['exact', 'icontains'],
            'applicant__user__email': ['exact', 'icontains'],
            'status': ['exact'],
            'about': ['exact', 'icontains'],
        }


class OpportunitySkillFilter(CODEDateFilter):
    class Meta:
        model = OpportunitySkill
        fields = {
            'opportunity__name': ['exact'],
            'opportunity__companyName': ['exact', 'icontains'],
            'skill__name': ['exact', 'icontains'],
        }
