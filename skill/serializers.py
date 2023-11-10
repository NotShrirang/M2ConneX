from skill.models import Skill, UserSkill
from rest_framework.serializers import ModelSerializer

class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class UserSkillSerializer(ModelSerializer):
    class Meta:
        model = UserSkill
        fields = '__all__'