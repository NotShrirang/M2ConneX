from skill.models import Skill, UserSkill
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'createdAt', 'updatedAt']


class UserSkillSerializer(ModelSerializer):
    userName = SerializerMethodField()

    class Meta:
        model = UserSkill
        fields = ['id', 'user', 'skill', 'experience', 'createdAt', 'updatedAt']
        list_fields = fields
        get_fields = fields

    def get_userName(self, instance):
        return instance.user.name