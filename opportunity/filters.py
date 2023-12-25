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
            'createdAt': ['exact'],
            'updatedAt': ['exact'],
            'payPerMonth': ['exact'],
            'isPaid': ['exact'],
            'type': ['exact'],
            'companyName': ['exact', 'icontains'],
            'workMode': ['exact'],
            'startDate': ['exact'],
            'endDate': ['exact'],
        }


class OpportunityApplicationFilter(CODEDateFilter):
    class Meta:
        model = OpportunityApplication
        fields = {
            'opportunity__name': ['exact'],
            'opportunity__companyName': ['exact', 'icontains'],
            'applicant__email': ['exact', 'icontains'],
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
