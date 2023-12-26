from skill.models import (
    Skill,
    UserSkill
)
from skill.serializers import (
    SkillSerializer,
    UserSkillSerializer
)
from skill.filters import SkillFilter, UserSkillFilter

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, generics, pagination, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


class SkillView(ModelViewSet):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
    permission_classes = [IsAuthenticated,]
    pagination_class = pagination.PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']
    filterset_fields = ['name', 'isActive']
    ordering_fields = ('name',)
    ordering = ('name',)

    def list(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.isVerified:
            return Response({"detail": "User is not verified"}, status=400)
        if not current_user.is_active:
            return Response({"detail": "User is not active"}, status=400)

        qs = self.filter_queryset(
            self.queryset.filter(isActive=True).order_by('name'))
        serializer = SkillSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.isVerified:
            return Response({"detail": "User is not verified"}, status=400)
        if not current_user.is_active:
            return Response({"detail": "User is not active"}, status=400)
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.isVerified:
            return Response({"detail": "User is not verified"}, status=400)
        if not current_user.is_active:
            return Response({"detail": "User is not active"}, status=400)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.isVerified:
            return Response({"detail": "User is not verified"}, status=400)
        if current_user.is_active:
            if current_user.privilege == 'Super Admin' or current_user.is_superuser:
                return super().update(request, *args, **kwargs)
            else:
                return Response({"error": "You are not authorized to update the skills"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error": "Your account is not active. Please contact admin."}, status=status.HTTP_401_UNAUTHORIZED)

    def partial_update(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.isVerified:
            return Response({"detail": "User is not verified"}, status=status.HTTP_400_BAD_REQUEST)
        if current_user.is_active:
            if current_user.privilege == 'Super Admin' or current_user.is_superuser:
                return super().update(request, *args, **kwargs)
            else:
                return Response({"error": "You are not authorized to update the skills"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error": "Your account is not active. Please contact admin."}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if not user.isVerified:
            return Response({"detail": "User is not verified"}, status=status.HTTP_400_BAD_REQUEST)
        if user.is_active:
            if user.privilege == 'Super Admin' or user.is_superuser:
                skill = Skill.objects.get(id=kwargs['id'])
                skill.isActive = False
                skill.save()
                return Response({'message': 'Skill deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'You are not authorized to delete skills'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to delete skills'}, status=status.HTTP_401_UNAUTHORIZED)


class UserSkillView(ModelViewSet):
    serializer_class = UserSkillSerializer
    queryset = UserSkill.objects.all()

    def create(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({"detail": "User is not active"}, status=status.HTTP_400_BAD_REQUEST)
        if not current_user.isVerified:
            return Response({"detail": "User is not verified"}, status=status.HTTP_400_BAD_REQUEST)
        if 'skill' not in request.data:
            return Response({"detail": "Skill is required"}, status=status.HTTP_400_BAD_REQUEST)
        if 'experience' not in request.data:
            return Response({"detail": "Experience is required"}, status=status.HTTP_400_BAD_REQUEST)
        skillName = request.data['skill']
        userSkill = UserSkill.objects.filter(
            user=current_user, skill=skillName)
        if userSkill.exists():
            return Response({"detail": "Skill already exists"}, status=status.HTTP_400_BAD_REQUEST)
        skill = Skill.objects.get(id=skillName)
        if skill is None:
            skill = Skill.objects.create(name=skillName)
        data = {
            'user': current_user.id,
            'skill': skill.id,
            'experience': request.data['experience']
        }
        serializer = UserSkillSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Skill added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_active:
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response({"error": "You are not authorized to view a skill"}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({"detail": "User is not active"}, status=status.HTTP_400_BAD_REQUEST)
        if not current_user.isVerified:
            return Response({"detail": "User is not verified"}, status=status.HTTP_400_BAD_REQUEST)
        if 'skill' not in request.data:
            return Response({"detail": "Skill is required"}, status=status.HTTP_400_BAD_REQUEST)
        if 'experience' not in request.data:
            return Response({"detail": "Experience is required"}, status=status.HTTP_400_BAD_REQUEST)
        skill = request.data['skill']
        skill = Skill.objects.get(id=skill)
        userSkill = UserSkill.objects.filter(id=kwargs['pk'])
        if userSkill.exists():
            userSkill = userSkill.first()
            if userSkill.user != current_user:
                return Response({"detail": "You are not authorized to update this skill"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"detail": "Skill does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if userSkill.skill.id != skill.id:
            userSkill.skill = skill
            userSkill.save()
        if userSkill.experience != request.data['experience']:
            userSkill.experience = request.data['experience']
            userSkill.save()
        return Response({"detail": "Skill updated successfully"}, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({"detail": "User is not active"}, status=status.HTTP_400_BAD_REQUEST)
        if not current_user.isVerified:
            return Response({"detail": "User is not verified"}, status=status.HTTP_400_BAD_REQUEST)
        if 'skill' not in request.data:
            return Response({"detail": "Skill is required"}, status=status.HTTP_400_BAD_REQUEST)
        if 'experience' not in request.data:
            return Response({"detail": "Experience is required"}, status=status.HTTP_400_BAD_REQUEST)
        skill = request.data['skill']
        skill = Skill.objects.get(id=skill)
        userSkill = UserSkill.objects.filter(id=kwargs['pk'])
        if userSkill.exists():
            userSkill = userSkill.first()
            if userSkill.user != current_user:
                return Response({"detail": "You are not authorized to update this skill"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"detail": "Skill does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if userSkill.skill.id != skill.id:
            userSkill.skill = skill
            userSkill.save()
        if userSkill.experience != request.data['experience']:
            userSkill.experience = request.data['experience']
            userSkill.save()
        return Response({"detail": "Skill updated successfully"}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            if user.privilege in ['Student', 'Staff', 'Alumni', 'Super Admin'] or user.is_superuser:
                skill = Skill.objects.get(id=kwargs['id'])
                if skill.createdByUser == user or user.privilege == 'Super Admin':
                    return Response({'message': 'Opportunity deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({'error': 'You are not authorized to delete opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'You are not authorized to delete opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to delete opportunities'}, status=status.HTTP_401_UNAUTHORIZED)

    def list(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_active:
            return super().list(request, *args, **kwargs)
        else:
            return Response({"error": "You are not authorized to view skills"}, status=status.HTTP_401_UNAUTHORIZED)


class UserSkillByUserView(generics.ListAPIView):
    serializer_class = UserSkillSerializer
    queryset = UserSkill.objects.all()
    permission_classes = [IsAuthenticated,]
    pagination_class = pagination.PageNumberPagination

    def list(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({"detail": "User is not active"}, status=400)
        if not current_user.isVerified:
            return Response({"detail": "User is not verified"}, status=400)
        userId = kwargs.get('userId')
        queryset = UserSkill.objects.filter(
            user=userId).order_by("-experience", "-createdAt")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSkillSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserSkillSerializer(queryset, many=True)
        return Response(serializer.data)
