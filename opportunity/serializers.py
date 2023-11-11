from opportunity.models import (
    Opportunity,
    OpportunitySkill
)
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class OpportunitySerializer(ModelSerializer):
    alumniName = SerializerMethodField()
    profilePicture = SerializerMethodField()
    requiredSkills = SerializerMethodField()

    class Meta:
        model = Opportunity
        fields = ['id', 'name', 'description', 'alumni', 'type', 'companyName', 'startDate', 'endDate', 'location', 'locationType', 'requiredSkills', 'createdAt', 'updatedAt']
        list_fields = fields
        get_fields = fields

    def get_alumniName(self, instance):
        return (instance.alumni.user.firstName or '') + ' ' + (instance.alumni.user.lastName or '')

    def get_profilePicture(self, instance):
        return instance.alumni.user.profilePicture

    def get_requiredSkills(self, instance):
        return OpportunitySkillSerializer(instance.skills.all(), many=True).data


class OpportunitySkillSerializer(ModelSerializer):
    skillName = SerializerMethodField()
    opportunityName = SerializerMethodField()

    class Meta:
        model = OpportunitySkill
        fields = ['id', 'opportunity', 'skill', 'createdAt', 'updatedAt']
        list_fields = fields
        get_fields = fields

    def get_skillName(self, instance):
        return instance.skill.name

    def get_opportunityName(self, instance):
        return instance.opportunity.name