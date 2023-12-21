from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.views import APIView
from rest_framework.response import Response
from users.views import (
    AlumniPortalUserView,
    AlumniPortalUserRegisterView,
    AlumniPortalUserLoginView,
    AlumniPortalUserLogoutView,
    EmailExistanceCheckerView,
    AlumniView,
    StudentView,
    FacultyView,
    SuperAdminView,
    BloggerView
)
from rest_framework_simplejwt.views import (
    TokenRefreshView
)


class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to MMCOE Alumni Portal Users API',
            'endpoints': [
                '/login/',
                '/register/',
                '/logout/',
                '/check-email/',
                '/token/refresh/',
                '/users/',
                '/students/',
                '/alumni/',
                '/faculty/',
                '/super-admin/'
            ]
        })


router = SimpleRouter()
router.register(r'users', AlumniPortalUserView, basename='users')
router.register(r'alumni', AlumniView, basename='alumni')
router.register(r'students', StudentView, basename='students')
router.register(r'faculty', FacultyView, basename='faculty')
router.register(r'super-admin', SuperAdminView, basename='super-admin')
router.register(r'blogger', BloggerView, basename='blogger')

urlpatterns = [
    path('', HomeView.as_view(), name="homeview"),
    path('register/', AlumniPortalUserRegisterView.as_view(), name="register"),
    path('login/', AlumniPortalUserLoginView.as_view(), name="login"),
    path('logout/', AlumniPortalUserLogoutView.as_view(), name="logout"),
    path('/check-email/', EmailExistanceCheckerView.as_view(), name='check-email'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
