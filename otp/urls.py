from django.urls import path
from .views import OTPView, VerifyOTPView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('', OTPView, basename='otp')

urlpatterns = [
    path('verify-otp/', VerifyOTPView.as_view())
]

urlpatterns += router.urls
