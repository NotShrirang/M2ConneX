from .models import (
    Skill,
    UserSkill
)

from CODE.filters import CODEDateFilter


class SkillFilter(CODEDateFilter):
    class Meta:
        model = Skill
        fields = {
            'name': ['exact', 'icontains'],
        }


class UserSkillFilter(CODEDateFilter):
    class Meta:
        model = UserSkill
        fields = {
            'user': ['exact'],
            'user__email': ['exact', 'icontains'],
            'skill': ['exact'],
            'skill__name': ['exact', 'icontains'],
        }
