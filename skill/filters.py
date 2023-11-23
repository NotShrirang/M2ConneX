from .models import(
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
        