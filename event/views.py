from event.models import Event, EventImage
from event.serializers import EventSerializer, EventImageSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class EventView(ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated,]

    def list(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_active:
            return super().list(request, *args, **kwargs)
        else:
            return Response({"error": "Your account is not active. Please contact admin"}, status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_active:
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response({"error": "Your account is not active. Please contact admin"}, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_active:
            if current_user.privilege in ['1', '2'] or current_user.is_superuser:
                return super().create(request, *args, **kwargs)
            else:
                return Response({"error": "You are not authorized to create an event"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error": "Your account is not active. Please contact admin"}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_active:
            if current_user.privilege == '1' or current_user.is_superuser:
                return super().update(request, *args, **kwargs)
            elif current_user.privilege == '2':
                event = Event.objects.get(id=kwargs['pk'])
                if event.createdByUser == current_user:
                    return super().update(request, *args, **kwargs)
                else:
                    return Response({"error": "You are not authorized to update this event"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"error": "You are not authorized to update an event"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error": "Your account is not active. Please contact admin"}, status=status.HTTP_401_UNAUTHORIZED)

    def partial_update(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_active:
            if current_user.privilege == '1' or current_user.is_superuser:
                return super().partial_update(request, *args, **kwargs)
            elif current_user.privilege == '2':
                event = Event.objects.get(id=kwargs['pk'])
                if event.createdByUser == current_user:
                    return super().partial_update(request, *args, **kwargs)
                else:
                    return Response({"error": "You are not authorized to update this event"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"error": "You are not authorized to update an event"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error": "Your account is not active. Please contact admin"}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_active:
            event = Event.objects.get(id=kwargs['pk'])
            if current_user.privilege == '1' or current_user.is_superuser:
                event.isActive = False
                event.save()
                return Response({"success": "Event deleted successfully"}, status=status.HTTP_200_OK)
            elif current_user.privilege == '2':
                if event.createdByUser == current_user:
                    event.isActive = False
                    event.save()
                    return Response({"success": "Event deleted successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "You are not authorized to destroy this event"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"error": "You are not authorized to destroy an event"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error": "Your account is not active. Please contact admin"}, status=status.HTTP_401_UNAUTHORIZED)


class EventImageView(ModelViewSet):
    serializer_class = EventImageSerializer
    queryset = EventImage.objects.all()
    permission_classes = [IsAuthenticated,]
