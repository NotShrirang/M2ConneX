from rest_framework import views, viewsets, status
from rest_framework.response import Response
from django.utils import timezone

from .models import OTP
from .serializers import OTPSerializer

from users.models import AlumniPortalUser
from CODE.utils import emails, otps


class OTPView(viewsets.ModelViewSet):
    queryset = OTP.objects.all()
    serializer_class = OTPSerializer
    ordering = ('-createdAt')


class VerifyOTPView(views.APIView):
    def post(self, request, *args, **kwargs):
        if 'otp' not in request.data:
            return Response({"message": "OTP not provided"}, status=status.HTTP_400_BAD_REQUEST)
        if 'email' not in request.data:
            return Response({"message": "Email not provided"}, status=status.HTTP_400_BAD_REQUEST)
        otp = request.data.get('otp')
        email = request.data.get('email')
        user = AlumniPortalUser.objects.filter(email=email)
        if not user.exists():
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        qs = OTP.objects.filter(user=user, otp=otp)
        if qs.exists():
            otp_obj = qs.first()
            if otp_obj.isUsed:
                return Response({"message": "OTP already used. Click on resend OTP to get a new OTP."}, status=status.HTTP_400_BAD_REQUEST)
            expiry_time = otp_obj.updatedAt + timezone.timedelta(minutes=5)
            if expiry_time < timezone.now():
                return Response({"message": "OTP Expired"}, status.HTTP_400_BAD_REQUEST)
            otp_obj.isUsed = True
            otp_obj.save()
            user.isVerified = True
            user.is_active = True
            user.save()
            emails.send_welcome_email(
                name=user.firstName + " " + user.lastName, receiver=user.email)
            return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "OTP verification failed"}, status=status.HTTP_400_BAD_REQUEST)


class ResendOTPView(views.APIView):
    def post(self, request, *args, **kwargs):
        if 'email' not in request.data:
            return Response({"message": "Email not provided"}, status=status.HTTP_400_BAD_REQUEST)
        email = request.data.get('email')
        user = AlumniPortalUser.objects.filter(email=email)
        if not user.exists():
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        otp = OTP.objects.filter(user=user, isUsed=False)
        if otp.exists():
            otp = otp.first()
            otp.otp = otps.generate_otp()
            otp.save()
        else:
            otp = OTP.objects.create(
                otp=otps.generate_otp(), user=user, isUsed=False)
        emails.send_otp_email(
            name=user.firstName + " " + user.lastName, email=user.email, otp=otp.otp)
        return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
