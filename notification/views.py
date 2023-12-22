from rest_framework import views, viewsets, permissions, status, pagination
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


class NotificationView(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = NotificationSerializer
    pagination_class = pagination.PageNumberPagination
    ordering = ['-createdAt']

    def list(self, request):
        current_user = request.user
        if not current_user.is_active:
            return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)

        if not current_user.isVerified:
            return Response({'message': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)

        queryset = Notification.objects.filter(
            user=current_user, isActive=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = NotificationSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        return Response({"message": "This method is not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, pk=None):
        return Response({"message": "This method is not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        return Response({"message": "This method is not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response({"message": "This method is not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        return Response({"message": "This method is not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class NotificationReadView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def post(self, request):
        current_user = request.user
        if not current_user.is_active:
            return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)

        if not current_user.isVerified:
            return Response({'message': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)

        notificationId = request.data.get('notificationId')
        if not notificationId:
            return Response({'message': 'notificationId is required'}, status=status.HTTP_400_BAD_REQUEST)

        notifications = Notification.objects.filter(
            id=notificationId, user=current_user)
        if not notifications:
            return Response({'message': 'No notifications found'}, status=status.HTTP_404_NOT_FOUND)
        notification = notifications.first()
        notification.isRead = True
        notification.save()
        return Response({'message': 'Notifications marked as read.'}, status=status.HTTP_200_OK)
