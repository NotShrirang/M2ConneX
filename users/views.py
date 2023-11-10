from users.models import AlumniPortalUser
from users.serializers import AlumniPortalUserSerializer, RegisterSerializer, LoginSerializer, LogoutSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions

class AlumniPortalUserRegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self,request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_id = AlumniPortalUser.objects.get(email=user['email']).id
        user_data = serializer.data
        user_data['id'] = user_id
        return Response(user_data, status=status.HTTP_201_CREATED)

class AlumniPortalUserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class AlumniPortalUserLogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AlumniPortalUserViewSet(ModelViewSet):
    queryset = AlumniPortalUser.objects.all()
    serializer_class = AlumniPortalUserSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)