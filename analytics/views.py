from django.db import models
from rest_framework import views, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from django.db.models.functions import TruncWeek, TruncMonth
from datetime import datetime, timedelta
from .models import UserAnalytics
from .serializers import UserAnalyticsSerializer


class UserAnalyticsView(viewsets.ModelViewSet):
    queryset = UserAnalytics.objects.all()
    serializer_class = UserAnalyticsSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['profileUser', 'visitor']
    search_fields = ['profileUser__firstName', 'profileUser__lastName',
                     'visitor__firstName', 'visitor__lastName']
    ordering_fields = ['-createdAt']

    def list(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({"data": "User is not active."}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.isVerified:
            return Response({"data": "User is not verified."}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = UserAnalytics.objects.filter(profileUser=current_user)
        serializer = UserAnalyticsSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({"data": "User is not active."}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.isVerified:
            return Response({"data": "User is not verified."}, status=status.HTTP_401_UNAUTHORIZED)
        if current_user.is_superuser:
            instance = UserAnalytics.objects.filter(id=kwargs['pk'])
        instance = UserAnalytics.objects.filter(
            profileUser=current_user, id=kwargs['pk'])
        if instance.exists():
            instance = instance.first()
            serializer = UserAnalyticsSerializer(instance)
            return Response(serializer.data)
        else:
            return Response({"data": "No such analytics."}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({"data": "User is not active."}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.isVerified:
            return Response({"data": "User is not verified."}, status=status.HTTP_401_UNAUTHORIZED)
        if 'visitor' not in request.data:
            return Response({"data": "Visitor not specified."}, status=status.HTTP_400_BAD_REQUEST)
        if 'analyticsType' not in request.data:
            return Response({"data": "Analytics type not specified."}, status=status.HTTP_400_BAD_REQUEST)
        visitor = request.data['visitor']
        if not visitor.isVerified:
            return Response({"data": "Visitor is not verified."}, status=status.HTTP_401_UNAUTHORIZED)
        if visitor == current_user:
            return Response({"data": "Visitor cannot be same as profile user."}, status=status.HTTP_400_BAD_REQUEST)
        data = {
            'profileUser': current_user.id,
            'visitor': visitor.id,
            'analyticsType': request.data['analyticsType']
        }
        serializer = UserAnalyticsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return Response({"data": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response({"data": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response({"data": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class AnalyticsCountView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({"data": "User is not active."}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.isVerified:
            return Response({"data": "User is not verified."}, status=status.HTTP_401_UNAUTHORIZED)
        analytics_data = {}
        total_data = UserAnalytics.objects.filter(profileUser=current_user).values(
            'analyticsType').annotate(count=models.Count('analyticsType'))
        total_data = {item['analyticsType']: item['count']
                      for item in total_data}
        weekly_data = UserAnalytics.objects.filter(profileUser=current_user).annotate(
            week_start=TruncWeek('createdAt')
        ).values('week_start').annotate(count=Count('id')).order_by('week_start')
        weekly_data = {str(item['week_start']): item['count']
                       for item in weekly_data}
        monthly_data = UserAnalytics.objects.filter(profileUser=current_user).annotate(
            month_start=TruncMonth('createdAt')
        ).values('month_start').annotate(count=Count('id')).order_by('month_start')
        monthly_data = {str(item['month_start']): item['count']
                        for item in monthly_data}
        analytics_data['total'] = total_data
        analytics_data['weekly'] = weekly_data
        analytics_data['monthly'] = monthly_data
        return Response(analytics_data, status=status.HTTP_200_OK)
