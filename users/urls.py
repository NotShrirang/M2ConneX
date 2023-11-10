from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.views import APIView
from rest_framework.response import Response
from users.views import (
    AlumniPortalUserViewSet,
    AlumniPortalUserRegisterView,
    AlumniPortalUserLoginView,
    AlumniPortalUserLogoutView,
    AlumniViewSet,
    StudentViewSet,
    FacultyViewSet,
    SuperAdminViewSet
)
from rest_framework_simplejwt.views import (
    TokenRefreshView
)

router = SimpleRouter()
router.register(r'users', AlumniPortalUserViewSet, basename='users')
router.register(r'students', StudentViewSet, basename='students')
router.register(r'alumni', AlumniViewSet, basename='alumni')
router.register(r'faculty', FacultyViewSet, basename='faculty')
router.register(r'super-admin', SuperAdminViewSet, basename='super-admin')


class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to MMCOE Alumni Portal Users API',
            'endpoints': [
                '/login/',
                '/register/',
                '/logout/',
                '/token/refresh/',
                '/users/',
                '/students/',
                '/alumni/',
                '/faculty/',
                '/super-admin/'
            ]
        })

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('register/', AlumniPortalUserRegisterView.as_view(),name="register"),
    path('login/', AlumniPortalUserLoginView.as_view(),name="login"),
    path('logout/', AlumniPortalUserLogoutView.as_view(), name="logout"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls