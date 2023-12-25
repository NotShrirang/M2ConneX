from opportunity.models import (
    Opportunity,
    OpportunitySkill,
    OpportunityApplication
)
from users.serializers import AlumniSerializer
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class OpportunitySerializer(ModelSerializer):
    userName = SerializerMethodField()
    profilePicture = SerializerMethodField()
    requiredSkills = SerializerMethodField()
    hasApplied = SerializerMethodField()

    class Meta:
        model = Opportunity
        fields = [
            'id',
            'name',
            'description',
            'payPerMonth',
            'isPaid',
            'user',
            'type',
            'companyName',
            'startDate',
            'endDate',
            'location',
            'workMode',
            'requiredSkills',
            'userName',
            'profilePicture',
            'hasApplied',
            'createdAt',
            'updatedAt',
        ]
        list_fields = fields
        get_fields = fields

    def get_userName(self, instance):
        return (instance.user.firstName or '') + ' ' + (instance.user.lastName or '')

    def get_profilePicture(self, instance):
        return instance.user.profilePicture

    def get_requiredSkills(self, instance):
        return OpportunitySkillSerializer(instance.skills.all(), many=True).data

    def get_hasApplied(self, instance):
        return OpportunityApplication.objects.filter(opportunity=instance, applicant=self.context['request'].user).exists()


class OpportunitySkillSerializer(ModelSerializer):
    skillName = SerializerMethodField()
    opportunityName = SerializerMethodField()

    class Meta:
        model = OpportunitySkill
        fields = ['id', 'opportunity', 'skill', 'createdAt',
                  'updatedAt', 'skillName', 'opportunityName']
        list_fields = fields
        get_fields = fields

    def get_skillName(self, instance):
        return instance.skill.name

    def get_opportunityName(self, instance):
        return instance.opportunity.name


class OpportunityApplicationSerializer(ModelSerializer):
    applicantDetails = SerializerMethodField()
    opportunityDetails = SerializerMethodField()

    class Meta:
        model = OpportunityApplication
        fields = ['id', 'opportunity', 'applicant', 'about', 'status',
                  'createdAt', 'updatedAt', 'applicantDetails', 'opportunityDetails']
        list_fields = fields
        get_fields = fields

    def get_applicantDetails(self, instance):
        data = {
            'name': instance.applicant.firstName + " " + instance.applicant.lastName,
            'email': instance.applicant.email,
            'resume': instance.applicant.resume,
            'phone': str(instance.applicant.phoneNumber),
            'location': instance.applicant.city.name + ", " + instance.applicant.city.state.name + ", " + instance.applicant.city.state.country.name,
            'profilePicture': instance.applicant.profilePicture
        }
        return data

    def get_opportunityDetails(self, instance):
        data = {
            'name': instance.opportunity.name,
            'description': instance.opportunity.description,
            'type': instance.opportunity.type,
            'companyName': instance.opportunity.companyName,
            'location': instance.opportunity.location,
            'workMode': instance.opportunity.workMode
        }
        return data
