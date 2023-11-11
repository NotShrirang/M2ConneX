from donation.views import DonationViewSet
from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.views import APIView
from rest_framework.response import Response


class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to MMCOE Alumni Portal Donation API',
            'endpoints': [
                '/donation/',
            ]
        })


router = SimpleRouter()
router.register('donation', DonationViewSet)

urlpatterns = [
    path('', HomeView.as_view()),
] + router.urls
