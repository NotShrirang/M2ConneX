from django.db import models
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncWeek, TruncMonth
from rest_framework import views, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserAnalytics
from .serializers import UserAnalyticsSerializer
from itertools import chain

from connection.models import Connection
from connection.serializers import ConnectionSerializer
from feed.models import Feed, FeedAction
from users.models import AlumniPortalUser


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


class YourInfluenceView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        current_user: AlumniPortalUser = request.user
        if not current_user.is_active:
            return Response({"data": "User is not active."}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.isVerified:
            return Response({"data": "User is not verified."}, status=status.HTTP_401_UNAUTHORIZED)

        # Get all connections of current user
        connectionA = Connection.objects.filter(
            Q(userA=current_user))
        connectionB = Connection.objects.filter(
            Q(userB=current_user))

        # Get all post count of current user's connections
        connection_post_count = 0
        for connection in connectionA:
            connection_post_count += connection.userB.feed.all().count()
        for connection in connectionB:
            connection_post_count += connection.userA.feed.all().count()

        connection_count = Connection.objects.filter(
            Q(userA=current_user) | Q(userB=current_user),
            status='accepted'
        ).count()

        # Get all feed of current user
        feed = current_user.feed

        # Get influence of current user
        feed_count = feed.count()

        actions = FeedAction.objects.filter(feed__user=current_user)
        action_count = actions.count()

        follower_count = Connection.objects.filter(
            userB=current_user, status='accepted').count()

        user_influence = connection_count + feed_count + action_count + follower_count

        total_influence = (
            Connection.objects.filter(status='accepted').count() +
            Feed.objects.annotate(action_count=Count('actions')).aggregate(Sum('action_count'))['action_count__sum'] +
            Connection.objects.filter(status='accepted').count()
        )

        if total_influence == 0:
            influence_percentage = 0

        if total_influence > 0:
            influence_percentage = round(
                (user_influence / total_influence) * 100, 2)

        # Get all connections of current user's connections
        connections = chain(connectionA, connectionB)
        serializer_data = ConnectionSerializer(connections, many=True).data

        # Get percentage of connected users actions on current user's feed.
        # Actions of connected users on current user's feed / total actions on current user's feed

        feed_actions = actions.filter(
            Q(user__in=connectionA.values_list('userB', flat=True)) |
            Q(user__in=connectionB.values_list('userA', flat=True))
        )

        feed_action_count = feed_actions.count()

        reach = actions.exclude(
            id__in=feed_actions.values_list('id', flat=True)).count()

        if action_count == 0:
            feed_action_percentage = 0

        if action_count > 0:
            feed_action_percentage = round(
                (feed_action_count / action_count) * 100, 2)

        return Response({
            'connection_count': connection_count,
            'follower_count': follower_count,
            'feed_count': feed_count,
            'action_count': action_count,
            'reach': reach,
            'connection_post_count': connection_post_count,
            'user_influence': user_influence,
            'influence_percentage': influence_percentage,
            'feed_action_percentage': feed_action_percentage,
            'connections': serializer_data
        }, status=status.HTTP_200_OK)
