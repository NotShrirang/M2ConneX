from opportunity.models import (
    Opportunity,
    OpportunitySkill,
    OpportunityApplication
)
from users.serializers import AlumniSerializer
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class OpportunitySerializer(ModelSerializer):
    alumniName = SerializerMethodField()
    profilePicture = SerializerMethodField()
    requiredSkills = SerializerMethodField()

    class Meta:
        model = Opportunity
        fields = [
            'id',
            'name', 
            'description',
            'payPerMonth',
            'isPaid',
            'alumni',
            'type',
            'companyName',
            'startDate',
            'endDate',
            'location',
            'workMode',
            'requiredSkills',
            'createdAt',
            'updatedAt',
            'alumniName',
            'profilePicture'
        ]
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
        fields = ['id', 'opportunity', 'skill', 'createdAt', 'updatedAt', 'skillName', 'opportunityName']
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
        fields = ['id', 'opportunity', 'applicant', 'about', 'status', 'createdAt', 'updatedAt', 'applicantDetails', 'opportunityDetails']
        list_fields = fields
        get_fields = fields

    def get_applicantDetails(self, instance):
        data = {
            'name': instance.applicant.user.firstName + " " + instance.applicant.user.lastName,
            'email': instance.applicant.user.email,
            'resume': instance.applicant.user.resume,
            'phone': instance.applicant.user.phoneNumber,
            'location': instance.applicant.user.city,
            'profilePicture': instance.applicant.user.profilePicture
        }
        return data

    def get_opportunityDetails(self, instance):
        data = {
            'name': instance.opportunity.name,
            'description': instance.opportunity.description,
            'type': instance.opportunity.type,
            'companyName': instance.opportunity.companyName,
            'location': instance.opportunity.location,
            'locationType': instance.opportunity.locationType
        }
        return data
