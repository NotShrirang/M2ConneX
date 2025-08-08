import os
import json
import logging
import firebase_admin
from firebase_admin import credentials, auth

logger = logging.getLogger(__name__)

def initialize_firebase():
    """
    Initialize Firebase Admin SDK with multiple configuration methods
    """
    if firebase_admin._apps:
        logger.info("Firebase already initialized")
        return firebase_admin
    
    try:
        cred = None
        
        # Method 1: Using service account JSON file (recommended for production)
        service_account_path = 'firebase-service-account.json'
        if os.path.exists(service_account_path):
            logger.info("Initializing Firebase with service account file")
            cred = credentials.Certificate(service_account_path)
        
        # Method 2: Using environment variable with full JSON
        elif os.getenv('FIREBASE_CREDENTIALS_JSON'):
            logger.info("Initializing Firebase with JSON from environment")
            firebase_creds = json.loads(os.getenv('FIREBASE_CREDENTIALS_JSON'))
            cred = credentials.Certificate(firebase_creds)
        
        # Method 3: Using individual environment variables
        elif all([
            os.getenv('FIREBASE_PROJECT_ID'),
            os.getenv('FIREBASE_PRIVATE_KEY'),
            os.getenv('FIREBASE_CLIENT_EMAIL')
        ]):
            logger.info("Initializing Firebase with individual environment variables")
            cred_dict = {
                "type": "service_account",
                "project_id": os.getenv('FIREBASE_PROJECT_ID'),
                "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID', ''),
                "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
                "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
                "client_id": os.getenv('FIREBASE_CLIENT_ID', ''),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{os.getenv('FIREBASE_CLIENT_EMAIL')}"
            }
            cred = credentials.Certificate(cred_dict)
        
        # Method 4: Application Default Credentials (for Google Cloud)
        else:
            logger.info("Attempting to use Application Default Credentials")
            cred = credentials.ApplicationDefault()
        
        if cred:
            firebase_admin.initialize_app(cred)
            logger.info("Firebase Admin SDK initialized successfully")
        else:
            raise ValueError("No valid Firebase credentials found")
            
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {str(e)}")
        raise Exception(f"Firebase initialization failed: {str(e)}")
    
    return firebase_admin

def verify_firebase_token(id_token):
    """
    Verify Firebase ID token and return decoded token data
    """
    try:
        initialize_firebase()
        decoded_token = auth.verify_id_token(id_token)
        logger.debug(f"Token verified for user: {decoded_token.get('email')}")
        return decoded_token
    except auth.InvalidIdTokenError as e:
        logger.warning(f"Invalid Firebase token: {str(e)}")
        return None
    except auth.ExpiredIdTokenError as e:
        logger.warning(f"Expired Firebase token: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        return None

def revoke_firebase_tokens(firebase_uid):
    """
    Revoke all refresh tokens for a user (logout)
    """
    try:
        initialize_firebase()
        auth.revoke_refresh_tokens(firebase_uid)
        logger.info(f"Tokens revoked for user: {firebase_uid}")
        return True
    except Exception as e:
        logger.error(f"Failed to revoke tokens: {str(e)}")
        return False