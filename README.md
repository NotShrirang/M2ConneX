# M2ConneX - AI-Powered Alumni Portal with Firebase SSO

![GitHub stars](https://img.shields.io/github/stars/NotShrirang/M2ConneX?style=social)
![GitHub forks](https://img.shields.io/github/forks/NotShrirang/M2ConneX?style=social)
![GitHub issues](https://img.shields.io/github/issues/NotShrirang/M2ConneX)
![GitHub pull requests](https://img.shields.io/github/issues-pr/NotShrirang/M2ConneX)
![GitHub](https://img.shields.io/github/license/NotShrirang/M2ConneX)
![GitHub last commit](https://img.shields.io/github/last-commit/NotShrirang/M2ConneX)
![GitHub repo size](https://img.shields.io/github/repo-size/NotShrirang/M2ConneX)

[![DB Diagram](https://img.shields.io/badge/DB%20Diagram-blue?style=for-the-badge&logo=sqlite&logoColor=white&logoSize=amd)](https://dbdiagram.io/d/MMCOE-Alumni-Portal-654ce8d57d8bbd6465dac5ae)

## Overview

M2ConneX is a comprehensive AI-powered platform designed to connect alumni of MMCOE (Marathwada Mitra Mandal's College of Engineering) and facilitate intelligent networking, collaboration, and content discovery. The platform features advanced machine learning-based recommendation systems, **secure Firebase SSO authentication**, and seamless user experience.

**🔐 Authentication Features:**
- **Firebase Single Sign-On (SSO)** - Secure, Google-grade authentication
- **Dual Authentication Support** - Both Firebase and legacy JWT authentication
- **Zero Downtime Migration** - Seamless transition from JWT to Firebase
- **Auto-Verification** - Firebase users are automatically verified
- **No Password Storage** - Enhanced security with Firebase handling all authentication

**🤖 AI-Powered Features:**
- **Semantic Content Recommendations**: Uses FAISS + Sentence Transformers for intelligent feed curation
- **Smart User Matching**: ML-based connection recommendations using profile similarity
- **Personalized Job Suggestions**: Skills-based opportunity matching with semantic understanding
- **Content Feed Rotation**: Prevents repetitive content using Redis-backed tracking
- **Real-time NSFW Detection**: Hugging Face API integration for content moderation

This is the backend API developed for the platform.
#### Frontend - https://github.com/NotShrirang/M2ConneX-frontend

## Features

- **🔥 Firebase SSO Authentication**: Secure, seamless login with Google-grade security
- **🎯 AI-Powered Recommendations**: Personalized content using FAISS vector similarity search
- **🔍 Semantic Search**: Advanced embedding-based content discovery
- **👥 Smart Networking**: ML-driven connection suggestions based on profile similarity
- **📱 Social Media**: Post and share updates with intelligent content curation
- **🏢 Job Opportunities**: AI-matched career opportunities with skills analysis
- **📅 Event Management**: Smart event recommendations and management
- **💼 Professional Profiles**: Rich profiles with skills, experience, and achievements
- **🎓 Alumni Directory**: Searchable directory with intelligent filtering
- **🏆 Skill Sharing**: Expertise matching and mentorship opportunities
- **🤝 Community Engagement**: Interest-based groups and discussions

## Architecture

### Authentication System
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Frontend      │    │   Django API     │    │   Firebase Admin    │
│                 │    │                  │    │                     │
│ Firebase SDK    │───▶│ Firebase Auth    │───▶│ Token Verification  │
│ ID Token        │    │ Middleware       │    │ User Management     │
│                 │    │                  │    │                     │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   PostgreSQL     │
                       │                  │
                       │ User Profiles    │
                       │ App Data         │
                       │ NO Passwords     │
                       └──────────────────┘
```

### AI/ML Technology Stack

- **FAISS**: Vector similarity search for real-time recommendations
- **Sentence Transformers**: Semantic embedding generation (`all-MiniLM-L6-v2`)
- **Hugging Face Transformers**: Pre-trained language models
- **Redis**: Caching and feed rotation management
- **PyTorch**: Deep learning framework
- **scikit-learn**: Traditional ML algorithms
- **NumPy**: Numerical computing
- **Firebase Admin SDK**: Server-side authentication and user management

## Getting Started

### Prerequisites

- Docker Desktop
- 8GB+ RAM (recommended for ML models)
- **Firebase Project** with Authentication enabled
- Python 3.9+ (for local development)

### Firebase Setup

1. **Create Firebase Project**:
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create new project or select existing
   - Enable **Authentication** service
   - Enable **Email/Password** provider in Sign-in methods

2. **Get Service Account**:
   - Go to **Project Settings** → **Service Accounts**
   - Click **"Generate new private key"**
   - Download JSON file as `firebase-service-account.json`
   - Place in project root directory

3. **Get Web API Key**:
   - Go to **Project Settings** → **General**
   - Copy the **Web API Key** for frontend integration

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/NotShrirang/M2ConneX.git
cd M2ConneX
```

2. **Environment Configuration:**

Create a `.env` file in the root directory:
```env
# Database Configuration
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres
DB_HOST=alumni-portal-db
DB_PORT=5432

# Email Configuration (Optional - for legacy features)
EMAIL=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# AI/ML Configuration
TEXT_NSFW_TOKEN=your_huggingface_token_here
TRANSFORMERS_CACHE=/tmp/transformers_cache
HF_HOME=/tmp/huggingface
TORCH_HOME=/tmp/torch
TOKENIZERS_PARALLELISM=false

# Firebase Configuration (automatically detected from service account file)
# Place firebase-service-account.json in project root

# Optional: Hugging Face API Token for enhanced features
HUGGINGFACE_API_TOKEN=your_hf_api_token
```

3. **Place Firebase Credentials:**
```bash
# Your project structure should look like:
├── firebase-service-account.json  ← Your Firebase credentials
├── docker-compose-dev.yml
├── manage.py
└── ... other files
```

### Quick Start with Docker

#### 1. Start the Application
```bash
# Windows
./run.bat start-dev

# Linux/Mac
./run.sh start-dev
```

#### 2. Set Up the Database
```bash
# Run migrations
docker exec -it alumni-portal-backend python manage.py migrate

# Create sample data (optional but recommended)
docker exec -it alumni-portal-backend python manage.py populate_db --users 50 --posts 100 --opportunities 30
```

#### 3. Verify Firebase Integration
```bash
# Test Firebase initialization
docker exec -it alumni-portal-backend python -c "
from firebase_config import initialize_firebase
initialize_firebase()
print('✅ Firebase is ready!')
"
```

#### 4. Build AI Recommendation Index
```bash
# Build FAISS index for personalized recommendations
docker exec -it alumni-portal-backend python manage.py build_faiss_index --rebuild
```

## Authentication System

### Firebase SSO Endpoints

#### Register New User
```bash
POST /users/firebase/register/
Content-Type: application/json

{
  "idToken": "firebase-id-token-from-frontend",
  "privilege": "Alumni|Student|Staff|Super Admin",
  "department": "1",
  "batch": "2024",
  "enrollmentYear": "2020-01-01", 
  "passingOutYear": "2024-01-01",
  "city": "Pune",
  "phoneNumber": "+919876543210",
  "bio": "Software Engineer"
}
```

#### Login User
```bash
POST /users/firebase/login/
Content-Type: application/json

{
  "idToken": "firebase-id-token-from-frontend"
}
```

#### Access Protected Endpoints
```bash
GET /users/
Authorization: Bearer firebase-id-token
```

### Legacy JWT Endpoints (Still Supported)

```bash
# Legacy authentication (backwards compatible)
POST /users/login/
POST /users/register/
POST /users/logout/
POST /users/token/refresh/
```

### Frontend Integration

#### Firebase SDK Setup (Frontend)
```javascript
// Install: npm install firebase
import { initializeApp } from 'firebase/app';
import { getAuth, signInWithEmailAndPassword } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "your-web-api-key",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id"
  // ... other config
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
```

#### Authentication Flow (Frontend)
```javascript
// Login
const login = async (email, password) => {
  const result = await signInWithEmailAndPassword(auth, email, password);
  const idToken = await result.user.getIdToken();
  
  // Send to your Django backend
  const response = await fetch('/users/firebase/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ idToken })
  });
};

// API calls with automatic token
const makeAuthenticatedRequest = async (url, options = {}) => {
  const user = auth.currentUser;
  const idToken = await user.getIdToken();
  
  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${idToken}`
    }
  });
};
```

## API Endpoints

### Authentication
```bash
# Firebase Authentication (Recommended)
POST /users/firebase/login/
POST /users/firebase/register/  
POST /users/firebase/logout/

# Legacy JWT Authentication (Backwards Compatible)
POST /users/login/
POST /users/register/
POST /users/logout/
```

### AI-Powered Endpoints
```bash
# Personalized feed recommendations
GET /feed/recommend-feed/
Authorization: Bearer <firebase-token>

# Smart user connections
GET /connection/recommend-connection/
Authorization: Bearer <firebase-token>

# Skill-based job matching
GET /opportunity/recommend-opportunity/?search=python
Authorization: Bearer <firebase-token>
```

### Core Endpoints
- **Users**: `/users/` - User management and profiles
- **Feed**: `/feed/` - Social media posts with AI curation
- **Connections**: `/connection/` - Smart networking
- **Opportunities**: `/opportunity/` - AI-matched job postings
- **Events**: `/event/` - Event management
- **Skills**: `/skill/` - Skills and expertise tracking
- **Analytics**: `/analytics/` - User engagement insights

## Access Points

- **Main API**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/ (admin@mmcoe.edu.in / admin123)
- **API Documentation**: http://localhost:8000/swagger/
- **Database Admin**: http://localhost:5050/ (admin@admin.com / root)
- **Message Queue**: http://localhost:15672/ (admin / admin)
- **Task Monitor**: http://localhost:5555/

## Authentication Migration Guide

### For Existing Applications

Your existing JWT-based applications continue to work without any changes. The system now supports **dual authentication**:

**Option 1: Keep using JWT (No changes needed)**
```javascript
// Existing JWT flow continues to work
fetch('/users/login/', {
  method: 'POST',
  body: JSON.stringify({ email, password })
});
```

**Option 2: Migrate to Firebase SSO (Recommended)**
```javascript
// New Firebase flow - more secure and user-friendly
import { signInWithEmailAndPassword } from 'firebase/auth';

const result = await signInWithEmailAndPassword(auth, email, password);
const idToken = await result.user.getIdToken();

fetch('/users/firebase/login/', {
  method: 'POST',
  body: JSON.stringify({ idToken })
});
```

### Migration Benefits

- **Enhanced Security**: Google-grade authentication infrastructure
- **Better UX**: Seamless login experience
- **No Password Storage**: Eliminates password-related security risks
- **Automatic Verification**: Users are verified by default
- **Scalable**: Firebase handles authentication infrastructure
- **Modern**: Industry-standard OAuth 2.0 / OpenID Connect

## Performance Optimization

### ML Model Optimization
```bash
# For memory-constrained environments, use lighter models
# Edit CODE/utils/recommendations.py and change:
# 'all-MiniLM-L6-v2' -> 'paraphrase-MiniLM-L3-v2'
```

### Cache Configuration
```bash
# Optimize Redis for better performance
docker exec -it alumni-portal-redis redis-cli CONFIG SET maxmemory 512mb
docker exec -it alumni-portal-redis redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

### FAISS Index Management
```bash
# Save index manually
docker exec -it alumni-portal-backend python -c "
from CODE.utils.recommendations import get_recommendation_engine
engine = get_recommendation_engine()
engine.save_index()
print('Index saved!')
"

# Check index size
docker exec -it alumni-portal-backend ls -lh /tmp/user_embeddings.index*
```

## Troubleshooting

### Common Issues

1. **Firebase initialization failed**:
```bash
# Check service account file exists
docker exec -it alumni-portal-backend ls -la firebase-service-account.json

# Verify Firebase credentials
docker logs alumni-portal-backend | grep -i firebase
```

2. **"Invalid Firebase token" errors**:
```bash
# Tokens expire after 1 hour - get fresh token
# Check Firebase project configuration matches
# Ensure Email/Password provider is enabled in Firebase Console
```

3. **Cache Permission Errors**:
```bash
docker exec -it alumni-portal-backend bash -c "
mkdir -p /tmp/transformers_cache /tmp/huggingface /tmp/torch
chmod 777 /tmp/transformers_cache /tmp/huggingface /tmp/torch
"
```

4. **Memory Issues with ML Models**:
```bash
# Restart containers to free memory
docker-compose -p alumni-portal-dev -f docker-compose-dev.yml restart backend
```

### Firebase Debugging

```bash
# Test Firebase token validation
curl -X POST http://localhost:8000/users/firebase/login/ \
  -H "Content-Type: application/json" \
  -d '{"idToken": "your-firebase-id-token"}'

# Check Firebase service in containers
docker exec -it alumni-portal-backend python -c "
import firebase_admin
print('Firebase apps:', len(firebase_admin._apps))
"
```

## Security Features

### Firebase SSO Security Benefits

- **Google-Grade Security**: Authentication handled by Google's infrastructure
- **No Password Storage**: Eliminates password-related vulnerabilities
- **Automatic Token Refresh**: Secure session management
- **Audit Logging**: Firebase provides comprehensive authentication logs
- **Rate Limiting**: Built-in protection against brute force attacks
- **Multi-Factor Authentication**: Easy to enable additional security layers

### Data Protection

- **JWT + Firebase Support**: Dual authentication for maximum compatibility
- **Token Validation**: All requests verified against Firebase servers
- **User Verification**: Automatic email verification through Firebase
- **Session Security**: Stateless authentication with secure token management

## Docker Services

- **backend**: Django API server with ML capabilities and Firebase authentication
- **db**: PostgreSQL database (no password storage for Firebase users)
- **redis**: Caching and session management
- **rabbit-mq**: Celery task queue
- **celery**: Background task processing
- **flower**: Task monitoring
- **pgadmin**: Database administration

## Development

### Adding New Firebase Features

1. **Custom Claims Integration**:
```python
# Add custom claims to Firebase tokens
from firebase_admin import auth

def set_custom_claims(firebase_uid, claims):
    auth.set_custom_user_claims(firebase_uid, claims)
```

2. **Advanced User Management**:
```python
# Firebase Admin operations
from firebase_admin import auth

def disable_user(firebase_uid):
    auth.update_user(firebase_uid, disabled=True)
```

### Testing Firebase Authentication

```bash
# Create test Firebase user
curl -X POST "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=YOUR_WEB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123", "returnSecureToken": true}'

# Test registration
curl -X POST http://localhost:8000/users/firebase/register/ \
  -H "Content-Type: application/json" \
  -d '{"idToken": "firebase-token", "privilege": "Alumni", "department": "1"}'
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/firebase-enhancement`
3. Commit changes: `git commit -am 'Add Firebase feature'`
4. Push to branch: `git push origin feature/firebase-enhancement`
5. Submit a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review API documentation at `/swagger/`
- Firebase Console for authentication issues

## Acknowledgments

- **Google Firebase** for secure authentication infrastructure
- **Hugging Face** for pre-trained models and inference API
- **FAISS** for efficient similarity search
- **Sentence Transformers** for semantic embeddings
- **MMCOE** for the opportunity to build this platform

---

**🚀 Your AI-powered alumni portal with Firebase SSO is ready!**

**🔐 Authentication**: Firebase SSO + Legacy JWT Support  
**🤖 AI Features**: FAISS + Transformers + Smart Recommendations  
**🚢 Production Ready**: Docker + PostgreSQL + Redis + Celery  

**Choose your authentication method and start building amazing alumni connections!** 🌟
