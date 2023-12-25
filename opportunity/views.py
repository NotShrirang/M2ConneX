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
from opportunity.filters import (
    OpportunityFilter,
    OpportunityApplicationFilter,
    OpportunitySkillFilter
)
from users.models import AlumniPortalUser, Student
from django.db.models import Q
from django.db.models.query import QuerySet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, pagination
from rest_framework.permissions import IsAuthenticated
from CODE.utils.notifications import create_notification


class OpportunityView(ModelViewSet):
    serializer_class = OpportunitySerializer
    permission_classes = [IsAuthenticated]
    queryset = Opportunity.objects.all()
    filterset_class = OpportunityFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = [
        'name',
        'description',
        'user__firstName',
        'user__lastName',
        'type',
        'companyName',
        'location',
        'workMode',
        'isPaid',
        'skills__skill__name'
    ]

    def list(self, request, *args, **kwargs):
        user = request.user
        if not user.isVerified:
            return Response({'error': 'You are not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_active:
            opportunities = self.filter_queryset(
                self.queryset.filter(isActive=True))
            opportunities = opportunities.exclude(
                applications__applicant=user)
            opportunities = opportunities.exclude(user=user)
            page = self.paginate_queryset(opportunities)
            if page is not None:
                serializer = OpportunitySerializer(
                    page, many=True, context={'request': request})
                return self.get_paginated_response(serializer.data)
            serializer = OpportunitySerializer(
                opportunities, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are not authorized to view opportunities'}, status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        if not user.isVerified:
            return Response({'error': 'You are not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_active:
            qs = Opportunity.objects.filter(id=kwargs['pk'], isActive=True)
            if qs.exists():
                serializer = OpportunitySerializer(
                    qs.first(), context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Opportunity not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'You are not authorized to view opportunities'}, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.isVerified:
            return Response({'error': 'You are not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        if current_user.is_active:
            data = request.data
            user = AlumniPortalUser.objects.filter(user=current_user.id)
            if user.exists():
                data['user'] = user.first().id
            else:
                return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = OpportunitySerializer(
                data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'You are not authorized to create opportunities'}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.isVerified:
            return Response({'error': 'You are not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        if current_user.is_active:
            opportunity = Opportunity.objects.get(id=kwargs['id'])
            if opportunity.user == current_user:
                request.data['user'] = current_user.id
                serializer = OpportunitySerializer(
                    data=request.data, context={'request': request})
                if serializer.is_valid():
                    serializer.update(opportunity, serializer.data)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'You are not authorized to update opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to update opportunities'}, status=status.HTTP_401_UNAUTHORIZED)

    def partial_update(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.isVerified:
            return Response({'error': 'You are not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        if current_user.is_active:
            opportunity = Opportunity.objects.get(id=kwargs['id'])
            if opportunity.user == current_user:
                request.data['user'] = current_user.id
                serializer = OpportunitySerializer(
                    data=request.data, context={'request': request})
                if serializer.is_valid():
                    serializer.update(
                        opportunity, serializer.data, partial=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'You are not authorized to update opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to update opportunities'}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.isVerified:
            return Response({'error': 'You are not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        if current_user.is_active:
            opportunity = Opportunity.objects.get(id=kwargs['id'])
            if opportunity.user == current_user:
                opportunity.isActive = False
                opportunity.save()
                return Response({'message': 'Opportunity deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'You are not authorized to delete opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to delete opportunities'}, status=status.HTTP_401_UNAUTHORIZED)


class OpportunitySkillView(ModelViewSet):
    serializer_class = OpportunitySkillSerializer
    queryset = OpportunitySkill.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_class = OpportunitySkillFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['opportunity__name', 'skill__name']

    def list(self, request, *args, **kwargs):
        user = request.user
        if not user.isVerified:
            return Response({'error': 'You are not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_active:
            qs = self.filter_queryset(self.queryset.filter(isActive=True))
            serializer = OpportunitySkillSerializer(qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are not authorized to view opportunity skills'}, status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        if not user.isVerified:
            return Response({'error': 'You are not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_active:
            qs = OpportunitySkill.objects.filter(
                id=kwargs['pk'], isActive=True)
            if qs.exists():
                serializer = OpportunitySkillSerializer(qs.first())
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Opportunity skill not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'You are not authorized to view opportunity skills'}, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.isVerified:
            return Response({'error': 'You are not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_active:
            if user.privilege == 'Alumni':
                opportunity = Opportunity.objects.get(
                    id=request.data['opportunity_id'])
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
        if not user.isVerified:
            return Response({'error': 'You are not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_active:
            if user.privilege == 'Alumni':
                opportunity = Opportunity.objects.get(
                    id=request.data['opportunity_id'])
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
        if not user.isVerified:
            return Response({'error': 'You are not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_active:
            if user.privilege == 'Alumni':
                opportunity = Opportunity.objects.get(
                    id=request.data['opportunity_id'])
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
        if not user.isVerified:
            return Response({'error': 'You are not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_active:
            if user.privilege == 'Alumni' or user.is_superuser or user.privilege == 'Super Admin':
                opportunity = Opportunity.objects.get(
                    id=request.data['opportunity_id'])
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
    filterset_class = OpportunityApplicationFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['opportunity__name', 'applicant__firstName',
                     'applicant__lastName', 'status']

    def list(self, request, *args, **kwargs):
        user = request.user
        if not user.isVerified:
            return Response({'error': 'You are not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_active:
            alumni = AlumniPortalUser.objects.filter(user=user.id)
            if alumni.exists():
                application = self.filter_queryset(
                    self.queryset.filter(isActive=True))
                application = application.filter(
                    opportunity__alumni=alumni.first())
                if application.exists():
                    return Response(OpportunityApplicationSerializer(application, many=True).data, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Opportunity applications not found.'}, status=status.HTTP_404_NOT_FOUND)
            student = Student.objects.filter(user=user.id)
            if student.exists():
                application = self.filter_queryset(
                    self.queryset.filter(isActive=True))
                application = application.filter(applicant=student.first())
                if application.exists():
                    return Response(OpportunityApplicationSerializer(application, many=True).data, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Opportunity applications not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'You are not authorized to view opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        if not user.isVerified:
            return Response({'error': 'You are not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_active:
            application = OpportunityApplication.objects.filter(
                id=kwargs['pk'], isActive=True)
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
        current_user = request.user
        if not current_user.isVerified:
            return Response({'error': 'You are not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.is_active:
            return Response({'error': 'You are not authorized to create opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)
        if 'opportunityId' not in request.data:
            return Response({'error': 'opportunityId is required'}, status=status.HTTP_400_BAD_REQUEST)
        if 'about' not in request.data:
            return Response({'error': 'about is required'}, status=status.HTTP_400_BAD_REQUEST)
        qs = Opportunity.objects.filter(
            id=request.data['opportunityId'], isActive=True)
        if qs.exists():
            opportunity = qs.first()
            if opportunity.user == current_user:
                return Response({'error': 'You are not authorized to create opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)
            if opportunity.applications.filter(applicant=current_user).exists():
                return Response({'error': 'You have already applied for this opportunity'}, status=status.HTTP_400_BAD_REQUEST)
            data = {
                'opportunity': request.data['opportunityId'],
                'applicant': current_user.id,
                'about': request.data['about']
            }
            serializer = OpportunityApplicationSerializer(
                data=data)
            if serializer.is_valid():
                serializer.save()
                application: OpportunityApplication = serializer.instance
                create_notification(
                    user=current_user,
                    notification_type='OPPORTUNITY_APPLICATION',
                    object=application
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'You are not authorized to create opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        user = request.user
        if not user.isVerified:
            return Response({'error': 'You are not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_active:
            if user.privilege == 'Student' or user.is_superuser:
                application = OpportunityApplication.objects.get(
                    id=kwargs['id'])
                if application.applicant == user:
                    serializer = OpportunityApplicationSerializer(
                        data=request.data)
                    if serializer.is_valid():
                        serializer.update(application, serializer.data)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'You are not authorized to update opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'You are not authorized to update opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to update opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)

    def partial_update(self, request, *args, **kwargs):
        user = request.user
        if not user.isVerified:
            return Response({'error': 'You are not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_active:
            if user.privilege == 'Student' or user.is_superuser:
                application = OpportunityApplication.objects.get(
                    id=kwargs['id'])
                if application.applicant == user:
                    serializer = OpportunityApplicationSerializer(
                        data=request.data)
                    if serializer.is_valid():
                        serializer.update(application, serializer.data)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'You are not authorized to update opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'You are not authorized to update opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to update opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if not user.isVerified:
            return Response({'error': 'You are not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_active:
            if user.privilege == 'Student' or user.is_superuser or user.privilege == 'Super Admin':
                application = OpportunityApplication.objects.get(
                    id=kwargs['id'])
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
        if not user.isVerified:
            return Response({'error': 'You are not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_active:
            if application.opportunity.user == user or user.is_superuser:
                application = OpportunityApplication.objects.get(
                    id=request.data['application_id'])
                application.status = 'ACCEPTED'
                application.save()
                create_notification(
                    user=application.applicant,
                    notification_type='OPPORTUNITY_APPLICATION_ACCEPTED',
                    object=application
                )
                return Response({'message': 'Opportunity application accepted successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'You are not authorized to accept opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to accept opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)


class RejectOpportunityApplication(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.isVerified:
            return Response({'error': 'You are not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_active:
            if application.opportunity.user == user or user.is_superuser:
                application = OpportunityApplication.objects.get(
                    id=request.data['application_id'])
                application.status = 'REJECTED'
                application.save()
                create_notification(
                    user=application.applicant,
                    notification_type='OPPORTUNITY_APPLICATION_REJECTED',
                    object=application
                )
                return Response({'message': 'Opportunity application rejected successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'You are not authorized to reject opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'You are not authorized to reject opportunity applications'}, status=status.HTTP_401_UNAUTHORIZED)


class RecommendOpportunityView(generics.ListAPIView):
    serializer_class = OpportunitySerializer
    queryset = Opportunity.objects.all()
    filterset_class = OpportunityFilter
    pagination_class = pagination.PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'description', 'companyName',
                     'location', 'workMode', 'skills__skill__name']

    def list(self, request, *args, **kwargs):
        user = request.user
        if not user.isVerified:
            return Response({'error': 'You are not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        search_query = request.GET.get('search', '')
        if user.is_active:
            qs = self.filter_queryset(self.queryset).filter(isActive=True)
            qs = qs.filter(Q(name__icontains=search_query) | Q(
                description__icontains=search_query) | Q(companyName__icontains=search_query))
            qs = qs.exclude(user=user)
            qs = qs.exclude(applications__applicant=user)
            final_qs = []
            user_skills: QuerySet = user.skills.all()
            if user_skills.count() == 0:
                qs = Opportunity.objects.filter(isActive=True)
                page = self.paginate_queryset(qs)
                if page is not None:
                    serializer = OpportunitySerializer(
                        page, many=True, context={'request': request})
                    return self.get_paginated_response(serializer.data)
                serializer = OpportunitySerializer(
                    qs, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            for opportunity in qs:
                opportunity_skills = opportunity.skills
                intersected_skills = opportunity_skills.filter(
                    skill__name__in=user_skills.values_list('skill__name', flat=True))
                serializer = OpportunitySerializer(
                    opportunity, context={'request': request})
                data = serializer.data
                if opportunity_skills.count() > 0:
                    ratio = intersected_skills.count() / opportunity_skills.count()
                    data['matchRatio'] = ratio
                else:
                    data['matchRatio'] = 0
                data['matchedSkills'] = intersected_skills.values_list(
                    'skill__name', flat=True)
                final_qs.append(data)
            final_qs = sorted(
                final_qs, key=lambda x: x['matchRatio'], reverse=True)
            page = self.paginate_queryset(final_qs)
            if page is not None:
                return self.get_paginated_response(page)
            return Response(final_qs, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are not authorized to view opportunities'}, status=status.HTTP_401_UNAUTHORIZED)
