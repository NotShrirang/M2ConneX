from users.models import (
    AlumniPortalUser,
    Alumni,
    Student,
    Faculty,
    SuperAdmin
)
from users.serializers import (
    AlumniPortalUserSerializer,
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    AlumniSerializer,
    StudentSerializer,
    FacultySerializer,
    SuperAdminSerializer
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions
from django.db import transaction
from CODE.utils import emails


class AlumniPortalUserRegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        with transaction.atomic():
            user = request.data
            if "privilege" not in request.data:
                return Response({"error": "privilege is required"}, status=status.HTTP_400_BAD_REQUEST)
            privilege = request.data['privilege']
            if privilege in ["Alumni", "Student"]:
                if "batch" not in request.data:
                    return Response({"error": "batch is required"}, status=status.HTTP_400_BAD_REQUEST)
                if "enrollmentYear" not in request.data:
                    return Response({"error": "enrollmentYear is required"}, status=status.HTTP_400_BAD_REQUEST)
                if "passingOutYear" not in request.data:
                    return Response({"error": "passingOutYear is required"}, status=status.HTTP_400_BAD_REQUEST)
            elif privilege == "Staff":
                if "college" not in request.data:
                    return Response({"error": "college is required"}, status=status.HTTP_400_BAD_REQUEST)
            elif privilege == "Super Admin":
                pass
            else:
                return Response({"error": "invalid privilege"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.serializer_class(data=user)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            user = AlumniPortalUser.objects.get(email=user['email'])
            user_id = user.id
            user_data = AlumniPortalUserSerializer(user).data
            user_data['id'] = user_id
            if privilege == "Alumni":
                alumni_data = {
                    "user": user_id,
                    "batch": request.data['batch'],
                    "enrollmentYear": request.data['enrollmentYear'],
                    "passingOutYear": request.data['passingOutYear']
                }
                alumni_serializer = AlumniSerializer(data=alumni_data)
                if alumni_serializer.is_valid():
                    alumni_serializer.save()
                    user_data['Alumni'] = alumni_serializer.data
                    emails.send_welcome_email(name=user_data['firstName'], receiver=user_data['email'])
                    return Response(user_data, status=status.HTTP_201_CREATED)
                else:
                    return Response(alumni_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif privilege == "Student":
                student_data = {
                    "user": user_id,
                    "batch": request.data['batch'],
                    "enrollmentYear": request.data['enrollmentYear'],
                    "passingOutYear": request.data['passingOutYear']
                }
                student_serializer = StudentSerializer(data=student_data)
                if student_serializer.is_valid():
                    student_serializer.save()
                    user_data['Student'] = student_serializer.data
                    emails.send_welcome_email(name=user_data['firstName'], receiver=user_data['email'])
                    return Response(user_data, status=status.HTTP_201_CREATED)
                else:
                    return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif privilege == "Staff":
                faculty_data = {
                    "user": user_id,
                    "college": request.data['college']
                }
                faculty_serializer = FacultySerializer(data=faculty_data)
                if faculty_serializer.is_valid():
                    faculty_serializer.save()
                    user_data['Staff'] = faculty_serializer.data
                    emails.send_welcome_email(name=user_data['firstName'], receiver=user_data['email'])
                    return Response(user_data, status=status.HTTP_201_CREATED)
                else:
                    return Response(faculty_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif privilege == "Super Admin":
                superAdmin_data = {
                    "user": user_id
                }
                superAdmin_serializer = SuperAdminSerializer(data=superAdmin_data)
                if superAdmin_serializer.is_valid():
                    superAdmin_serializer.save()
                    user_data['Super Admin'] = superAdmin_serializer.data
                    emails.send_welcome_email(name=user_data['firstName'], receiver=user_data['email'])
                    return Response(user_data, status=status.HTTP_201_CREATED)
                else:
                    return Response(superAdmin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "invalid privilege"}, status=status.HTTP_400_BAD_REQUEST)


class AlumniPortalUserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlumniPortalUserLogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlumniPortalUserView(ModelViewSet):
    queryset = AlumniPortalUser.objects.all()
    serializer_class = AlumniPortalUserSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class AlumniView(ModelViewSet):
    queryset = Alumni.objects.all()
    serializer_class = AlumniSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class StudentView(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class FacultyView(ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class BloggerView(ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    search_fields = [
        'user__firstName',
        'user__lastName',
        'user__email',
    ]


class SuperAdminView(ModelViewSet):
    queryset = SuperAdmin.objects.all()
    serializer_class = SuperAdminSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
