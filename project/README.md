# Exam System - Full Stack Application

A complete exam-taking system built with Django REST API backend and React frontend, featuring JWT authentication, timed exams, and automatic scoring.

## Features

### Student Features
- User registration and login with JWT authentication
- Dashboard showing available exams
- Exam interface with:
  - Randomized multiple choice questions
  - 30-minute countdown timer with auto-submit
  - Next/Previous question navigation
  - Question overview grid
  - Progress tracking
- Automatic score calculation
- Detailed results page with performance analysis

### Technical Features
- Django REST API with JWT authentication
- React frontend with Redux state management
- Responsive design for all devices
- Real-time timer with auto-submit
- Secure API endpoints
- Clean, professional UI

## Technology Stack

### Frontend
- React 18 with TypeScript
- Redux Toolkit for state management
- React Router for navigation
- Axios for API calls
- Tailwind CSS for styling
- Lucide React for icons

### Backend
- Django 4.2
- Django REST Framework
- Simple JWT for authentication
- PostgreSQL/SQLite database
- CORS headers for cross-origin requests

## Setup Instructions

### Backend Setup

1. **Create a virtual environment:**
   ```bash
   cd backend
   python -m venv exam_env
   source exam_env/bin/activate  # On Windows: exam_env\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the backend directory:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

4. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

The Django API will be available at `http://localhost:8000`

### Frontend Setup

The React application is already running in this environment. To run locally:

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```

The React app will be available at `http://localhost:5173`

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `GET /api/auth/profile/` - Get user profile
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Exams
- `GET /api/exams/available/` - Get available exams
- `POST /api/exams/{id}/start/` - Start an exam session
- `GET /api/exams/session/{session_id}/questions/` - Get exam questions
- `POST /api/exams/session/{session_id}/answer/` - Submit an answer
- `POST /api/exams/session/{session_id}/submit/` - Submit complete exam
- `GET /api/exams/session/{session_id}/result/` - Get exam results
- `GET /api/exams/history/` - Get user's exam history

## Sample Data

To add sample exams and questions, use the Django admin interface:

1. Go to `http://localhost:8000/admin`
2. Login with your superuser credentials
3. Add Exams, Questions, and Choices

### Sample Exam Structure:
```
Exam: "JavaScript Fundamentals"
- Duration: 30 minutes
- Total Questions: 10
- Difficulty: Medium

Questions:
1. "What is the correct way to declare a variable in JavaScript?"
   a) var myVar; (correct)
   b) variable myVar;
   c) declare myVar;
   d) new myVar;

2. "Which of the following is not a primitive data type in JavaScript?"
   a) string
   b) number
   c) boolean
   d) object (correct)
```

## Testing the API

### Using curl:

1. **Register a user:**
   ```bash
   curl -X POST http://localhost:8000/api/auth/register/ \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "email": "test@example.com",
       "first_name": "Test",
       "last_name": "User",
       "password": "testpass123",
       "password_confirm": "testpass123"
     }'
   ```

2. **Login:**
   ```bash
   curl -X POST http://localhost:8000/api/auth/login/ \
     -H "Content-Type: application/json" \
     -d '{
       "email": "test@example.com",
       "password": "testpass123"
     }'
   ```

3. **Get available exams:**
   ```bash
   curl -X GET http://localhost:8000/api/exams/available/ \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
   ```

## Project Structure

```
├── backend/
│   ├── exam_system/          # Django project settings
│   ├── accounts/             # User authentication app
│   ├── exams/               # Exam management app
│   ├── manage.py
│   └── requirements.txt
├── src/
│   ├── components/
│   │   ├── auth/            # Login/Register components
│   │   └── exam/            # Exam-related components
│   ├── store/               # Redux store and slices
│   ├── services/            # API service layer
│   └── App.tsx
└── README.md
```

## Security Features

- JWT-based authentication
- Password validation
- CORS configuration
- Protected API endpoints
- Secure session management
- Input validation and sanitization

## Future Enhancements

- Question categories and tags
- Exam scheduling
- Performance analytics
- Multi-language support
- Offline exam capability
- Advanced question types (drag-drop, fill-in-the-blank)

## License

This project is created for educational purposes and assessment requirements.