from users.models import (
    AlumniPortalUser,
    Alumni,
    Student,
    Faculty,
    SuperAdmin
)
from django.contrib import auth
from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField, Serializer, ValidationError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.password_validation import validate_password
import requests

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
    
class RegisterGoogleSerializer(ModelSerializer):
    token = CharField(required=True)

    class Meta:
        model = AlumniPortalUser
        fields = (
            'token',
        )

    def validate(self, data):
        """
        Check if the user exists.
        """
        url = f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={data['token']}"
        response = requests.get(url)
        if (response.status_code == 200):
            response_body = response.json()
            email = response_body["email"]
            user = AlumniPortalUser.objects.filter(email=email)
            if user.exists():
                raise ValidationError(f"User with email {email} already exists")
            data['email'] = email
            return data
        raise ValidationError('invalid token')

    def create(self, validated_data):
        validated_data['is_active'] = True
        validated_data['signInMethod'] = "Google"
        validated_data['isVerified'] = False
        validated_data['privilege'] = "3"
        del validated_data['token']
        user = AlumniPortalUser.objects.create(**validated_data)
        user.save()
        return user
    
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

class GoogleLoginSerializer(ModelSerializer):
    accessToken = CharField(write_only=True, required=True)

    class Meta:
        model = AlumniPortalUser
        fields = (
            'accessToken',
        )

    def validate(self, data):
        """
        Check if the user exists.
        """
        url = f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={data['accessToken']}"
        response = requests.get(url)
        if (response.status_code == 200):
            response_body = response.json()
            email = response_body["email"]
            user = AlumniPortalUser.objects.filter(email=email)
            if not user.exists():
                raise ValidationError(f"User with email {email} does not exist")
            if not user.first().is_active:
                raise ValidationError(f"User with email {email} is inactive")
            token = RefreshToken.for_user(user.first())
            data = dict()
            data['refresh'] = str(token)
            data['access'] = str(token.access_token)
            return data
        else:
            raise ValidationError('invalid token')

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

class AlumniSerializer(ModelSerializer):
    class Meta:
        model = Alumni
        fields = ['id', 'user', 'batch', 'enrollmentYear', 'passingOutYear']

class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user', 'batch', 'enrollmentYear', 'passingOutYear']

class FacultySerializer(ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'user', 'college']

class SuperAdminSerializer(ModelSerializer):
    class Meta:
        model = SuperAdmin
        fields = ['id', 'user']

class UpdatePasswordSerializer(ModelSerializer):
    password = CharField(write_only=True, required=True, validators=[validate_password])
    confirmPassword = CharField(write_only=True, required=True)
    oldPassword = CharField(write_only=True, required=True)

    class Meta:
        model = AlumniPortalUser
        fields = ('oldPassword', 'password', 'confirmPassword')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmPassword']:
            raise ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate_oldPassword(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise ValidationError({"oldPassword": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.pk != instance.pk:
            raise ValidationError({"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()
        return instance