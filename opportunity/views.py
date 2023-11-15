from opportunity.models import (
    Opportunity,
    OpportunitySkill,
    OpportunityApplication
)
from opportunity.serializers import (
    OpportunitySerializer,
    OpportunitySkillSerializer,
    OpportunityApplicationSerializer
)
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class OpportunityView(ModelViewSet):
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


class OpportunitySkillView(ModelViewSet):
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


class OpportunityApplicationView(ModelViewSet):
    serializer_class = OpportunityApplicationSerializer
    queryset = OpportunityApplication.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            application = OpportunityApplication.objects.filter(isActive=True)
            application = application.filter(Q(opportunity__alumni=user) | Q(applicant=user))
            if application.exists():
                    return Response(OpportunityApplicationSerializer(application).data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Opportunity applications not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'You are not authorized to view opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            application = OpportunityApplication.objects.filter(id=kwargs['pk'], isActive=True)
            if application.exists():
                if application.first().opportunity.alumni == user or application.first().applicant == user:
                    return Response(OpportunityApplicationSerializer(application.first()).data, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'You are not authorized to view opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'Opportunity application not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'You are not authorized to view opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            if user.privilege == '3':
                super().create(request, *args, **kwargs)
            else:
                return Response({'error': 'You are not authorized to create opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to create opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            if user.privilege == '1' or user.is_superuser:
                application = OpportunityApplication.objects.get(id=kwargs['id'])
                serializer = OpportunityApplicationSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.update(application, serializer.data)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'You are not authorized to update opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to update opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def partial_update(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            if user.privilege == '1' or user.is_superuser:
                application = OpportunityApplication.objects.get(id=kwargs['id'])
                serializer = OpportunityApplicationSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.update(application, serializer.data)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'You are not authorized to update opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to update opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)
        
    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            if user.privilege == '1' or user.is_superuser or user.privilege == '3':
                application = OpportunityApplication.objects.get(id=kwargs['id'])
                application.isActive = False
                application.save()
                return Response({'message': 'Opportunity application deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'You are not authorized to delete opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to delete opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)
