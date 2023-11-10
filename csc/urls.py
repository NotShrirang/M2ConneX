from csc.views import (
    CityViewSet,
    StateViewSet,
    CountryViewSet
)
from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.views import APIView
from rest_framework.response import Response

class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to MMCOE Alumni Portal CSC (City State Country) API',
            'endpoints': [
                '/city/',
                '/state/',
                '/country/',
            ]
        })

router = SimpleRouter()
router.register('city', CityViewSet)
router.register('state', StateViewSet)
router.register('country', CountryViewSet)

urlpatterns = [
    path('', HomeView.as_view()),
] + router.urls