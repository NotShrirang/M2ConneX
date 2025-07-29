# M2ConneX


![GitHub stars](https://img.shields.io/github/stars/NotShrirang/M2ConneX?style=social)
![GitHub forks](https://img.shields.io/github/forks/NotShrirang/M2ConneX?style=social)
![GitHub issues](https://img.shields.io/github/issues/NotShrirang/M2ConneX)
![GitHub pull requests](https://img.shields.io/github/issues-pr/NotShrirang/M2ConneX)
![GitHub](https://img.shields.io/github/license/NotShrirang/M2ConneX)
![GitHub last commit](https://img.shields.io/github/last-commit/NotShrirang/M2ConneX)
![GitHub repo size](https://img.shields.io/github/repo-size/NotShrirang/M2ConneX)


[![DB Diagram](https://img.shields.io/badge/DB%20Diagram-blue?style=for-the-badge&logo=sqlite&logoColor=white&logoSize=amd)](https://dbdiagram.io/d/MMCOE-Alumni-Portal-654ce8d57d8bbd6465dac5ae)
## Overview

M2ConneX is a comprehensive platform designed to connect alumni of MMCOE (Marathwada Mitra Mandal's College of Engineering) and facilitate communication, networking, and collaboration among them. The portal offers various features and functionalities tailored to the needs of alumni, including event management, skill sharing, job opportunities, and more. Alumni can also receive recommendations for connections, posts, and job opportunities based on their skills and experience. Built with modern web technologies and powered by Django, this portal provides a seamless and user-friendly experience for MMCOE alumni to stay connected and engaged with their alma mater.

This is backend developed for the platform.
#### Frontend - https://github.com/NotShrirang/M2ConneX-frontend

## Features

- **Social Media**: Post and share your life updates with your college.
- **Recommendations**: Receive personalized recommendations for connections, posts, and job opportunities based on your skills and experience.
- **Event Management**: Alumni can create, manage, and participate in events such as reunions, workshops, and networking sessions.
- **Skill Sharing**: A platform for alumni to share their expertise, offer mentorship, and collaborate on projects.
- **Job Opportunities**: Access to job postings, internships, and career advancement opportunities specifically curated for MMCOE alumni.
- **Networking**: Connect with fellow alumni, industry professionals, and faculty members to expand professional networks.
- **Community Engagement**: Engage in discussions, forums, and special interest groups within the MMCOE alumni community.
- **Personal Profiles**: Create and customize personal profiles showcasing professional achievements, education, and interests.

## Architecture
(Click on the image to zoom)
![m2connex](https://github.com/user-attachments/assets/591dc730-0963-4e9b-8211-d9d555fedcf0)

## Getting Started

### Prerequisites

Ensure you have Docker Desktop installed.

### Installation

1. Clone the repository:

```sh
git clone https://github.com/NotShrirang/M2ConneX-frontend.git
cd M2ConneX
```

### Database Configuration (PostgreSQL)

Create a `.env` file in the root directory with the following configurations:
```
DB_NAME = *****
DB_USER = *****
DB_PASS = *****
DB_HOST = *****
DB_PORT = *****
EMAIL = *****
EMAIL_PASSWORD = *****
TEXT_NSFW_TOKEN = *****
```


### Running the Application

#### Docker Container:

To run the application using Docker, execute the following command:

```bash
./run.sh start-dev
```

This will build and start the Docker container for the application.

#### Manual Setup:

1. Install required packages:

```bash
pip install -r requirements.txt
```

2. Migrate to the database:
```bash
python manage.py migrate
```

3. Run the backend server:
```bash
python manage.py runserver
```

## Contributing
Feel free to submit pull requests, create issues, or spread the word!

## Support
Support me by simply starring this repository! ⭐
