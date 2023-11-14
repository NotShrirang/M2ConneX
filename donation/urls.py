from donation.views import DonationView
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
router.register('donation', DonationView, basename='donation')

urlpatterns = [
    path('', HomeView.as_view()),
] + router.urls
