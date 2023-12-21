from django.db.models import Q
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics

from analytics.models import UserAnalytics
from analytics.serializers import UserAnalyticsSerializer
from connection.models import Connection
from connection.serializers import ConnectionSerializer
from connection.filters import ConnectionFilter
from users.models import AlumniPortalUser
from users.serializers import AlumniPortalUserSerializer, RecommendUserSerializer
from CODE.utils.recommendations import get_user_recommendation


class ConnectionView(ModelViewSet):
    serializer_class = ConnectionSerializer
    queryset = Connection.objects.all()
    filterset_class = ConnectionFilter
    search_fields = [
        'userA__firstName',
        'userA__lastName',
        'userA__email',
        'userB__firstName',
        'userB__lastName',
        'userB__email',
        'status'
    ]
    ordering_fields = (
        'createdAt',
        'updatedAt',
    )
    ordering = ('-createdAt',)

    def list(self, request, *args, **kwargs):
        current_user: AlumniPortalUser = request.user
        if current_user.is_active is False:
            return Response({"detail": "User is not active"}, status=400)
        elif current_user.isVerified is False:
            return Response({"detail": "User is not verified"}, status=400)
        else:
            queryset = Connection.objects.filter(
                Q(userA=current_user) | Q(userB=current_user))
            serializer = ConnectionSerializer(queryset, many=True)
            return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        connectionId = kwargs.get('pk')
        connection = Connection.objects.filter(id=connectionId)
        if not connection.exists():
            return Response({"detail": "Connection does not exist"}, status=400)
        connection = connection.first()
        current_user: AlumniPortalUser = request.user
        if current_user.is_active is False:
            return Response({"detail": "User is not active"}, status=400)
        elif current_user.isVerified is False:
            return Response({"detail": "User is not verified"}, status=400)
        else:
            serializer = ConnectionSerializer(connection)
            return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        userA: AlumniPortalUser = request.user
        userB = request.data.get('userB')
        data = {
            "userA": userA.id,
            "userB": userB,
            "status": "pending"
        }
        serializer = ConnectionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def update(self, request, *args, **kwargs):
        connectionId = kwargs.get('pk')
        connection = Connection.objects.filter(id=connectionId)
        if not connection.exists():
            return Response({"detail": "Connection does not exist"}, status=400)
        connection = connection.first()
        current_user: AlumniPortalUser = request.user
        if current_user.is_active is False:
            return Response({"detail": "User is not active"}, status=400)
        elif current_user.isVerified is False:
            return Response({"detail": "User is not verified"}, status=400)
        else:
            serializer = ConnectionSerializer(
                connection, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.update(connection, serializer.validated_data)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)

    def partial_update(self, request, *args, **kwargs):
        connectionId = kwargs.get('pk')
        connection = Connection.objects.filter(id=connectionId)
        if not connection.exists():
            return Response({"detail": "Connection does not exist"}, status=400)
        connection = connection.first()
        current_user: AlumniPortalUser = request.user
        if current_user.is_active is False:
            return Response({"detail": "User is not active"}, status=400)
        elif current_user.isVerified is False:
            return Response({"detail": "User is not verified"}, status=400)
        else:
            serializer = ConnectionSerializer(
                connection, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.update(connection, serializer.validated_data)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        connectionId = kwargs.get('pk')
        connection = Connection.objects.filter(id=connectionId, isActive=True)
        if not connection.exists():
            return Response({"detail": "Connection does not exist"}, status=400)
        connection = connection.first()
        current_user: AlumniPortalUser = request.user
        if connection.userA != current_user and connection.userB != current_user:
            return Response({"detail": "User is not authorized to delete this connection"}, status=400)
        if current_user.is_active is False:
            return Response({"detail": "User is not active"}, status=400)
        elif current_user.isVerified is False:
            return Response({"detail": "User is not verified"}, status=400)
        else:
            connection.isActive = False
            connection.save()
            return Response({"detail": "Connection deleted successfully"}, status=200)


class ConnectionRequestView(APIView):
    """
    View to send a connection request

    * Requires token authentication.
    * Only active and verified users are able to send a connection request
    * User A is the user who sends the connection request
    * User B is the user who receives the connection request
    * User B must be active and verified
    * User A must not have sent a connection request to User B before

    * Request: POST

    * Parameters:
        * userB: User B's id

    * Response:
        * 200: Connection request sent successfully
        * 400: Bad request

    * Sample request:
        {
            "userB": 2
        }

    * Sample response:
        {
            "id": 1,
            "userA": 1,
            "userB": 2,
            "status": "pending",
        }
    """

    def post(self, request, *args, **kwargs):
        current_user: AlumniPortalUser = request.user
        if not current_user.is_active:
            return Response({"detail": "User is not active"}, status=400)
        elif not current_user.isVerified:
            return Response({"detail": "User is not verified"}, status=400)
        qs = AlumniPortalUser.objects.filter(
            id=request.data.get('userB', None))
        if qs.exists():
            userB = qs.first()
            if userB.is_active is False:
                return Response({"detail": "User B is not active"}, status=400)
            elif userB.isVerified is False:
                return Response({"detail": "User B is not verified"}, status=400)
            else:
                connection_qs = Connection.objects.filter(
                    userA=current_user.id, userB=userB.id, status="pending")
                if connection_qs.exists():
                    return Response({"detail": "Connection request already sent"}, status=400)
                else:
                    data = {
                        'userA': current_user.id,
                        'userB': userB.id,
                        'status': 'pending'
                    }
                    serializer = ConnectionSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        # TODO: Add notifications.
                        return Response(serializer.data, status=200)
                    else:
                        return Response(serializer.errors, status=400)
        else:
            return Response({"detail": "User B does not exist"}, status=400)


class ConnectionRequestAcceptView(APIView):
    def post(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response({"detail": "User is not active"}, status=400)
        elif not current_user.isVerified:
            return Response({"detail": "User is not verified"}, status=400)
        connection = Connection.objects.filter(
            id=request.data.get('connectionId'))
        if not connection.exists():
            return Response({"detail": "Connection request does not exist"}, status=400)
        connection = connection.first()
        if connection.userB != current_user:
            return Response({"detail": "User is not authorized to accept this connection request"}, status=400)
        if connection.userA.is_active is False:
            return Response({"detail": "User A is not active"}, status=400)
        elif connection.userA.isVerified is False:
            return Response({"detail": "User A is not verified"}, status=400)
        if connection.isActive:
            if connection.status == 'accepted':
                return Response({"details": "Connection request already accepted."}, status=400)
            else:
                connection.status = 'accepted'
                connection.save()
                UserAnalytics.objects.create(
                    profileUser=connection.userA,
                    visitor=connection.userB,
                    analyticsType='connection'
                )
                UserAnalytics.objects.create(
                    profileUser=connection.userB,
                    visitor=connection.userA,
                    analyticsType='connection'
                )
                return Response({"details": "Connection request accepted successfully."}, status=200)
        else:
            return Response({"details": "Connection request does not exist."}, status=400)


class RecommendConnectionView(generics.ListAPIView):
    serializer_class = ConnectionSerializer
    queryset = Connection.objects.all()
    filterset_class = ConnectionFilter
    permission_classes = [IsAuthenticated,]
    search_fields = ['userA__firstName', 'userA__lastName',
                     'userA__email', 'userB__firstName', 'userB__lastName', 'userB__email']
    ordering = ('-createdAt',)

    def list(self, request, *args, **kwargs):
        current_user = request.user

        if not current_user.is_active:
            return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)

        if not current_user.isVerified:
            return Response({'message': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)

        userA_connected = Connection.objects.filter(
            userA=current_user, status='accepted').values_list('userB', flat=True)
        userB_connected = Connection.objects.filter(
            userB=current_user, status='accepted').values_list('userA', flat=True)

        qs = AlumniPortalUser.objects.filter(is_active=True, isVerified=True).exclude(
            id__in=userA_connected).exclude(id__in=userB_connected).exclude(id=current_user.id)

        if not qs.exists():
            return Response({'message': 'No users to recommend'}, status=status.HTTP_200_OK)
        if qs.count() == 1:
            page = self.paginate_queryset(qs)
            if page is not None:
                serializer = RecommendUserSerializer(
                    page, context={'request': request}, many=True)
                return self.get_paginated_response(serializer.data)
            else:
                serializer = RecommendUserSerializer(
                    qs, context={'request': request}, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        qs, similarity_score = get_user_recommendation(qs, current_user)

        # Paginate the queryset
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = RecommendUserSerializer(
                page, context={'request': request}, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)
