from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import status, pagination

from event.models import Event, EventImage
from event.serializers import EventSerializer, EventImageSerializer
from event.filters import EventFilter
from club.models import Club, ClubMember


class EventView(ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    pagination_class = pagination.PageNumberPagination
    filterset_class = EventFilter
    filterset_fields = ['department', 'club']
    search_fields = ['name', 'description', 'venue', 'department']
    permission_classes = [IsAuthenticated,]

    def list(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.isVerified:
            return Response({"error": "Your account is not verified. Please contact admin"}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.is_active:
            return Response({"error": "Your account is not active. Please contact admin"}, status=status.HTTP_401_UNAUTHORIZED)
        qs = self.filter_queryset(self.queryset.filter(isActive=True))
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            return Response(response.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.isVerified:
            return Response({"error": "Your account is not verified. Please contact admin"}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.is_active:
            return Response({"error": "Your account is not active. Please contact admin"}, status=status.HTTP_401_UNAUTHORIZED)
        event = Event.objects.get(id=kwargs['pk'])
        serializer = self.get_serializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.isVerified:
            return Response({"error": "Your account is not verified. Please contact admin"}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.is_active:
            return Response({"error": "Your account is not active. Please contact admin"}, status=status.HTTP_401_UNAUTHORIZED)
        if 'club' not in request.data:
            if current_user.privilege in ['Super Admin', 'Staff'] or current_user.is_superuser:
                data = {
                    'name': request.data['name'],
                    'description': request.data['description'],
                    'date': request.data['date'],
                    'time': request.data['time'],
                    'venue': request.data['venue'],
                    'department': request.data['department'],
                    'link': request.data['link'],
                    'isClubEvent': False,
                    'club': None,
                    'createdByUser': current_user.id,
                }
                serializer = self.get_serializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "You are not authorized to create an event"}, status=status.HTTP_401_UNAUTHORIZED)
        club = Club.objects.get(id=request.data['club'])
        if not club:
            return Response({"error": "Club not found"}, status=status.HTTP_404_NOT_FOUND)
        club_member = ClubMember.objects.filter(
            user=current_user, club=club, isClubAdmin=True)
        if not club_member.exists():
            return Response({"error": "You are not a club admin"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            club_member = club_member.first()
            data = {
                'name': request.data['name'],
                'description': request.data['description'],
                'date': request.data['date'],
                'time': request.data['time'],
                'venue': request.data['venue'],
                'department': request.data['department'],
                'link': request.data['link'],
                'isClubEvent': True,
                'club': club_member.club.id,
                'createdByUser': current_user.id,
            }
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.isVerified:
            return Response({"error": "Your account is not verified. Please contact admin"}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.is_active:
            return Response({"error": "Your account is not active. Please contact admin"}, status=status.HTTP_401_UNAUTHORIZED)
        if 'club' not in request.data:
            if current_user.privilege in ['Super Admin', 'Staff'] or current_user.is_superuser:
                event = Event.objects.get(id=kwargs['pk'])
                if event.createdByUser == current_user:
                    data = {
                        'name': request.data['name'],
                        'description': request.data['description'],
                        'date': request.data['date'],
                        'time': request.data['time'],
                        'venue': request.data['venue'],
                        'department': request.data['department'],
                        'link': request.data['link'],
                        'isClubEvent': False,
                        'club': None,
                        'createdByUser': current_user.id,
                    }
                    serializer = self.get_serializer(event)
                    if serializer.is_valid():
                        serializer.update(event, data)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error": "You are not authorized to update this event"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"error": "You are not authorized to update an event"}, status=status.HTTP_401_UNAUTHORIZED)
        club = Club.objects.get(id=request.data['club'])
        if not club:
            return Response({"error": "Club not found"}, status=status.HTTP_404_NOT_FOUND)
        club_member = ClubMember.objects.filter(
            user=current_user, club=club, isClubAdmin=True)
        if not club_member.exists():
            return Response({"error": "You are not a club admin"}, status=status.HTTP_401_UNAUTHORIZED)
        club_member = club_member.first()
        event = Event.objects.get(id=kwargs['pk'])
        if event.club == club_member.club:
            data = {
                'name': request.data['name'],
                'description': request.data['description'],
                'date': request.data['date'],
                'time': request.data['time'],
                'venue': request.data['venue'],
                'department': request.data['department'],
                'link': request.data['link'],
                'isClubEvent': True,
                'club': club_member.club.id,
            }
            serializer = self.get_serializer(event)
            if serializer.is_valid():
                serializer.update(event, data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You are not authorized to update this event"}, status=status.HTTP_401_UNAUTHORIZED)

    def partial_update(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.isVerified:
            return Response({"error": "Your account is not verified. Please contact admin"}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.is_active:
            return Response({"error": "Your account is not active. Please contact admin"}, status=status.HTTP_401_UNAUTHORIZED)
        if 'club' not in request.data:
            if current_user.privilege in ['Super Admin', 'Staff'] or current_user.is_superuser:
                event = Event.objects.get(id=kwargs['pk'])
                if event.createdByUser == current_user:
                    data = {
                        'name': request.data['name'],
                        'description': request.data['description'],
                        'date': request.data['date'],
                        'time': request.data['time'],
                        'venue': request.data['venue'],
                        'department': request.data['department'],
                        'link': request.data['link'],
                        'isClubEvent': False,
                        'club': None,
                        'createdByUser': current_user.id,
                    }
                    serializer = self.get_serializer(event)
                    if serializer.is_valid():
                        serializer.update(event, data, partial=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error": "You are not authorized to update this event"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"error": "You are not authorized to update an event"}, status=status.HTTP_401_UNAUTHORIZED)
        club = Club.objects.get(id=request.data['club'])
        if not club:
            return Response({"error": "Club not found"}, status=status.HTTP_404_NOT_FOUND)
        club_member = ClubMember.objects.filter(
            user=current_user, club=club, isClubAdmin=True)
        if not club_member.exists():
            return Response({"error": "You are not a club admin"}, status=status.HTTP_401_UNAUTHORIZED)
        club_member = club_member.first()
        event = Event.objects.get(id=kwargs['pk'])
        if event.club == club_member.club:
            data = {
                'name': request.data['name'],
                'description': request.data['description'],
                'date': request.data['date'],
                'time': request.data['time'],
                'venue': request.data['venue'],
                'department': request.data['department'],
                'link': request.data['link'],
                'isClubEvent': True,
                'club': club_member.club.id,
            }
            serializer = self.get_serializer(event)
            if serializer.is_valid():
                serializer.update(event, data, partial=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You are not authorized to update this event"}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.isVerified:
            return Response({"error": "Your account is not verified. Please contact admin"}, status=status.HTTP_401_UNAUTHORIZED)
        if not current_user.is_active:
            return Response({"error": "Your account is not active. Please contact admin"}, status=status.HTTP_401_UNAUTHORIZED)
        event = Event.objects.get(id=kwargs['pk'])
        if event.createdByUser == current_user:
            event.delete()
            return Response({"success": "Event deleted successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You are not authorized to delete this event"}, status=status.HTTP_401_UNAUTHORIZED)


class EventImageView(ModelViewSet):
    serializer_class = EventImageSerializer
    queryset = EventImage.objects.all()
    permission_classes = [IsAuthenticated,]
