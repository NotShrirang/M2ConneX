from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from firebase_config import verify_firebase_token
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class FirebaseAuthentication(BaseAuthentication):
    """
    Firebase authentication for Django REST Framework
    Handles Bearer token authentication with Firebase ID tokens
    """
    
    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        auth_header = self.get_authorization_header(request)
        
        if not auth_header:
            return None
            
        try:
            # Extract token from header
            auth_parts = auth_header.split()
            
            if len(auth_parts) != 2 or auth_parts[0].lower() != b'bearer':
                return None
                
            id_token = auth_parts[1].decode('utf-8')
            
            # Verify Firebase token
            decoded_token = verify_firebase_token(id_token)
            if not decoded_token:
                raise AuthenticationFailed('Invalid or expired Firebase token')
                
            email = decoded_token.get('email')
            firebase_uid = decoded_token.get('uid')
            
            if not email:
                raise AuthenticationFailed('Email not found in Firebase token')
                
            # Get user from database
            try:
                user = User.objects.get(email=email)
                
                # Update Firebase UID if needed
                if user.identifier != firebase_uid:
                    user.identifier = firebase_uid
                    user.signInMethod = 'firebase'
                    user.save(update_fields=['identifier', 'signInMethod'])
                    
                if not user.is_active:
                    raise AuthenticationFailed('User account is disabled')
                    
                if not user.isVerified:
                    raise AuthenticationFailed('User account is not verified')
                    
                logger.debug(f"Authenticated user: {email}")
                return (user, id_token)
                
            except User.DoesNotExist:
                raise AuthenticationFailed('User not found. Please register first.')
                
        except AuthenticationFailed:
            raise
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            raise AuthenticationFailed('Authentication failed')
    
    def get_authorization_header(self, request):
        """
        Get authorization header from request
        """
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        if isinstance(auth, str):
            auth = auth.encode('iso-8859-1')
        return auth
    
    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response.
        """
        return 'Bearer realm="api"'