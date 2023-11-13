from django.contrib import admin
from django.urls import path, include
from rest_framework.views import APIView
from rest_framework.response import Response

class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to MMCOE Alumni Portal Main API',
            'endpoints': [
                '/users/',
                '/skill/',
                '/opportunity/',
                '/feed/',
                '/event/',
                '/experience/',
                '/donation/',
                '/csc/',
                '/connection/',
            ]
        })

urlpatterns = [
    path("", HomeView.as_view()),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("skill/", include("skill.urls")),
    path("opportunity/", include("opportunity.urls")),
    path("feed/", include("feed.urls")),
    path("event/", include("event.urls")),
    path("experience/", include("experience.urls")),
    path("donation/", include("donation.urls")),
    path("csc/", include("csc.urls")),
    path("connection/", include("connection.urls")),
]
