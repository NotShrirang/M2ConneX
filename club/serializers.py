from rest_framework import serializers
from .models import Club, ClubMember


class ClubSerializer(serializers.ModelSerializer):
    facultyMentor = serializers.SerializerMethodField()
    facultyMentorName = serializers.SerializerMethodField()
    memberCount = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = ['id', 'name', 'description', 'logo', 'website',
                  'socialMedia1', 'socialMedia2', 'socialMedia3', 'email',
                  'phone', 'facultyMentor', 'memberCount']
        get_fields = fields
        list_fields = fields

    def get_facultyMentor(self, obj):
        facultyMentor = ClubMember.objects.filter(
            club=obj, position='faculty_mentor').first()
        if facultyMentor:
            return facultyMentor.user.id
        else:
            return None

    def get_facultyMentorName(self, obj):
        facultyMentor = ClubMember.objects.filter(
            club=obj, position='faculty_mentor').first()
        if facultyMentor:
            return facultyMentor.user.firstName + ' ' + facultyMentor.user.lastName
        else:
            return None

    def get_memberCount(self, obj):
        return ClubMember.objects.filter(club=obj).count()


class ClubMemberSerializer(serializers.ModelSerializer):
    clubName = serializers.SerializerMethodField()
    userName = serializers.SerializerMethodField()

    class Meta:
        model = ClubMember
        fields = ['id', 'user', 'club', 'position', 'positionInWords',
                  'isClubAdmin', 'clubName', 'userName']
        get_fields = fields
        list_fields = fields

    def get_clubName(self, obj):
        return obj.club.name

    def get_userName(self, obj):
        return obj.user.firstName + ' ' + obj.user.lastName
