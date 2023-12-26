from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, pagination

from experience.models import Experience
from experience.serializers import ExperienceSerializer
from users.models import AlumniPortalUser


class ExperienceView(ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated,]
    pagination_class = pagination.PageNumberPagination
    ordering = ['-endDate']

    def list(self, request, *args, **kwargs):
        current_user: AlumniPortalUser = request.user
        if current_user.is_active is False:
            return Response({"detail": "User is not active"}, status=400)
        elif current_user.isVerified is False:
            return Response({"detail": "User is not verified"}, status=400)
        else:
            queryset = Experience.objects.filter(
                user=current_user, isActive=True)
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
        if current_user.isVerified is False:
            return Response({"detail": "User is not verified"}, status=400)
        data = request.data
        if 'endDate' not in request.data:
            if 'isCurrent' not in request.data:
                return Response({"detail": "Experience must be current or have an end date"}, status=400)
            else:
                if request.data.get('isCurrent') is False:
                    return Response({"detail": "Experience must be current or have an end date"}, status=400)
            data['endDate'] = None
        if data.get('endDate') and data.get('startDate') > data.get('endDate'):
            return Response({"detail": "Start date cannot be after end date"}, status=400)
        data['user'] = current_user.id
        print("EXPERIENCE DATA", data, flush=True)
        serializer = ExperienceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
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


class UserExperienceView(generics.ListAPIView):
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated,]
    pagination_class = pagination.PageNumberPagination

    def list(self, request, *args, **kwargs):
        userId = kwargs.get('userId')
        user = AlumniPortalUser.objects.filter(id=userId)
        if not user.exists():
            return Response({"detail": "User does not exist"}, status=400)
        user = user.first()
        if not user.is_active:
            return Response({"detail": "User is not active"}, status=400)
        if not user.isVerified:
            return Response({"detail": "User is not verified"}, status=400)
        queryset = Experience.objects.filter(user=user, isActive=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ExperienceSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ExperienceSerializer(queryset, many=True)
        return Response(serializer.data)
