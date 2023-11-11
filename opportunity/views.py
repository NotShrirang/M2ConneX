from opportunity.models import (
    Opportunity,
    OpportunitySkill
)
from opportunity.serializers import (
    OpportunitySerializer,
    OpportunitySkillSerializer
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class OpportunityViewSet(ModelViewSet):
    serializer_class = OpportunitySerializer
    queryset = Opportunity.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            super().list(request, *args, **kwargs)
        else:
            return Response({'error': 'You are not authorized to view opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            super().retrieve(request, *args, **kwargs)
        else:
            return Response({'error': 'You are not authorized to view opportunities'}, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            if user.privilege == '3':
                super().create(request, *args, **kwargs)
            else:
                return Response({'error': 'You are not authorized to create opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to create opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
        
    def update(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            if user.privilege == '3':
                opportunity = Opportunity.objects.get(id=kwargs['id'])
                if opportunity.alumni == user:
                    super().update(request, *args, **kwargs)
                else:
                    return Response({'error': 'You are not authorized to update opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'You are not authorized to update opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to update opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
        
    def partial_update(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            if user.privilege == '3':
                opportunity = Opportunity.objects.get(id=kwargs['id'])
                if opportunity.alumni == user:
                    super().update(request, *args, **kwargs)
                else:
                    return Response({'error': 'You are not authorized to update opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'You are not authorized to update opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to update opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            if user.privilege == '3' or user.is_superuser or user.privilege == '1':
                opportunity = Opportunity.objects.get(id=kwargs['id'])
                if opportunity.alumni == user:
                    opportunity.isActive = False
                    opportunity.save()
                    return Response({'message': 'Opportunity deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({'error': 'You are not authorized to delete opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'You are not authorized to delete opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to delete opportunities'}, status=status.HTTP_401_UNAUTHORIZED)


class OpportunitySkillViewSet(ModelViewSet):
    serializer_class = OpportunitySkillSerializer
    queryset = OpportunitySkill.objects.all()

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            super().list(request, *args, **kwargs)
        else:
            return Response({'error': 'You are not authorized to view opportunity skills'}, status=status.HTTP_401_UNAUTHORIZED)
        
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            super().retrieve(request, *args, **kwargs)
        else:
            return Response({'error': 'You are not authorized to view opportunity skills'}, status=status.HTTP_401_UNAUTHORIZED)
        
    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            if user.privilege == '3':
                opportunity = Opportunity.objects.get(id=request.data['opportunity_id'])
                if opportunity.alumni == user:
                    super().create(request, *args, **kwargs)
                else:
                    return Response({'error': 'You are not authorized to create opportunity skills'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'You are not authorized to create opportunity skills'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to create opportunity skills'}, status=status.HTTP_401_UNAUTHORIZED)
        
    def update(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            if user.privilege == '3':
                opportunity = Opportunity.objects.get(id=request.data['opportunity_id'])
                if opportunity.alumni == user:
                    super().update(request, *args, **kwargs)
                else:
                    return Response({'error': 'You are not authorized to update opportunity skills'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'You are not authorized to update opportunity skills'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to update opportunity skills'}, status=status.HTTP_401_UNAUTHORIZED)
        
    def partial_update(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            if user.privilege == '3':
                opportunity = Opportunity.objects.get(id=request.data['opportunity_id'])
                if opportunity.alumni == user:
                    super().update(request, *args, **kwargs)
                else:
                    return Response({'error': 'You are not authorized to update opportunity skills'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'You are not authorized to update opportunity skills'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to update opportunity skills'}, status=status.HTTP_401_UNAUTHORIZED)
        
    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            if user.privilege == '3' or user.is_superuser or user.privilege == '1':
                opportunity = Opportunity.objects.get(id=request.data['opportunity_id'])
                if opportunity.alumni == user:
                    skill = OpportunitySkill.objects.get(id=kwargs['id'])
                    skill.isActive = False
                    skill.save()
                    return Response({'message': 'Opportunity skill deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({'error': 'You are not authorized to delete opportunity skills'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'You are not authorized to delete opportunity skills'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to delete opportunity skills'}, status=status.HTTP_401_UNAUTHORIZED)

