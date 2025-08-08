from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from firebase_config import verify_firebase_token
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class FirebaseAuthenticationBackend(BaseBackend):
    """
    firebase authentication backend
    """
    
    def authenticate(self, request, firebase_token=None, **kwargs):
        """
        authenticate user using firebase ID token
        """
        if firebase_token is None:
            return None
            
        # verify firebase token
        decoded_token = verify_firebase_token(firebase_token)
        if not decoded_token:
            logger.warning("Failed to verify Firebase token")
            return None
            
        email = decoded_token.get('email')
        firebase_uid = decoded_token.get('uid')
        
        if not email or not firebase_uid:
            logger.warning("Email or UID missing from Firebase token")
            return None
            
        try:
            # get existing user by email
            user = User.objects.get(email=email)
            
            # update firebase UID if it's different or missing
            if user.identifier != firebase_uid:
                user.identifier = firebase_uid
                user.signInMethod = 'firebase'
                user.save(update_fields=['identifier', 'signInMethod'])
                logger.info(f"Updated Firebase UID for user: {email}")
                
            # check if user is active
            if not user.is_active:
                logger.warning(f"Inactive user attempted login: {email}")
                return None
                
            logger.info(f"Successfully authenticated user: {email}")
            return user
            
        except User.DoesNotExist:
            logger.warning(f"User does not exist: {email}")
            return None
    
    def get_user(self, user_id):
        """
        Get user by ID
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None