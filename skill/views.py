from skill.models import (
    Skill,
    UserSkill
)
from skill.serializers import (
    SkillSerializer,
    UserSkillSerializer
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from skill.serializers import UserSkillSerializer
from rest_framework.permissions import IsAuthenticated

class SkillView(ModelViewSet):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
    permission_classes = [IsAuthenticated,]
    
    def create(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.isActive:
            return super().create(request, *args, **kwargs)
        else:
            return Response({"error": "You are not authorized to create a skill"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def retrieve(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.isActive:
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response({"error": "You are not authorized to view a skill"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.isActive:
            if current_user.privilege == '1' or current_user.is_superuser:
                return super().update(request, *args, **kwargs)
            elif current_user.privilege in [2,3,4]:
                skill = Skill.objects.get(id=kwargs['pk'])
                if skill.createdByUser == current_user:
                    return super().update(request, *args, **kwargs)
                else:
                    return Response({"error": "You are not authorized to update the skills"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"error": "You are not authorized to update the skills"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error": "Your account is not active. Please contact admin"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def partial_update(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.isActive:
            if current_user.privilege == '1' or current_user.is_superuser:
                return super().update(request, *args, **kwargs)
            elif current_user.privilege in [2,3,4]:
                skill = Skill.objects.get(id=kwargs['pk'])
                if skill.createdByUser == current_user:
                    return super().update(request, *args, **kwargs)
                else:
                    return Response({"error": "You are not authorized to update the skills"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"error": "You are not authorized to update the skills"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error": "Your account is not active. Please contact admin"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            if user.privilege in ['1','2','3','4'] or user.is_superuser:
                skill = Skill.objects.get(id=kwargs['id'])
                if skill.createdByUser == user or user.privilege == '1':
                    return Response({'message': 'Opportunity deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({'error': 'You are not authorized to delete opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'You are not authorized to delete opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to delete opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def list(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.isActive:
            return super().list(request, *args, **kwargs)
        else:
            return Response({"error": "You are not authorized to view skills"}, status=status.HTTP_401_UNAUTHORIZED)
    
class UserSkillView(ModelViewSet):
    serializer_class = UserSkillSerializer
    queryset = UserSkill.objects.all()
    
    def create(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.isActive:
            return super().create(request, *args, **kwargs)
        else:
            return Response({"error": "You are not authorized to create a skill"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def retrieve(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.isActive:
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response({"error": "You are not authorized to view a skill"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.isActive:
            if current_user.privilege == '1' or current_user.is_superuser:
                return super().update(request, *args, **kwargs)
            elif current_user.privilege in [2,3,4]:
                skill = Skill.objects.get(id=kwargs['pk'])
                if skill.createdByUser == current_user:
                    return super().update(request, *args, **kwargs)
                else:
                    return Response({"error": "You are not authorized to update the skills"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"error": "You are not authorized to update the skills"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error": "Your account is not active. Please contact admin"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def partial_update(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.isActive:
            if current_user.privilege == '1' or current_user.is_superuser:
                return super().update(request, *args, **kwargs)
            elif current_user.privilege in [2,3,4]:
                skill = Skill.objects.get(id=kwargs['pk'])
                if skill.createdByUser == current_user:
                    return super().update(request, *args, **kwargs)
                else:
                    return Response({"error": "You are not authorized to update the skills"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"error": "You are not authorized to update the skills"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error": "Your account is not active. Please contact admin"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            if user.privilege in ['1','2','3','4'] or user.is_superuser:
                skill = Skill.objects.get(id=kwargs['id'])
                if skill.createdByUser == user or user.privilege == '1':
                    return Response({'message': 'Opportunity deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({'error': 'You are not authorized to delete opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'You are not authorized to delete opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to delete opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def list(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.isActive:
            return super().list(request, *args, **kwargs)
        else:
            return Response({"error": "You are not authorized to view skills"}, status=status.HTTP_401_UNAUTHORIZED)