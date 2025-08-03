# M2ConneX - AI-Powered Alumni Portal

![GitHub stars](https://img.shields.io/github/stars/NotShrirang/M2ConneX?style=social)
![GitHub forks](https://img.shields.io/github/forks/NotShrirang/M2ConneX?style=social)
![GitHub issues](https://img.shields.io/github/issues/NotShrirang/M2ConneX)
![GitHub pull requests](https://img.shields.io/github/issues-pr/NotShrirang/M2ConneX)
![GitHub](https://img.shields.io/github/license/NotShrirang/M2ConneX)
![GitHub last commit](https://img.shields.io/github/last-commit/NotShrirang/M2ConneX)
![GitHub repo size](https://img.shields.io/github/repo-size/NotShrirang/M2ConneX)

[![DB Diagram](https://img.shields.io/badge/DB%20Diagram-blue?style=for-the-badge&logo=sqlite&logoColor=white&logoSize=amd)](https://dbdiagram.io/d/MMCOE-Alumni-Portal-654ce8d57d8bbd6465dac5ae)

## Overview

M2ConneX is a comprehensive AI-powered platform designed to connect alumni of MMCOE (Marathwada Mitra Mandal's College of Engineering) and facilitate intelligent networking, collaboration, and content discovery. The portal features advanced machine learning-based recommendation systems that provide personalized content, connection suggestions, and smart job matching.

**🤖 AI-Powered Features:**
- **Semantic Content Recommendations**: Uses FAISS + Sentence Transformers for intelligent feed curation
- **Smart User Matching**: ML-based connection recommendations using profile similarity
- **Personalized Job Suggestions**: Skills-based opportunity matching with semantic understanding
- **Content Feed Rotation**: Prevents repetitive content using Redis-backed tracking
- **Real-time NSFW Detection**: Hugging Face API integration for content moderation

This is the backend API developed for the platform.
#### Frontend - https://github.com/NotShrirang/M2ConneX-frontend

## Features

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

![m2connex](https://github.com/user-attachments/assets/591dc730-0963-4e9b-8211-d9d555fedcf0)

## AI/ML Technology Stack

- **FAISS**: Vector similarity search for real-time recommendations
- **Sentence Transformers**: Semantic embedding generation (`all-MiniLM-L6-v2`)
- **Hugging Face Transformers**: Pre-trained language models
- **Redis**: Caching and feed rotation management
- **PyTorch**: Deep learning framework
- **scikit-learn**: Traditional ML algorithms
- **NumPy**: Numerical computing

## Getting Started

### Prerequisites

- Docker Desktop
- 8GB+ RAM (recommended for ML models)
- Python 3.9+ (for local development)

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

# Email Configuration
EMAIL=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# AI/ML Configuration
TEXT_NSFW_TOKEN=your_huggingface_token_here
TRANSFORMERS_CACHE=/tmp/transformers_cache
HF_HOME=/tmp/huggingface
TORCH_HOME=/tmp/torch
TOKENIZERS_PARALLELISM=false

# Optional: Hugging Face API Token for enhanced features
HUGGINGFACE_API_TOKEN=your_hf_api_token
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

#### 3. Build AI Recommendation Index
```bash
# Build FAISS index for personalized recommendations
docker exec -it alumni-portal-backend python manage.py build_faiss_index --rebuild
```

#### 4. Create Admin User
```bash
docker exec -it alumni-portal-backend python manage.py shell
```
```python
from users.models import AlumniPortalUser, SuperAdmin
from csc.models import City

city = City.objects.first()
user = AlumniPortalUser.objects.create_user(
    email='admin@mmcoe.edu.in',
    password='admin123',
    firstName='Admin',
    lastName='User',
    department='1',
    privilege='Super Admin',
    city=city,
    isVerified=True,
    is_active=True,
    is_superuser=True,
    is_staff=True
)
SuperAdmin.objects.create(user=user)
print("Admin created: admin@mmcoe.edu.in / admin123")
exit()
```

### Manual Setup (Alternative)

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set environment variables:**
```bash
export TRANSFORMERS_CACHE=/tmp/transformers_cache
export HF_HOME=/tmp/huggingface
export TORCH_HOME=/tmp/torch
export TOKENIZERS_PARALLELISM=false
```

3. **Run migrations and start server:**
```bash
python manage.py migrate
python manage.py runserver
```

## AI Recommendation System Setup

### Understanding the Recommendation Engine

The M2ConneX recommendation system uses a sophisticated FAISS-based approach:

1. **User Embeddings**: Creates semantic representations of users based on:
   - Profile information (bio, department, skills)
   - Activity patterns (posts, likes, comments)
   - Professional experience
   - Connection network

2. **Content Analysis**: Analyzes posts and content using:
   - Semantic similarity matching
   - User interaction history
   - Connection-based filtering

3. **Real-time Recommendations**: Provides instant suggestions for:
   - Personalized feed content
   - User connections
   - Job opportunities
   - Event recommendations

### Building the Recommendation Index

```bash
# Full rebuild (recommended after major data changes)
docker exec -it alumni-portal-backend python manage.py build_faiss_index --rebuild

# Incremental update (for new users)
docker exec -it alumni-portal-backend python manage.py build_faiss_index
```

### Testing the Recommendation System

```bash
docker exec -it alumni-portal-backend python manage.py shell
```

```python
# Test the recommendation engine
from CODE.utils.recommendations import get_recommendation_engine
from users.models import AlumniPortalUser

engine = get_recommendation_engine()
users = AlumniPortalUser.objects.filter(is_active=True, isVerified=True)
print(f"Users in index: {engine.index.ntotal}")
print(f"Total active users: {users.count()}")

# Test user embedding
test_user = users.first()
embedding = engine.get_or_create_user_embedding(test_user)
print(f"Embedding shape: {embedding.shape}")
```

### Monitoring Recommendations

Check the recommendation system logs:
```bash
# View recommendation engine logs
docker logs alumni-portal-backend | grep -i "recommendation\|faiss\|embedding"

# Monitor ML model loading
docker logs alumni-portal-backend | grep -i "transformers\|sentence"
```

## API Endpoints

### Authentication
```bash
# Login
POST /users/login/
{
    "email": "admin@mmcoe.edu.in",
    "password": "admin123"
}
```

### AI-Powered Endpoints
```bash
# Personalized feed recommendations
GET /feed/recommend-feed/
Authorization: Bearer <token>

# Smart user connections
GET /connection/recommend-connection/
Authorization: Bearer <token>

# Skill-based job matching
GET /opportunity/recommend-opportunity/?search=python
Authorization: Bearer <token>
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

1. **Cache Permission Errors**:
```bash
docker exec -it alumni-portal-backend bash -c "
mkdir -p /tmp/transformers_cache /tmp/huggingface /tmp/torch
chmod 777 /tmp/transformers_cache /tmp/huggingface /tmp/torch
"
```

2. **Memory Issues with ML Models**:
```bash
# Restart containers to free memory
docker-compose -p alumni-portal-dev -f docker-compose-dev.yml restart backend
```

3. **FAISS Index Corruption**:
```bash
# Rebuild the index
docker exec -it alumni-portal-backend python manage.py build_faiss_index --rebuild
```

4. **No Recommendations Appearing**:
```bash
# Check if index is built and has data
docker exec -it alumni-portal-backend python -c "
from CODE.utils.recommendations import get_recommendation_engine
engine = get_recommendation_engine()
print(f'Index size: {engine.index.ntotal}')
"
```

### Performance Monitoring

```bash
# Check memory usage
docker stats alumni-portal-backend

# Monitor ML model loading
docker logs alumni-portal-backend --tail 100 | grep -E "(FAISS|embedding|model)"

# Check API response times
curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:8000/feed/recommend-feed/" -H "Authorization: Bearer <token>"
```

## Docker Services

- **backend**: Django API server with ML capabilities
- **db**: PostgreSQL database
- **redis**: Caching and session management
- **rabbit-mq**: Celery task queue
- **celery**: Background task processing
- **flower**: Task monitoring
- **pgadmin**: Database administration

## Development

### Adding New Recommendation Features

1. **Extend User Representation**:
```python
# In CODE/utils/recommendations.py
def create_user_text_representation(self, user):
    # Add new user attributes for better recommendations
    components.append(f"New_Feature: {user.new_field}")
```

2. **Custom Similarity Metrics**:
```python
# Add domain-specific similarity calculations
def calculate_custom_similarity(self, user1, user2):
    # Implement custom similarity logic
    return similarity_score
```

3. **A/B Testing Framework**:
```python
# Implement recommendation variants for testing
def get_recommendation_variant(self, user, variant='default'):
    # Return different recommendation strategies
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/ai-enhancement`
3. Commit changes: `git commit -am 'Add new AI feature'`
4. Push to branch: `git push origin feature/ai-enhancement`
5. Submit a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review API documentation at `/swagger/`

## Acknowledgments

- **Hugging Face** for pre-trained models and inference API
- **FAISS** for efficient similarity search
- **Sentence Transformers** for semantic embeddings
- **MMCOE** for the opportunity to build this platform

---

**🚀 Your AI-powered alumni portal is ready!** The recommendation system will improve over time as users interact with the platform.