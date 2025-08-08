from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.db import models
from datetime import datetime, timedelta
import random
from faker import Faker

from users.models import AlumniPortalUser, Alumni, Student, Faculty, SuperAdmin
from csc.models import Country, State, City
from skill.models import Skill, UserSkill
from experience.models import Experience
from opportunity.models import Opportunity, OpportunitySkill, OpportunityApplication
from feed.models import Feed, FeedImage, FeedAction, FeedActionComment
from event.models import Event, EventImage
from blog.models import Blog, BlogAction, BlogComment
from connection.models import Connection
from club.models import Club, ClubMember
from donation.models import Donation

fake = Faker()

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=50, help='Number of users to create')
        parser.add_argument('--posts', type=int, default=100, help='Number of posts to create')
        parser.add_argument('--opportunities', type=int, default=30, help='Number of opportunities to create')
        parser.add_argument('--events', type=int, default=20, help='Number of events to create')
        parser.add_argument('--blogs', type=int, default=25, help='Number of blogs to create')

    def handle(self, *args, **options):
        self.stdout.write('Starting database population...')
        
        # Create basic data first
        self.create_locations()
        self.create_skills()
        
        # Create users and their profiles
        users = self.create_users(options['users'])
        
        # Create relationships and content
        self.create_connections(users)
        self.create_experiences(users)
        self.create_opportunities(users, options['opportunities'])
        self.create_feeds(users, options['posts'])
        self.create_events(users, options['events'])
        self.create_blogs(users, options['blogs'])
        self.create_clubs_and_members(users)
        self.create_donations(users)
        
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))

    def create_locations(self):
        self.stdout.write('Creating locations...')
        
        # Create countries
        countries_data = [
            'India', 'United States', 'United Kingdom', 'Canada', 'Australia',
            'Germany', 'France', 'Japan', 'Singapore', 'UAE'
        ]
        
        countries = []
        for country_name in countries_data:
            country, created = Country.objects.get_or_create(name=country_name)
            countries.append(country)
        
        # Create states and cities
        india = countries[0]  # Assuming India is first
        
        states_cities = {
            'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad'],
            'Karnataka': ['Bangalore', 'Mysore', 'Hubli', 'Mangalore'],
            'Delhi': ['New Delhi', 'Delhi'],
            'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai'],
            'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara']
        }
        
        for state_name, cities in states_cities.items():
            state, created = State.objects.get_or_create(name=state_name, country=india)
            for city_name in cities:
                City.objects.get_or_create(name=city_name, state=state)

    def create_skills(self):
        self.stdout.write('Creating skills...')
        
        skills_data = [
            'Python', 'JavaScript', 'Java', 'C++', 'React', 'Django', 'Flask',
            'Node.js', 'Angular', 'Vue.js', 'Machine Learning', 'Data Science',
            'Artificial Intelligence', 'Cloud Computing', 'AWS', 'Docker',
            'Kubernetes', 'DevOps', 'Git', 'SQL', 'MongoDB', 'PostgreSQL',
            'HTML', 'CSS', 'Bootstrap', 'Tailwind CSS', 'TypeScript',
            'Android Development', 'iOS Development', 'Flutter', 'React Native',
            'Cybersecurity', 'Blockchain', 'IoT', 'Robotics', 'Computer Vision',
            'Natural Language Processing', 'Deep Learning', 'TensorFlow',
            'PyTorch', 'Selenium', 'Jest', 'Unit Testing', 'Agile', 'Scrum',
            'Project Management', 'Leadership', 'Communication', 'Problem Solving',
            'Critical Thinking', 'Team Work', 'Public Speaking', 'Technical Writing'
        ]
        
        for skill_name in skills_data:
            Skill.objects.get_or_create(name=skill_name)

    def create_users(self, count):
        self.stdout.write(f'Creating {count} users...')
        
        departments = ['1', '2', '3', '4', '5', '6', '7', '8']
        privileges = ['Alumni', 'Student', 'Staff']
        cities = list(City.objects.all())
        skills = list(Skill.objects.all())
        
        users = []
        
        # Create a super admin first
        super_admin = AlumniPortalUser.objects.create(
            email='admin@mmcoe.edu.in',
            firstName='Admin',
            lastName='User',
            department=random.choice(departments),
            privilege='Super Admin',
            bio='System Administrator',
            city=random.choice(cities),
            phoneNumber='+919876543210',
            isVerified=True,
            is_active=True,
            is_superuser=True,
            is_staff=True,
            is_admin=True
        )
        super_admin.set_password('admin123')
        super_admin.save()
        
        SuperAdmin.objects.create(user=super_admin)
        users.append(super_admin)
        
        for i in range(count - 1):
            privilege = random.choice(privileges)
            department = random.choice(departments)
            
            user = AlumniPortalUser.objects.create(
                email=fake.unique.email(),
                firstName=fake.first_name(),
                lastName=fake.last_name(),
                department=department,
                privilege=privilege,
                bio=fake.text(max_nb_chars=200),
                city=random.choice(cities),
                phoneNumber=fake.phone_number(),
                isVerified=True,
                is_active=True
            )
            user.set_password('password123')
            user.save()
            
            # Create profile based on privilege
            if privilege == 'Alumni':
                batch = random.randint(2015, 2023)
                Alumni.objects.create(
                    user=user,
                    batch=batch,
                    enrollmentYear=datetime(batch - 4, 6, 1),
                    passingOutYear=datetime(batch, 5, 31)
                )
            elif privilege == 'Student':
                batch = random.randint(2024, 2028)
                Student.objects.create(
                    user=user,
                    batch=batch,
                    enrollmentYear=datetime(batch - 4, 6, 1),
                    passingOutYear=datetime(batch, 5, 31)
                )
            elif privilege == 'Staff':
                Faculty.objects.create(
                    user=user,
                    college='MMCOE'
                )
            
            # Add random skills
            user_skills = random.sample(skills, random.randint(3, 8))
            for skill in user_skills:
                UserSkill.objects.create(
                    user=user,
                    skill=skill,
                    experience=random.choice(['1', '2', '3', '4', '5'])
                )
            
            users.append(user)
        
        return users

    def create_connections(self, users):
        self.stdout.write('Creating connections...')
        
        for _ in range(len(users) * 3):  # Each user gets ~3 connections on average
            user_a, user_b = random.sample(users, 2)
            if not Connection.objects.filter(
                models.Q(userA=user_a, userB=user_b) | models.Q(userA=user_b, userB=user_a)
            ).exists():
                Connection.objects.create(
                    userA=user_a,
                    userB=user_b,
                    status=random.choice(['pending', 'accepted', 'accepted', 'accepted'])  # More accepted
                )

    def create_experiences(self, users):
        self.stdout.write('Creating experiences...')
        
        alumni_users = [u for u in users if hasattr(u, 'alumni')]
        companies = [
            'Google', 'Microsoft', 'Amazon', 'Apple', 'Meta', 'Netflix', 'Tesla',
            'IBM', 'Oracle', 'Salesforce', 'Adobe', 'Uber', 'Airbnb', 'Spotify',
            'TCS', 'Infosys', 'Wipro', 'Cognizant', 'Accenture', 'Capgemini',
            'Startups Inc', 'Tech Solutions', 'Innovation Labs', 'Digital Dynamics'
        ]
        
        positions = [
            'Software Engineer', 'Senior Software Engineer', 'Lead Developer',
            'Full Stack Developer', 'Frontend Developer', 'Backend Developer',
            'Data Scientist', 'Machine Learning Engineer', 'DevOps Engineer',
            'Product Manager', 'Technical Lead', 'Architect', 'Consultant'
        ]
        
        for user in alumni_users:
            # Create 1-3 experiences per alumni
            for _ in range(random.randint(1, 3)):
                start_date = fake.date_between(start_date='-5y', end_date='-1y')
                is_current = random.choice([True, False, False])  # 1/3 chance current
                end_date = None if is_current else fake.date_between(start_date=start_date, end_date='today')
                
                Experience.objects.create(
                    user=user,
                    company=random.choice(companies),
                    designation=random.choice(positions),
                    description=fake.text(max_nb_chars=300),
                    startDate=start_date,
                    endDate=end_date,
                    isCurrent=is_current
                )

    def create_opportunities(self, users, count):
        self.stdout.write(f'Creating {count} opportunities...')
        
        alumni_users = [u for u in users if hasattr(u, 'alumni')]
        skills = list(Skill.objects.all())
        
        opportunity_types = ['Job', 'Internship', 'Consultancy']
        companies = [
            'Google', 'Microsoft', 'Amazon', 'Meta', 'Apple', 'Netflix',
            'TCS', 'Infosys', 'Wipro', 'Accenture', 'Startups Inc'
        ]
        
        job_titles = [
            'Software Developer', 'Data Scientist', 'Machine Learning Engineer',
            'Full Stack Developer', 'Frontend Developer', 'Backend Developer',
            'DevOps Engineer', 'Product Manager', 'UI/UX Designer',
            'Mobile App Developer', 'Cloud Engineer', 'Cybersecurity Analyst'
        ]
        
        locations = ['Mumbai', 'Pune', 'Bangalore', 'Hyderabad', 'Chennai', 'Delhi', 'Remote']
        work_modes = ['Remote', 'In Office', 'Hybrid']
        
        for _ in range(count):
            opportunity = Opportunity.objects.create(
                name=random.choice(job_titles),
                description=fake.text(max_nb_chars=500),
                payPerMonth=random.randint(50000, 200000) if random.choice([True, False]) else None,
                isPaid=random.choice([True, False]),
                user=random.choice(alumni_users),
                type=random.choice(opportunity_types),
                companyName=random.choice(companies),
                startDate=fake.date_between(start_date='today', end_date='+6m'),
                endDate=fake.date_between(start_date='+6m', end_date='+2y') if random.choice([True, False]) else None,
                location=random.choice(locations),
                workMode=random.choice(work_modes)
            )
            
            # Add required skills
            required_skills = random.sample(skills, random.randint(2, 5))
            for skill in required_skills:
                OpportunitySkill.objects.create(
                    opportunity=opportunity,
                    skill=skill
                )
            
            # Create some applications
            applicants = random.sample([u for u in users if u != opportunity.user], random.randint(0, 5))
            for applicant in applicants:
                OpportunityApplication.objects.create(
                    opportunity=opportunity,
                    applicant=applicant,
                    about=fake.text(max_nb_chars=300),
                    status=random.choice(['PENDING', 'ACCEPTED', 'REJECTED'])
                )

    def create_feeds(self, users, count):
        self.stdout.write(f'Creating {count} feed posts...')
        
        subjects = [
            'Excited to share my new project!',
            'Looking for collaboration opportunities',
            'Thoughts on the latest tech trends',
            'Celebrating a milestone',
            'Learning something new',
            'Industry insights',
            'Career update',
            'Technical discussion',
            'Event announcement',
            'Achievement unlocked!'
        ]
        
        for _ in range(count):
            feed = Feed.objects.create(
                subject=random.choice(subjects),
                body=fake.text(max_nb_chars=800),
                user=random.choice(users),
                isPublic=random.choice([True, True, True, False])  # Mostly public
            )
            
            # Create some likes and comments
            likers = random.sample(users, random.randint(0, 10))
            for liker in likers:
                if liker != feed.user:
                    action = FeedAction.objects.create(
                        feed=feed,
                        action='LIKE',
                        user=liker
                    )
            
            # Create some comments
            commenters = random.sample(users, random.randint(0, 3))
            for commenter in commenters:
                if commenter != feed.user:
                    action = FeedAction.objects.create(
                        feed=feed,
                        action='COMMENT',
                        user=commenter
                    )
                    FeedActionComment.objects.create(
                        feedAction=action,
                        comment=fake.sentence()
                    )

    def create_events(self, users, count):
        self.stdout.write(f'Creating {count} events...')
        
        event_names = [
            'Tech Talk: AI and Machine Learning',
            'Alumni Meetup 2024',
            'Career Guidance Workshop',
            'Coding Competition',
            'Industry Panel Discussion',
            'Startup Pitch Event',
            'Technical Symposium',
            'Research Paper Presentation',
            'Networking Session',
            'Innovation Challenge'
        ]
        
        departments = ['1', '2', '3', '4', '5', '6', '7', '8']
        venues = ['Auditorium', 'Conference Hall', 'Seminar Room', 'Online', 'Campus Ground']
        
        for _ in range(count):
            Event.objects.create(
                name=random.choice(event_names),
                description=fake.text(max_nb_chars=400),
                date=fake.date_between(start_date='today', end_date='+6m'),
                time=fake.time(),
                venue=random.choice(venues),
                department=random.choice(departments),
                link=fake.url() if random.choice([True, False]) else None,
                createdByUser=random.choice([u for u in users if u.privilege in ['Staff', 'Super Admin']])
            )

    def create_blogs(self, users, count):
        self.stdout.write(f'Creating {count} blogs...')
        
        blog_titles = [
            'The Future of Artificial Intelligence',
            'Best Practices in Software Development',
            'Career Tips for Fresh Graduates',
            'Industry Trends to Watch',
            'My Journey in Tech',
            'Building Scalable Applications',
            'Data Science Fundamentals',
            'Cybersecurity in Modern World',
            'Cloud Computing Benefits',
            'Mobile App Development Guide'
        ]
        
        keywords_list = [
            'technology, AI, machine learning',
            'software, development, programming',
            'career, tips, guidance',
            'industry, trends, analysis',
            'personal, journey, experience'
        ]
        
        for _ in range(count):
            blog = Blog.objects.create(
                title=random.choice(blog_titles),
                content=fake.text(max_nb_chars=2000),
                author=random.choice(users),
                keywords=random.choice(keywords_list),
                isPublic=random.choice([True, True, True, False]),
                isDrafted=random.choice([True, False, False, False])
            )
            
            # Create some blog actions
            readers = random.sample(users, random.randint(0, 8))
            for reader in readers:
                if reader != blog.author:
                    action_type = random.choice(['like', 'comment'])
                    action = BlogAction.objects.create(
                        action=action_type,
                        user=reader,
                        blog=blog
                    )
                    
                    if action_type == 'comment':
                        BlogComment.objects.create(
                            comment=fake.sentence(),
                            user=reader,
                            action=action
                        )

    def create_clubs_and_members(self, users):
        self.stdout.write('Creating clubs and members...')
        
        clubs_data = [
            {'name': 'Computer Society of India', 'description': 'Promoting computer science and technology'},
            {'name': 'Robotics Club', 'description': 'Building and programming robots'},
            {'name': 'Data Science Club', 'description': 'Exploring data analytics and machine learning'},
            {'name': 'Entrepreneurship Cell', 'description': 'Fostering startup culture'},
            {'name': 'Technical Writing Club', 'description': 'Improving technical communication skills'}
        ]
        
        for club_data in clubs_data:
            club = Club.objects.create(
                name=club_data['name'],
                description=club_data['description'],
                logo='https://via.placeholder.com/150',
                website=fake.url(),
                email=fake.email()
            )
            
            # Add members
            members = random.sample(users, random.randint(5, 15))
            positions = ['faculty_mentor', 'head', 'core_member', 'member']
            
            for i, member in enumerate(members):
                if i == 0:
                    position = 'faculty_mentor'
                    is_admin = True
                elif i == 1:
                    position = 'head'
                    is_admin = True
                elif i < 4:
                    position = 'core_member'
                    is_admin = False
                else:
                    position = 'member'
                    is_admin = False
                
                ClubMember.objects.create(
                    user=member,
                    club=club,
                    position=position,
                    positionInWords=position.replace('_', ' ').title(),
                    isClubAdmin=is_admin
                )

    def create_donations(self, users):
        self.stdout.write('Creating donations...')
        
        alumni_users = [u for u in users if hasattr(u, 'alumni')]
        departments = ['1', '2', '3', '4', '5', '6', '7', '8']
        
        donation_purposes = [
            'Scholarship Fund',
            'Infrastructure Development',
            'Laboratory Equipment',
            'Library Enhancement',
            'Student Activities',
            'Research Funding'
        ]
        
        for _ in range(20):
            Donation.objects.create(
                name=random.choice(donation_purposes),
                description=fake.text(max_nb_chars=200),
                amount=random.randint(1000, 100000),
                user=random.choice(alumni_users),
                department=random.choice(departments)
            )