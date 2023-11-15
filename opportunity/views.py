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
from django.db.models.query import QuerySet
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class OpportunityView(ModelViewSet):
    serializer_class = OpportunitySerializer
    queryset = Opportunity.objects.all()
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'description', 'alumni__user__firstName', 'alumni__user__lastName', 'type', 'companyName', 'location', 'locationType', 'skills__skill__name']

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            qs = Opportunity.objects.filter(isActive=True)
            serializer = OpportunitySerializer(qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are not authorized to view opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            qs = Opportunity.objects.filter(id=kwargs['pk'], isActive=True)
            if qs.exists():
                serializer = OpportunitySerializer(qs.first())
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Opportunity not found'}, status=status.HTTP_404_NOT_FOUND)
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
    permission_classes = [IsAuthenticated]
    search_fields = ['opportunity__name', 'skill__name']

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            qs = OpportunitySkill.objects.filter(isActive=True)
            serializer = OpportunitySkillSerializer(qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are not authorized to view opportunity skills'}, status=status.HTTP_401_UNAUTHORIZED)
        
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            qs = OpportunitySkill.objects.filter(id=kwargs['pk'], isActive=True)
            if qs.exists():
                serializer = OpportunitySkillSerializer(qs.first())
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Opportunity skill not found'}, status=status.HTTP_404_NOT_FOUND)
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
    search_fields = ['opportunity__name', 'applicant__user__firstName', 'applicant__user__lastName', 'status']

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


class AcceptOpportunityApplication(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            if application.opportunity.alumni == user or user.is_superuser:
                application = OpportunityApplication.objects.get(id=request.data['application_id'])
                application.status = 'ACCEPTED'
                application.save()
                # TODO: Send email to applicant
                return Response({'message': 'Opportunity application accepted successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'You are not authorized to accept opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to accept opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)


class RejectOpportunityApplication(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            if application.opportunity.alumni == user or user.is_superuser:
                application = OpportunityApplication.objects.get(id=request.data['application_id'])
                application.status = 'REJECTED'
                application.save()
                # TODO: Send email to applicant
                return Response({'message': 'Opportunity application rejected successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'You are not authorized to reject opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to reject opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)


class RecommendOpportunityView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            qs = Opportunity.objects.filter(isActive=True)
            final_qs = []
            for opportunity in qs:
                user_skills: QuerySet = user.skills.all()
                opportunity_skills = opportunity.skills
                intersected_skills = opportunity_skills.filter(skill__name__in=user_skills.values_list('skill__name', flat=True))
                ratio = intersected_skills.count() / opportunity_skills.count()
                serializer = OpportunitySerializer(opportunity)
                data = serializer.data
                data['matchRatio'] = ratio
                data['matchedSkills'] = intersected_skills.values_list('skill__name', flat=True)
                if intersected_skills.count() > 0:
                    final_qs.append(data)
            return Response(final_qs, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are not authorized to view opportunities'}, status=status.HTTP_401_UNAUTHORIZED)