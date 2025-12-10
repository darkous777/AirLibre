# AirLibre

A Django-based web application for sharing and discovering activities and hobbies within your community.

## Overview

AirLibre is a social platform that enables users to create profiles, share their favorite activities, and connect with others who have similar interests. Whether you're into sports, arts, music, or any other hobby, AirLibre helps you find and engage with like-minded people.

## Features

- **User Authentication**: Secure registration and login system
- **Profile Management**: Create and customize your personal profile with avatar uploads
- **Activity Sharing**: Post and browse activities and hobbies
- **Activity Details**: View comprehensive information about each activity
- **Responsive Design**: Bootstrap-powered responsive interface

## Technology Stack

- **Backend**: Django (Python)
- **Database**: SQLite3
- **Frontend**: HTML, CSS, Bootstrap
- **Authentication**: Django built-in authentication system

## Project Structure

```
AirLibre/
├── activites/          # Activities app (models, views, templates)
├── gestionutilisateur/ # User management app
├── media/              # User-uploaded files (avatars, images)
├── static/             # CSS, JavaScript, images
├── templates/          # HTML templates
│   ├── registration/   # Login/signup pages
│   ├── profile.html    # User profile page
│   └── detail.html     # Activity detail page
└── db.sqlite3          # SQLite database
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/darkous777/AirLibre.git
cd AirLibre
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install django
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Open your browser and navigate to `http://127.0.0.1:8000`

## Usage

- Register a new account or log in with existing credentials
- Complete your profile with personal information and an avatar
- Browse activities shared by other users
- Create and share your own activities
- View detailed information about any activity

## Screenshots

_Coming soon_

## Contributing

This is a personal project, but suggestions and feedback are welcome!

## License

This project is open source and available for educational purposes.

## Author

Mohammed Amine Boumediene Blal
