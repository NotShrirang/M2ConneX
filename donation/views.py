from donation.models import Donation
from donation.serializers import DonationSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class DonationView(ModelViewSet):
    serializer_class = DonationSerializer
    queryset = Donation.objects.all()
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
            return super().list(request, *args, **kwargs)
        else:
            return Response({"error": "Your account is not active. Please contact admin"}, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_active:
            if current_user.privilege == '3':
                return super().create(request, *args, **kwargs)
            else:
                return Response({"error": "We appreciate your efforts, but sadly we can't donation from you."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error": "We would really like your donation. Please contact the college office for further procedure."}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        return Response({"error": "Why change now? Ek baar ho gaya to ho gaya."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response({"error": "Why change now? Ek baar ho gaya to ho gaya."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response({"error": "Bade harami ho. But ab nahi hoga delete."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

