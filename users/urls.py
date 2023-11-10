from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.views import APIView
from rest_framework.response import Response
from users.views import (
    AlumniPortalUserViewSet,
    AlumniPortalUserRegisterView,
    AlumniPortalUserLoginView,
    AlumniPortalUserLogoutView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView
)

router = SimpleRouter()
router.register(r'users', AlumniPortalUserViewSet, basename='users')

class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to MMCOE Alumni Portal Users API',
            'endpoints': [
                '/login/',
                '/register/',
                '/logout/',
                '/users/',
            ]
        })

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('register/', AlumniPortalUserRegisterView.as_view(),name="register"),
    path('login/', AlumniPortalUserLoginView.as_view(),name="login"),
    path('logout/', AlumniPortalUserLogoutView.as_view(), name="logout"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls