import numpy as np
import faiss
import pickle
import redis
import logging
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
import os
import threading
from django.db.models import Q
from django.conf import settings

logger = logging.getLogger(__name__)

class FAISSRecommendationEngine:
    """FAISS-based recommendation engine for M2ConneX Alumni Portal"""
    
    def __init__(self, embedding_dim=384, index_path="/tmp/user_embeddings.index"):
        self.embedding_dim = embedding_dim
        self.index_path = index_path
        
        # Set cache directory for HuggingFace models
        cache_dir = "/tmp/transformers_cache"
        os.makedirs(cache_dir, exist_ok=True)
        
        # Initialize model with writable cache directory
        self.model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder=cache_dir)
        
        # FAISS index - Use IndexIDMap to support add_with_ids
        base_index = faiss.IndexFlatIP(embedding_dim)
        self.index = faiss.IndexIDMap(base_index)
        self.user_id_to_faiss_id = {}
        self.faiss_id_to_user_id = {}
        self.next_faiss_id = 0
        
        # Redis for feed rotation - try different Redis hosts
        self.redis_client = None
        redis_hosts = ['alumni-portal-redis', 'redis', 'localhost']
        
        for host in redis_hosts:
            try:
                self.redis_client = redis.Redis(
                    host=host, 
                    port=6379, 
                    db=0, 
                    decode_responses=True,
                    socket_connect_timeout=2
                )
                self.redis_client.ping()
                logger.info(f"Connected to Redis at {host} for feed rotation")
                break
            except Exception as e:
                logger.debug(f"Failed to connect to Redis at {host}: {e}")
                continue
        
        if not self.redis_client:
            logger.warning("Redis not available - feed rotation disabled")
        
        self.index_lock = threading.Lock()
        self.load_index()
    
    def create_user_text_representation(self, user):
        """Create text representation matching M2ConneX model structure"""
        components = []
        
        # Basic info - matching your AlumniPortalUser model
        if hasattr(user, 'firstName') and user.firstName:
            components.append(user.firstName)
        if hasattr(user, 'lastName') and user.lastName:
            components.append(user.lastName)
        
        # Department mapping from your DEPARTMENT_CHOICES
        department_map = {
            '1': 'Computer Engineering',
            '2': 'Mechanical Engineering', 
            '3': 'Electronics & Telecommunication Engineering',
            '4': 'Electrical Engineering',
            '5': 'Information Technology',
            '6': 'Artificial Intelligence & Data Science',
            '7': 'First Year Engineering',
            '8': 'MBA'
        }
        
        if hasattr(user, 'department') and user.department:
            dept_name = department_map.get(user.department, user.department)
            components.append(f"Department: {dept_name}")
        
        # Bio
        if hasattr(user, 'bio') and user.bio:
            components.append(f"Bio: {user.bio}")
        
        # Privilege info
        if hasattr(user, 'privilege') and user.privilege:
            components.append(f"Role: {user.privilege}")
        
        # Skills - using your UserSkill model structure
        try:
            user_skills = user.skills.all().select_related('skill')
            skills_list = []
            experience_map = {
                '1': 'interested',
                '2': 'beginner', 
                '3': 'intermediate',
                '4': 'expert',
                '5': 'gawd'
            }
            
            for us in user_skills:
                if us.skill and us.skill.name:
                    skill_name = us.skill.name
                    exp_level = experience_map.get(us.experience, us.experience)
                    
                    # Weight by experience level
                    if exp_level in ['expert', 'gawd']:
                        skills_list.extend([skill_name] * 3)
                    elif exp_level == 'intermediate':
                        skills_list.extend([skill_name] * 2)
                    else:
                        skills_list.append(skill_name)
            
            if skills_list:
                components.append(f"Skills: {' '.join(skills_list)}")
        except Exception as e:
            logger.debug(f"Error getting user skills: {e}")
        
        # Feed posts - using your Feed model structure  
        try:
            user_feeds = user.feed.all()[:10]  # Related name is 'feed' in your model
            for feed in user_feeds:
                feed_text = ""
                if hasattr(feed, 'subject') and feed.subject:
                    # Handle semicolon-separated subjects in your model
                    feed_text += feed.subject.replace(";", " ")
                if hasattr(feed, 'body') and feed.body:
                    feed_text += " " + feed.body
                if feed_text.strip():
                    components.append(f"Posted: {feed_text.strip()}")
        except Exception as e:
            logger.debug(f"Error getting user feeds: {e}")
        
        # Feed actions - using your FeedAction model
        try:
            feed_actions = user.feed_actions.all()[:20]  # Related name is 'feed_actions'
            action_content = []
            for action in feed_actions:
                if hasattr(action, 'feed') and action.feed:
                    feed = action.feed
                    action_text = ""
                    if hasattr(feed, 'subject') and feed.subject:
                        action_text += feed.subject.replace(";", " ")
                    if hasattr(feed, 'body') and feed.body:
                        action_text += " " + feed.body
                    if action_text.strip():
                        action_content.append(action_text.strip())
            
            if action_content:
                components.append(f"Engaged with: {' '.join(action_content)}")
        except Exception as e:
            logger.debug(f"Error getting feed actions: {e}")
        
        # Experience data - your Experience model
        try:
            experiences = user.experiences.all()
            exp_text = []
            for exp in experiences:
                if exp.company:
                    exp_text.append(exp.company)
                if exp.designation:
                    exp_text.append(exp.designation)
            if exp_text:
                components.append(f"Experience: {' '.join(exp_text)}")
        except Exception as e:
            logger.debug(f"Error getting experiences: {e}")
        
        # City/Location info
        try:
            if hasattr(user, 'city') and user.city:
                location_text = f"{user.city.name}, {user.city.state.name}, {user.city.state.country.name}"
                components.append(f"Location: {location_text}")
        except Exception as e:
            logger.debug(f"Error getting location: {e}")
        
        return ' '.join(components) if components else f"User {user.firstName or ''} {user.lastName or ''}"
    
    def get_or_create_user_embedding(self, user, force_refresh=False):
        """Get or create user embedding in FAISS"""
        user_id_str = str(user.id)
        
        # Check if user exists in FAISS and not forcing refresh
        if not force_refresh and user_id_str in self.user_id_to_faiss_id:
            faiss_id = self.user_id_to_faiss_id[user_id_str]
            try:
                # Try to reconstruct existing embedding
                embedding = self.index.reconstruct(faiss_id)
                return embedding
            except:
                # If reconstruction fails, remove from mappings and regenerate
                logger.warning(f"Failed to reconstruct embedding for user {user_id_str}, regenerating...")
                del self.user_id_to_faiss_id[user_id_str]
                if faiss_id in self.faiss_id_to_user_id:
                    del self.faiss_id_to_user_id[faiss_id]

        # Generate new embedding
        user_text = self.create_user_text_representation(user)
        embedding = self.model.encode(user_text, convert_to_numpy=True)
        embedding = embedding / np.linalg.norm(embedding)  # Normalize

        # Add to FAISS with proper locking
        with self.index_lock:
            if user_id_str in self.user_id_to_faiss_id and not force_refresh:
                # User was added by another thread, return existing
                faiss_id = self.user_id_to_faiss_id[user_id_str]
                try:
                    existing_embedding = self.index.reconstruct(faiss_id)
                    return existing_embedding
                except:
                    # Continue with adding new embedding
                    pass
            
            # Assign new unique FAISS ID
            faiss_id = self.next_faiss_id
            
            # Check if this FAISS ID is already in use (safety check)
            while faiss_id in self.faiss_id_to_user_id:
                faiss_id += 1
            
            # Update mappings
            self.user_id_to_faiss_id[user_id_str] = faiss_id
            self.faiss_id_to_user_id[faiss_id] = user_id_str
            self.next_faiss_id = faiss_id + 1
            
            try:
                # Add embedding to FAISS index
                self.index.add_with_ids(
                    embedding.reshape(1, -1).astype('float32'),
                    np.array([faiss_id], dtype=np.int64)
                )
                logger.debug(f"Added user {user_id_str} with FAISS ID {faiss_id}")
            except Exception as e:
                # If adding fails, clean up mappings
                logger.error(f"Failed to add user {user_id_str} to FAISS index: {e}")
                if user_id_str in self.user_id_to_faiss_id:
                    del self.user_id_to_faiss_id[user_id_str]
                if faiss_id in self.faiss_id_to_user_id:
                    del self.faiss_id_to_user_id[faiss_id]
                raise

        return embedding
    
    def get_shown_posts(self, user_id):
        """Get posts already shown to user"""
        if not self.redis_client:
            return set()
        
        try:
            shown_posts = self.redis_client.smembers(f"shown_posts:{user_id}")
            return {int(post_id) for post_id in shown_posts}
        except:
            return set()
    
    def mark_posts_as_shown(self, user_id, post_ids):
        """Mark posts as shown to user"""
        if not self.redis_client or not post_ids:
            return
        
        try:
            key = f"shown_posts:{user_id}"
            self.redis_client.sadd(key, *post_ids)
            self.redis_client.expire(key, 3600 * 24)  # 24 hour TTL
        except Exception as e:
            logger.debug(f"Error marking posts as shown: {e}")
    
    def calculate_mutual_connections_score(self, user1, user2):
        """Calculate mutual connections score using your Connection model"""
        try:
            from connection.models import Connection
            
            # Get user1's connections
            user1_connections = set()
            connections1_a = Connection.objects.filter(userA=user1, status='accepted')
            connections1_b = Connection.objects.filter(userB=user1, status='accepted')
            
            for conn in connections1_a:
                user1_connections.add(conn.userB.id)
            for conn in connections1_b:
                user1_connections.add(conn.userA.id)
            
            # Get user2's connections  
            user2_connections = set()
            connections2_a = Connection.objects.filter(userA=user2, status='accepted')
            connections2_b = Connection.objects.filter(userB=user2, status='accepted')
            
            for conn in connections2_a:
                user2_connections.add(conn.userB.id)
            for conn in connections2_b:
                user2_connections.add(conn.userA.id)
            
            # Calculate mutual connections
            mutual = len(user1_connections & user2_connections)
            return min(1.0, mutual / 5.0)  # Normalize to max 1.0
        except Exception as e:
            logger.debug(f"Error calculating mutual connections: {e}")
            return 0.0
    
    def save_index(self):
        """Save FAISS index to disk"""
        try:
            with self.index_lock:
                faiss.write_index(self.index, self.index_path)
                
                mappings = {
                    'user_id_to_faiss_id': self.user_id_to_faiss_id,
                    'faiss_id_to_user_id': self.faiss_id_to_user_id,
                    'next_faiss_id': self.next_faiss_id
                }
                
                with open(f"{self.index_path}.mappings", 'wb') as f:
                    pickle.dump(mappings, f)
                logger.info("FAISS index saved successfully")
        except Exception as e:
            logger.error(f"Error saving FAISS index: {e}")
    
    def load_index(self):
        """Load FAISS index from disk"""
        try:
            if os.path.exists(self.index_path):
                loaded_index = faiss.read_index(self.index_path)
                # Ensure we have IndexIDMap
                if not isinstance(loaded_index, faiss.IndexIDMap):
                    base_index = faiss.IndexFlatIP(self.embedding_dim)
                    self.index = faiss.IndexIDMap(base_index)
                else:
                    self.index = loaded_index
                
                mappings_path = f"{self.index_path}.mappings"
                if os.path.exists(mappings_path):
                    with open(mappings_path, 'rb') as f:
                        mappings = pickle.load(f)
                    
                    self.user_id_to_faiss_id = mappings.get('user_id_to_faiss_id', {})
                    self.faiss_id_to_user_id = mappings.get('faiss_id_to_user_id', {})
                    self.next_faiss_id = mappings.get('next_faiss_id', 0)
                
                logger.info(f"Loaded FAISS index with {self.index.ntotal} users")
            else:
                logger.info("No existing FAISS index found, starting fresh")
                base_index = faiss.IndexFlatIP(self.embedding_dim)
                self.index = faiss.IndexIDMap(base_index)
        except Exception as e:
            logger.error(f"Error loading FAISS index: {e}")
            base_index = faiss.IndexFlatIP(self.embedding_dim)
            self.index = faiss.IndexIDMap(base_index)


# Global engine instance
_recommendation_engine = None

def get_recommendation_engine():
    """Get or create global recommendation engine instance"""
    global _recommendation_engine
    if _recommendation_engine is None:
        _recommendation_engine = FAISSRecommendationEngine()
    return _recommendation_engine


def get_feed_recommendation(qs, user):
    """
    Enhanced FAISS-based feed recommendation - drop-in replacement
    
    Args:
        qs: Queryset of Feed objects
        user: Current user
    
    Returns:
        Tuple of (feed_objects, similarity_scores) - SAME as your original
    """
    engine = get_recommendation_engine()
    
    # Get all feed objects (same as your original)
    feed_objects = list(qs.all())
    
    if len(feed_objects) == 0:
        return feed_objects, []
    
    # Check if user has any feed actions (same logic as your original)
    try:
        liked_feed_objects = qs.filter(
            id__in=user.feed_actions.all().values_list('feed', flat=True)
        )
        
        if liked_feed_objects.count() == 0:
            return feed_objects, []
    except:
        # If no feed actions, return original order with zero scores
        return feed_objects, [0.0] * len(feed_objects)
    
    try:
        # Get user embedding
        user_embedding = engine.get_or_create_user_embedding(user)
        
        # Filter out already shown posts for better user experience
        shown_posts = engine.get_shown_posts(user.id)
        available_feeds = [f for f in feed_objects if f.id not in shown_posts]
        
        if not available_feeds:
            # If all posts shown, use all feeds with slight preference for unseen
            available_feeds = feed_objects
        
        # Calculate similarities for each feed
        feed_similarities = []
        for feed in available_feeds:
            # Create feed text representation
            feed_text = ""
            if hasattr(feed, 'subject') and feed.subject:
                # Handle your semicolon-separated subjects
                feed_text += feed.subject.replace(";", " ")
            if hasattr(feed, 'body') and feed.body:
                feed_text += " " + feed.body
            
            if feed_text.strip():
                # Get feed embedding
                feed_embedding = engine.model.encode(feed_text, convert_to_numpy=True)
                feed_embedding = feed_embedding / np.linalg.norm(feed_embedding)
                
                # Calculate similarity
                similarity = np.dot(user_embedding, feed_embedding)
                
                # Boost score if not shown recently
                if feed.id not in shown_posts:
                    similarity += 0.1  # Small boost for fresh content
                    
                # Consider feed author's connection to user
                try:
                    if feed.user != user:
                        connection_boost = engine.calculate_mutual_connections_score(user, feed.user)
                        similarity += 0.2 * connection_boost
                except:
                    pass
                    
            else:
                similarity = 0.0
            
            feed_similarities.append((feed, similarity))
        
        # Add remaining feeds that weren't in available_feeds
        remaining_feeds = [f for f in feed_objects if f not in available_feeds]
        for feed in remaining_feeds:
            feed_similarities.append((feed, -1.0))  # Lower score for already shown
        
        # Sort by similarity (same as your original sorting)
        feed_similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Prepare return values in same format as your original
        sorted_feeds = [feed for feed, _ in feed_similarities]
        sorted_scores = [score for _, score in feed_similarities]
        
        # Mark top posts as shown for feed rotation
        shown_feed_ids = [feed.id for feed in sorted_feeds[:20]]
        engine.mark_posts_as_shown(user.id, shown_feed_ids)
        
        return sorted_feeds, sorted_scores
        
    except Exception as e:
        logger.error(f"Error in FAISS feed recommendation: {e}")
        # Fallback to original TF-IDF method
        from CODE.utils.recommendations import get_feed_recommendation as original_get_feed_recommendation
        return original_get_feed_recommendation(qs, user)


def get_user_recommendation(qs, current_user):
    """
    Enhanced FAISS-based user recommendation - drop-in replacement
    
    Args:
        qs: Queryset of User objects  
        current_user: Current user
    
    Returns:
        Tuple of (user_objects, similarity_scores) - SAME as your original
    """
    engine = get_recommendation_engine()
    
    # Get all user objects (same as your original)
    user_objects = list(qs.all())
    
    if len(user_objects) == 0:
        return user_objects, []
    
    # Same minimum user check as your original
    if len(user_objects) < 6:
        return user_objects, []
    
    try:
        # Get current user embedding
        current_user_embedding = engine.get_or_create_user_embedding(current_user)
        
        # Filter out current user
        other_users = [u for u in user_objects if u.id != current_user.id]
        
        # Filter out existing connections using your Connection model
        try:
            from connection.models import Connection
            existing_connections = set()
            
            # Get connections where current_user is userA
            connections_a = Connection.objects.filter(userA=current_user)
            for conn in connections_a:
                existing_connections.add(conn.userB.id)
            
            # Get connections where current_user is userB  
            connections_b = Connection.objects.filter(userB=current_user)
            for conn in connections_b:
                existing_connections.add(conn.userA.id)
            
            other_users = [u for u in other_users if u.id not in existing_connections]
        except Exception as e:
            logger.debug(f"Error filtering connections: {e}")
        
        if not other_users:
            return user_objects, []
        
        # Calculate similarities
        user_similarities = []
        for user in other_users:
            try:
                user_embedding = engine.get_or_create_user_embedding(user)
                similarity = np.dot(current_user_embedding, user_embedding)
                
                # Add mutual connections boost (similar to your original logic)
                mutual_boost = engine.calculate_mutual_connections_score(current_user, user)
                
                # Weight similarity more heavily, but include mutual connections
                final_score = 0.8 * similarity + 0.2 * mutual_boost
                
                # Add small departmental boost if same department
                if (hasattr(current_user, 'department') and hasattr(user, 'department') and 
                    current_user.department == user.department and current_user.department):
                    final_score += 0.1
                
                user_similarities.append((user, final_score))
            except Exception as e:
                logger.debug(f"Error calculating similarity for user {user.id}: {e}")
                user_similarities.append((user, 0.0))
        
        # Sort by similarity (same as your original)
        user_similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Add small random noise (same as your original)
        import random
        for i, (user, score) in enumerate(user_similarities):
            noise = random.uniform(-0.05, 0.05)
            user_similarities[i] = (user, score + noise)
        
        # Re-sort with noise
        user_similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Prepare return values in same format as your original
        sorted_users = [user for user, _ in user_similarities]
        sorted_scores = [score for _, score in user_similarities]
        
        # Extend to match original queryset if needed
        remaining_users = [u for u in user_objects if u not in sorted_users and u.id != current_user.id]
        sorted_users.extend(remaining_users)
        sorted_scores.extend([0.0] * len(remaining_users))
        
        return sorted_users, sorted_scores
        
    except Exception as e:
        logger.error(f"Error in FAISS user recommendation: {e}")
        # Fallback to original TF-IDF method
        from CODE.utils.recommendations import get_user_recommendation as original_get_user_recommendation
        return original_get_user_recommendation(qs, current_user)


# Celery tasks for maintenance (compatible with your existing celery setup)
try:
    from alumniportal.celery import app
    
    @app.task(bind=True)
    def rebuild_faiss_index(self):
        """Rebuild entire FAISS index"""
        engine = get_recommendation_engine()
        
        from users.models import AlumniPortalUser
        users = AlumniPortalUser.objects.filter(is_active=True, isVerified=True)
        
        logger.info(f"Rebuilding FAISS index for {users.count()} users")
        
        for user in users:
            try:
                engine.get_or_create_user_embedding(user, force_refresh=True)
            except Exception as e:
                logger.error(f"Error updating user {user.id}: {e}")
        
        engine.save_index()
        logger.info("FAISS index rebuild complete")
        return f"Rebuilt index for {users.count()} users"
    
    @app.task(bind=True)
    def save_faiss_index(self):
        """Save FAISS index to disk"""
        engine = get_recommendation_engine()
        engine.save_index()
        return "FAISS index saved"
        
except ImportError:
    logger.warning("Celery not available - maintenance tasks disabled")