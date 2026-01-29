# Mental Health Tracker

A Django-based web application designed to help users track their mental health journey, manage daily mood entries, and access helpful mental health resources.

## Project Purpose

This Full-Stack application provides a centrally-owned dataset for mental health tracking, with authentication mechanisms and role-based access control. Users can privately log their daily mental health status, while administrators can manage educational resources and support materials.

## Target Audience

- Individuals managing mental health conditions (ADHD, depression, anxiety)
- People seeking to track their emotional wellbeing
- Mental health support organizations

## Key Features

### For Registered Users
- **Daily Mood Tracking**: Log daily mood scores with optional notes
- **Mood History**: View personal mood trends over time
- **Resource Library**: Access curated mental health resources and support information
- **Secure & Private**: All personal data is protected and private to each user

### For Administrators
- **Resource Management**: Add, edit, and remove mental health resources
- **Content Moderation**: Manage educational materials and support links
- **User Overview**: Access to general platform statistics

## Technologies Used

- **Backend**: Python 3.12, Django 6.0
- **Database**: PostgreSQL (production) / SQLite (development)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: Django built-in authentication system
- **Version Control**: Git & GitHub
- **Deployment**: (TBD - Heroku/Railway)

## Project Status

🚧 **In Development** - Portfolio Project 4 for Code Institute Full Stack Developer Diploma

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- virtualenv

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/oliveiracle/mental-health-tracker.git
cd mental-health-tracker
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run development server:
```bash
python manage.py runserver
```

7. Access the application at `http://127.0.0.1:8000`

## User Stories & Agile Methodology

This project follows Agile development practices. User stories and project planning are managed using GitHub Projects.

[Link to GitHub Project Board - To be added]

## Testing

Comprehensive testing documentation will be provided in the TESTING.md file.

## Deployment

Deployment instructions will be documented here once the application is ready for production.

## Credits & Acknowledgements

- Code Institute for project requirements and guidance
- Django Documentation
- Bootstrap Documentation

## License

This project is created for educational purposes as part of the Code Institute Full Stack Developer Diploma.

## Author

Cleino de Oliveira
- GitHub: [@oliveiracle](https://github.com/oliveiracle)
- Project Repository: [mental-health-tracker](https://github.com/oliveiracle/mental-health-tracker)

---

**Note**: This is a student project and should not be used as a substitute for professional mental health support. If you're experiencing a mental health crisis, please contact emergency services or a mental health professional.
