from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from experience.models import Experience
from experience.serializers import ExperienceSerializer
from users.models import AlumniPortalUser


class ExperienceView(ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated,]

    def list(self, request, *args, **kwargs):
        current_user: AlumniPortalUser = request.user
        if current_user.is_active is False:
            return Response({"detail": "User is not active"}, status=400)
        elif current_user.isVerified is False:
            return Response({"detail": "User is not verified"}, status=400)
        else:
            queryset = Experience.objects.filter(user=current_user, isActive=True)
            serializer = ExperienceSerializer(queryset, many=True)
            return Response(serializer.data)
        
    def retrieve(self, request, *args, **kwargs):
        experienceId = kwargs.get('pk')
        experience = Experience.objects.filter(id=experienceId, isActive=True)
        if not experience.exists():
            return Response({"detail": "Experience does not exist"}, status=400)
        experience = experience.first()
        current_user: AlumniPortalUser = request.user
        if current_user.is_active is False:
            return Response({"detail": "User is not active"}, status=400)
        elif current_user.isVerified is False:
            return Response({"detail": "User is not verified"}, status=400)
        else:
            serializer = ExperienceSerializer(experience)
            return Response(serializer.data)
        
    def create(self, request, *args, **kwargs):
        current_user: AlumniPortalUser = request.user
        if current_user.is_active is False:
            return Response({"detail": "User is not active"}, status=400)
        elif current_user.isVerified is False:
            return Response({"detail": "User is not verified"}, status=400)
        else:
            data = request.data
            data['user'] = current_user.id
            serializer = ExperienceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        
    def update(self, request, *args, **kwargs):
        experienceId = kwargs.get('pk')
        experience = Experience.objects.filter(id=experienceId, isActive=True)
        if not experience.exists():
            return Response({"detail": "Experience does not exist"}, status=400)
        experience = experience.first()
        current_user: AlumniPortalUser = request.user
        if experience.user != current_user:
            return Response({"detail": "User is not authorized to update this experience"}, status=400)
        if not current_user.is_active:
            return Response({"detail": "User is not active"}, status=400)
        if not current_user.isVerified:
            return Response({"detail": "User is not verified"}, status=400)
        data = request.data
        serializer = ExperienceSerializer(experience, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        
    def partial_update(self, request, *args, **kwargs):
        experienceId = kwargs.get('pk')
        experience = Experience.objects.filter(id=experienceId, isActive=True)
        if not experience.exists():
            return Response({"detail": "Experience does not exist"}, status=400)
        experience = experience.first()
        current_user: AlumniPortalUser = request.user
        if experience.user != current_user:
            return Response({"detail": "User is not authorized to update this experience"}, status=400)
        if not current_user.is_active:
            return Response({"detail": "User is not active"}, status=400)
        if not current_user.isVerified:
            return Response({"detail": "User is not verified"}, status=400)
        data = request.data
        serializer = ExperienceSerializer(experience, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        
    def destroy(self, request, *args, **kwargs):
        experienceId = kwargs.get('pk')
        experience = Experience.objects.filter(id=experienceId, isActive=True)
        if not experience.exists():
            return Response({"detail": "Experience does not exist"}, status=400)
        experience = experience.first()
        current_user: AlumniPortalUser = request.user
        if experience.user != current_user:
            return Response({"detail": "User is not authorized to delete this experience"}, status=400)
        if not current_user.is_active:
            return Response({"detail": "User is not active"}, status=400)
        if not current_user.isVerified:
            return Response({"detail": "User is not verified"}, status=400)
        experience.isActive = False
        experience.save()
        return Response({"detail": "Experience deleted successfully"}, status=200)
