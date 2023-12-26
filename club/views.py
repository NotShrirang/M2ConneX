from rest_framework import viewsets, filters, pagination, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Club, ClubMember
from .serializers import ClubSerializer, ClubMemberSerializer

from users.models import AlumniPortalUser


class ClubView(viewsets.ModelViewSet):
    serializer_class = ClubSerializer
    queryset = Club.objects.all()
    pagination_class = pagination.PageNumberPagination
    search_fields = ['name', 'website', 'email']
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    ordering_fields = ['name', '-createdAt', '-updatedAt']
    ordering = ['-createdAt']

    def list(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response("User is not active", status=status.HTTP_403_FORBIDDEN)
        if not current_user.isVerified:
            return Response("User is not verified", status=status.HTTP_403_FORBIDDEN)
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.order_by('name')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_active:
            return Response("User is not active", status=status.HTTP_403_FORBIDDEN)
        if not current_user.isVerified:
            return Response("User is not verified", status=status.HTTP_403_FORBIDDEN)
        clubId = kwargs['pk']
        club = Club.objects.filter(id=clubId).first()
        if not club:
            return Response("Club not found", status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(club)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        current_user: AlumniPortalUser = request.user
        if not current_user.is_active:
            return Response("User is not active", status=status.HTTP_403_FORBIDDEN)
        if not current_user.isVerified:
            return Response("User is not verified", status=status.HTTP_403_FORBIDDEN)
        if not current_user.privilege == 'Super Admin':
            return Response("User is not super admin", status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        current_user: AlumniPortalUser = request.user
        if not current_user.is_active:
            return Response("User is not active", status=status.HTTP_403_FORBIDDEN)
        if not current_user.isVerified:
            return Response("User is not verified", status=status.HTTP_403_FORBIDDEN)
        if not current_user.privilege == 'Super Admin':
            return Response("User is not super admin", status=status.HTTP_403_FORBIDDEN)
        clubId = kwargs['pk']
        club = Club.objects.filter(id=clubId).first()
        if not club:
            return Response("Club not found", status=status.HTTP_404_NOT_FOUND)
        admin = club.members.filter(
            user=current_user, isClubAdmin=True)
        if not admin:
            return Response("User is not club admin", status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(club)
        serializer.update(club, request.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        current_user: AlumniPortalUser = request.user
        if not current_user.is_active:
            return Response("User is not active", status=status.HTTP_403_FORBIDDEN)
        if not current_user.isVerified:
            return Response("User is not verified", status=status.HTTP_403_FORBIDDEN)
        if not current_user.privilege == 'Super Admin':
            return Response("User is not super admin", status=status.HTTP_403_FORBIDDEN)
        clubId = kwargs['pk']
        club = Club.objects.filter(id=clubId).first()
        if not club:
            return Response("Club not found", status=status.HTTP_404_NOT_FOUND)
        admin = club.members.filter(
            user=current_user, isClubAdmin=True)
        if not admin:
            return Response("User is not club admin", status=status.HTTP_403_FORBIDDEN)
        club.isActive = False
        club.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        current_user: AlumniPortalUser = request.user
        if not current_user.is_active:
            return Response("User is not active", status=status.HTTP_403_FORBIDDEN)
        if not current_user.isVerified:
            return Response("User is not verified", status=status.HTTP_403_FORBIDDEN)
        if not current_user.privilege == 'Super Admin':
            return Response("User is not super admin", status=status.HTTP_403_FORBIDDEN)
        clubId = kwargs['pk']
        club = Club.objects.filter(id=clubId).first()
        if not club:
            return Response("Club not found", status=status.HTTP_404_NOT_FOUND)
        admin = club.members.filter(
            user=current_user, isClubAdmin=True)
        if not admin:
            return Response("User is not club admin", status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(club)
        serializer.update(club, request.data, partial=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class ClubMemberView(viewsets.ModelViewSet):
    serializer_class = ClubMemberSerializer
    queryset = ClubMember.objects.all()
    pagination_class = pagination.PageNumberPagination
    search_fields = ['user__firstName', 'user__lastName', 'user__email']
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    ordering_fields = ['user__firstName',
                       'user__lastName', '-createdAt', '-updatedAt']
    ordering = ['-createdAt']

    def list(self, request, *args, **kwargs):
        current_user: AlumniPortalUser = request.user
        if not current_user.is_active:
            return Response("User is not active", status=status.HTTP_403_FORBIDDEN)
        if not current_user.isVerified:
            return Response("User is not verified", status=status.HTTP_403_FORBIDDEN)
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.order_by('user__firstName', 'user__lastName')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            return response
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        current_user: AlumniPortalUser = request.user
        if not current_user.is_active:
            return Response("User is not active", status=status.HTTP_403_FORBIDDEN)
        if not current_user.isVerified:
            return Response("User is not verified", status=status.HTTP_403_FORBIDDEN)
        clubMemberId = kwargs['pk']
        clubMember = ClubMember.objects.filter(id=clubMemberId).first()
        if not clubMember:
            return Response("Club member not found", status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(clubMember)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        current_user: AlumniPortalUser = request.user
        if not current_user.is_active:
            return Response("User is not active", status=status.HTTP_403_FORBIDDEN)
        if not current_user.isVerified:
            return Response("User is not verified", status=status.HTTP_403_FORBIDDEN)
        if 'club' not in request.data:
            return Response("Club not provided", status=status.HTTP_400_BAD_REQUEST)
        if 'user' not in request.data:
            return Response("User not provided", status=status.HTTP_400_BAD_REQUEST)
        if 'position' not in request.data:
            return Response("Position not provided", status=status.HTTP_400_BAD_REQUEST)
        clubId = request.data['club']
        club = Club.objects.filter(id=clubId).first()
        if not club:
            return Response("Club not found", status=status.HTTP_404_NOT_FOUND)
        admin = club.members.filter(
            user=current_user, isClubAdmin=True)
        if not admin:
            return Response("User is not club admin", status=status.HTTP_403_FORBIDDEN)
        userId = request.data['user']
        user = AlumniPortalUser.objects.filter(id=userId).first()
        if not user:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        current_user: AlumniPortalUser = request.user
        if not current_user.is_active:
            return Response("User is not active", status=status.HTTP_403_FORBIDDEN)
        clubMemberId = kwargs['pk']
        clubMember = ClubMember.objects.filter(id=clubMemberId).first()
        if not clubMember:
            return Response("Club member not found", status=status.HTTP_404_NOT_FOUND)
        admin = clubMember.club.members.filter(
            user=current_user, isClubAdmin=True)
        if not admin:
            return Response("User is not club admin", status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(clubMember)
        serializer.update(clubMember, request.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        current_user: AlumniPortalUser = request.user
        if not current_user.is_active:
            return Response("User is not active", status=status.HTTP_403_FORBIDDEN)

        clubMemberId = kwargs['pk']
        clubMember = ClubMember.objects.filter(id=clubMemberId).first()
        if not clubMember:
            return Response("Club member not found", status=status.HTTP_404_NOT_FOUND)
        admin = clubMember.club.members.filter(
            user=current_user, isClubAdmin=True)
        if not admin:
            return Response("User is not club admin", status=status.HTTP_403_FORBIDDEN)
        clubMember.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        current_user: AlumniPortalUser = request.user
        if not current_user.is_active:
            return Response("User is not active", status=status.HTTP_403_FORBIDDEN)

        clubMemberId = kwargs['pk']
        clubMember = ClubMember.objects.filter(id=clubMemberId).first()
        if not clubMember:
            return Response("Club member not found", status=status.HTTP_404_NOT_FOUND)
        admin = clubMember.club.members.filter(
            user=current_user, isClubAdmin=True)
        if not admin:
            return Response("User is not club admin", status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(clubMember)
        serializer.update(clubMember, request.data, partial=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
