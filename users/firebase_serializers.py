from rest_framework.serializers import Serializer, CharField, ValidationError, ModelSerializer, SerializerMethodField
from rest_framework.exceptions import AuthenticationFailed
from firebase_config import verify_firebase_token
from users.models import AlumniPortalUser, Alumni, Student, Faculty, SuperAdmin
from users.serializers import AlumniPortalUserSerializer
import logging

logger = logging.getLogger(__name__)

class FirebaseLoginSerializer(Serializer):
    """
    Serializer for Firebase login
    Accepts Firebase ID token and returns user data
    """
    idToken = CharField(required=True, write_only=True)
    user = SerializerMethodField(read_only=True)
    
    def get_user(self, validated_data):
        """Return full user data"""
        if 'user_instance' in validated_data:
            return AlumniPortalUserSerializer(validated_data['user_instance'], context=self.context).data
        return None
    
    def validate_idToken(self, value):
        """
        Validate Firebase ID token and return decoded data
        """
        decoded_token = verify_firebase_token(value)
        if not decoded_token:
            raise ValidationError('Invalid or expired Firebase token')
        return decoded_token
    
    def validate(self, attrs):
        """
        Authenticate user with Firebase token
        """
        decoded_token = attrs['idToken']
        email = decoded_token.get('email')
        firebase_uid = decoded_token.get('uid')
        
        if not email:
            raise ValidationError('Email not found in Firebase token')
            
        try:
            # Get existing user
            user = AlumniPortalUser.objects.get(email=email)
            
            # Update Firebase UID if needed
            if user.identifier != firebase_uid:
                user.identifier = firebase_uid
                user.signInMethod = 'firebase'
                user.save(update_fields=['identifier', 'signInMethod'])
                
            if not user.is_active:
                raise AuthenticationFailed('Account is disabled')
                
            if not user.isVerified:
                raise AuthenticationFailed('Account is not verified')
                
            # Store user instance for get_user method
            attrs['user_instance'] = user
            return attrs
            
        except AlumniPortalUser.DoesNotExist:
            raise ValidationError('User not found. Please register first.')

class FirebaseRegisterSerializer(Serializer):
    """
    Serializer for Firebase registration
    Creates new user account with Firebase authentication
    """
    idToken = CharField(required=True, write_only=True)
    privilege = CharField(required=True)
    department = CharField(required=False, allow_blank=True)
    city = CharField(required=False, allow_blank=True)
    phoneNumber = CharField(required=False, allow_blank=True)
    bio = CharField(required=False, allow_blank=True)
    
    # Role-specific fields
    batch = CharField(required=False, allow_blank=True)
    enrollmentYear = CharField(required=False, allow_blank=True)
    passingOutYear = CharField(required=False, allow_blank=True)
    college = CharField(required=False, allow_blank=True)
    
    user = SerializerMethodField(read_only=True)
    
    def get_user(self, validated_data):
        """Return created user data"""
        if 'user_instance' in validated_data:
            return AlumniPortalUserSerializer(validated_data['user_instance'], context=self.context).data
        return None
    
    def validate_idToken(self, value):
        """
        Validate Firebase ID token
        """
        decoded_token = verify_firebase_token(value)
        if not decoded_token:
            raise ValidationError('Invalid or expired Firebase token')
        return decoded_token
    
    def validate_privilege(self, value):
        """
        Validate privilege choice
        """
        valid_privileges = ['Alumni', 'Student', 'Staff', 'Super Admin']
        if value not in valid_privileges:
            raise ValidationError(f'Invalid privilege. Must be one of: {valid_privileges}')
        return value
    
    def validate(self, attrs):
        """
        Validate registration data
        """
        decoded_token = attrs['idToken']
        email = decoded_token.get('email')
        firebase_uid = decoded_token.get('uid')
        
        if not email:
            raise ValidationError('Email not found in Firebase token')
            
        # Check if user already exists
        if AlumniPortalUser.objects.filter(email=email).exists():
            raise ValidationError(f'User with email {email} already exists')
            
        # Extract user data from Firebase token
        name = decoded_token.get('name', '') or decoded_token.get('email', '').split('@')[0]
        name_parts = name.split(' ', 1) if name else ['User', '']
        
        attrs.update({
            'email': email,
            'firebase_uid': firebase_uid,
            'firstName': name_parts[0] or 'User',
            'lastName': name_parts[1] if len(name_parts) > 1 else '',
            'profilePicture': decoded_token.get('picture', ''),
            'isVerified': True,  # Auto-verify Firebase users since Firebase handles auth
        })
        
        return attrs
    
    def save(self):
        """
        Create new user with Firebase authentication
        """
        from django.db import transaction
        from csc.models import City
        
        validated_data = self.validated_data
        
        # Extract Firebase data
        firebase_uid = validated_data['firebase_uid']
        privilege = validated_data['privilege']
        
        # Extract role-specific data
        batch = validated_data.get('batch', '')
        enrollment_year = validated_data.get('enrollmentYear', '')
        passing_out_year = validated_data.get('passingOutYear', '')
        college = validated_data.get('college', '')
        
        # Handle city
        city_name = validated_data.get('city', '')
        city_instance = None
        if city_name:
            try:
                city_instance = City.objects.filter(name__icontains=city_name).first()
            except Exception:
                pass
        
        with transaction.atomic():
            # Create user
            user_data = {
                'email': validated_data['email'],
                'firstName': validated_data['firstName'],
                'lastName': validated_data['lastName'],
                'profilePicture': validated_data['profilePicture'],
                'isVerified': validated_data['isVerified'],
                'identifier': firebase_uid,
                'signInMethod': 'firebase',
                'is_active': True,
                'privilege': privilege,
                'department': validated_data.get('department', ''),
                'bio': validated_data.get('bio', ''),
                'phoneNumber': validated_data.get('phoneNumber', ''),
                'city': city_instance
            }
            
            # Create user without password (Firebase handles authentication)
            user = AlumniPortalUser(**user_data)
            user.set_unusable_password()  # Mark password as unusable
            user.save()
            
            # Create role-specific record
            if privilege == 'Alumni':
                Alumni.objects.create(
                    user=user,
                    batch=int(batch) if batch and batch.isdigit() else 2024,
                    enrollmentYear=enrollment_year or '2020-01-01',
                    passingOutYear=passing_out_year or '2024-01-01'
                )
            elif privilege == 'Student':
                Student.objects.create(
                    user=user,
                    batch=int(batch) if batch and batch.isdigit() else 2025,
                    enrollmentYear=enrollment_year or '2021-01-01',
                    passingOutYear=passing_out_year or '2025-01-01'
                )
            elif privilege == 'Staff':
                Faculty.objects.create(
                    user=user,
                    college=college or 'MMCOE'
                )
            elif privilege == 'Super Admin':
                SuperAdmin.objects.create(user=user)
                user.is_staff = True
                user.is_superuser = True
                user.save(update_fields=['is_staff', 'is_superuser'])
            
            logger.info(f"Created new user: {user.email} with privilege: {privilege}")
            
            # Store user instance for get_user method
            self.validated_data['user_instance'] = user
            return user


class FirebaseLogoutSerializer(Serializer):
    """
    Serializer for Firebase logout
    """
    revoke_tokens = CharField(required=False, default='false')
    
    def validate(self, attrs):
        """
        Handle logout logic
        """
        user = self.context['request'].user
        
        if attrs.get('revoke_tokens', 'false').lower() == 'true':
            # Revoke all refresh tokens for this user
            from firebase_config import revoke_firebase_tokens
            if user.identifier:  # Firebase UID
                revoke_firebase_tokens(user.identifier)
                
        return attrs