# Student Campus - Django Application

A Django-based web application with role-based authentication for Students and Teachers.

## Features

- **Role-Based Authentication**: Separate login for Students and Teachers
- **Custom User Model**: Extended Django user model with role field
- **Dashboards**: 
  - Student Dashboard with courses, assignments, and grades sections
  - Teacher Dashboard with class management, assignments, and grading sections
- **Bootstrap UI**: Modern, responsive design using Bootstrap 5
- **Secure Authentication**: Django's built-in authentication system

## Project Structure

```
student_campus/
├── authentication/      # User authentication and custom user model
├── students/           # Student-specific views and features
├── teachers/           # Teacher-specific views and features
├── templates/          # HTML templates
├── student_campus/     # Main project settings
└── app.py             # PDF chatbot core logic (unchanged)
```

## Setup Instructions

### 1. Database is already migrated
The database has been set up with all necessary tables.

### 2. Create a superuser (admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 3. Run the development server

```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

## URLs

- **Home/Login**: `http://127.0.0.1:8000/`
- **Sign Up**: `http://127.0.0.1:8000/auth/signup/`
- **Login**: `http://127.0.0.1:8000/auth/login/`
- **Logout**: `http://127.0.0.1:8000/auth/logout/`
- **Student Dashboard**: `http://127.0.0.1:8000/student/dashboard/`
- **Teacher Dashboard**: `http://127.0.0.1:8000/teacher/dashboard/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`

## User Roles

### Student
- Access to student dashboard
- View courses, assignments, and grades
- Cannot access teacher features

### Teacher
- Access to teacher dashboard
- Manage classes and create assignments
- Grade student submissions
- Cannot access student features

## Testing the Application

### Create Test Users

1. **Via Sign Up Page**:
   - Go to `http://127.0.0.1:8000/auth/signup/`
   - Fill in the form and select role (Student or Teacher)
   - Submit to create account

2. **Via Admin Panel**:
   - Go to `http://127.0.0.1:8000/admin/`
   - Login with superuser credentials
   - Navigate to Users → Add User
   - Create user and assign role

### Login and Test

1. Login with student account → Redirects to Student Dashboard
2. Login with teacher account → Redirects to Teacher Dashboard
3. Try accessing wrong dashboard → Shows "Permission Denied"

## Next Steps / Future Enhancements

- Integrate PDF chatbot functionality from `app.py`
- Add course management system
- Implement assignment creation and submission
- Add grading system
- Create student-teacher communication features
- Add file upload for assignments
- Implement notifications system

## Notes

- `app.py` contains the core PDF chatbot logic and remains unchanged
- You can integrate the PDF chatbot functionality into the Django app later
- All authentication is handled through Django's secure system
- Bootstrap 5 is loaded via CDN (no local installation needed)
