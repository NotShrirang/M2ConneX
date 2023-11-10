from users.models import AlumniPortalUser
from django.contrib import auth
from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField, Serializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class AlumniPortalUserSerializer(ModelSerializer):
    class Meta:
        model = AlumniPortalUser
        fields = ['id', 'email', 'firstName', 'lastName', 'department', 'privilege', 'resume', 'profilePicture', 'city', 'phoneNumber', 'createdAt', 'updatedAt', 'is_active', 'is_admin', 'is_staff', 'is_superuser']

class RegisterSerializer(ModelSerializer):
    password = CharField(min_length=8, write_only=True)

    class Meta:
        model = AlumniPortalUser
        fields = ['email', 'password', 'firstName', 'lastName', 'department', 'privilege', 'city']

    def create(self, validated_data):
        return AlumniPortalUser.objects.create_user(**validated_data)
    
class LoginSerializer(ModelSerializer):
    password = CharField(min_length=6, write_only=True)
    username = CharField(max_length=255, min_length=3)
    tokens = SerializerMethodField()

    def get_tokens(self, obj):
        user = AlumniPortalUser.objects.get(email=obj['email'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
    
    class Meta:
        model = AlumniPortalUser
        fields = ['email', 'password','tokens']

    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')
        user = auth.authenticate(email=email,password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        return {
            'email': user.email,
            'tokens': user.tokens
        }

class LogoutSerializer(Serializer):
    refresh = CharField()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')