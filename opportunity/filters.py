from .models import (
    Opportunity,
    OpportunityApplication,
    OpportunitySkill
)

from CODE.filters import CODEDateFilter


class OpportunityFilter(CODEDateFilter):
    class Meta:
        model = Opportunity
        fields = [
            'createdAt',
            'updatedAt',
            'payPerMonth',
            'isPaid',
            'type',
            'companyName',
            'workMode',
            'startDate',
            'endDate',
        ]


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
