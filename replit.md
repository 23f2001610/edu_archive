# Academic Resource Portal

## Overview
A Flask-based web application for accessing college academic resources including course notes and previous year question papers. Features a student-facing portal for browsing/downloading resources and an admin panel for managing content.

## Project Structure
```
├── app.py              # Flask app initialization and configuration
├── main.py             # Entry point
├── models.py           # SQLAlchemy database models
├── routes.py           # All application routes
├── forms.py            # WTForms form definitions
├── init_admin.py       # Admin user initialization script
├── templates/          # Jinja2 HTML templates
│   ├── base.html       # Base layout
│   ├── index.html      # Home page
│   ├── notes.html      # Notes browsing
│   ├── question_papers.html  # Question papers with filtering
│   ├── login.html      # Admin login
│   └── admin/          # Admin panel templates
├── static/css/         # Stylesheets
└── uploads/            # Uploaded files storage
```

## Database Models
- **Admin**: Admin users with username/password authentication
- **Course**: Academic courses (e.g., Computer Science, Electronics)
- **Subject**: Subjects under courses with semester info
- **Note**: Uploaded study notes linked to subjects
- **QuestionPaper**: Previous year exam papers with year/semester/exam type

## Features
### Student Portal
- Browse courses and subjects
- View and download notes organized by course/subject
- Filter question papers by semester and year
- Download PDF/document files

### Admin Panel
- Secure login authentication
- CRUD operations for courses, subjects, notes, question papers
- File upload management (PDF, DOC, DOCX, PPT, PPTX, TXT)
- Dashboard with statistics

## Admin Access
Run `python init_admin.py` to create admin account. Password is auto-generated securely or can be set via `ADMIN_PASSWORD` environment variable.

## Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `SESSION_SECRET`: Flask session secret key
- `ADMIN_PASSWORD` (optional): Custom admin password

## Running the Application
The application runs on port 5000 using gunicorn:
```bash
gunicorn --bind 0.0.0.0:5000 --reload main:app
```

## Recent Changes
- December 2024: Initial implementation with full CRUD functionality
- Secure admin password generation (no hard-coded credentials)
