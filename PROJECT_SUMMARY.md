# VidyaGuide - Project Summary & Architecture

## Project Overview

VidyaGuide is a comprehensive AI-powered web application designed to help students and young professionals with career planning and resume mentoring. The application features an easy-to-use interface combined with intelligent AI responses to provide personalized career guidance.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                              │
├─────────────────────────────────────────────────────────────────┤
│  Frontend (React + Vite + Tailwind CSS) - Port 3000              │
├─────────────────────────────────────────────────────────────────┤
│                       HTTP/REST API                              │
│                 (axios with JWT Authentication)                  │
├─────────────────────────────────────────────────────────────────┤
│  Backend (Flask + Python) - Port 5000                            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ ┌──────────────────────────────────────────────────────┐ │   │
│  │ │ Authentication (JWT)                                 │ │   │
│  │ │ - User Registration & Login                          │ │   │
│  │ │ - Token Generation & Validation                      │ │   │
│  │ └──────────────────────────────────────────────────────┘ │   │
│  │ ┌──────────────────────────────────────────────────────┐ │   │
│  │ │ Chat System                                          │ │   │
│  │ │ - Message Storage & Retrieval                        │ │   │
│  │ │ - AI Response Generation                             │ │   │
│  │ │ - Context Management                                 │ │   │
│  │ └──────────────────────────────────────────────────────┘ │   │
│  │ ┌──────────────────────────────────────────────────────┐ │   │
│  │ │ Resume Processing                                    │ │   │
│  │ │ - File Upload & Validation                           │ │   │
│  │ │ - PDF/DOC/DOCX Parsing                               │ │   │
│  │ │ - Data Extraction (Skills, Education, Experience)    │ │   │
│  │ │ - Suggestion Generation                              │ │   │
│  │ └──────────────────────────────────────────────────────┘ │   │
│  │ ┌──────────────────────────────────────────────────────┐ │   │
│  │ │ Career Guidance                                      │ │   │
│  │ │ - Career Path Definitions                            │ │   │
│  │ │ - Skill Requirements                                 │ │   │
│  │ │ - Interview & Resume Tips                            │ │   │
│  │ └──────────────────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  Database Layer (JSON-based)                                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ users.json - User accounts & profiles                   │   │
│  │ chats.json - Chat conversations per user                │   │
│  │ resumes.json - Uploaded resume metadata                 │   │
│  │ uploads/ - Resume files (PDFs, DOCs)                    │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Backend Architecture

### Core Components

#### 1. **app.py** (Main Application)
The Flask application that handles all HTTP endpoints:

```python
# Authentication Routes
POST   /api/auth/signup    → Create new user
POST   /api/auth/login     → Authenticate user
GET    /api/auth/profile   → Get user details

# Chat Routes
POST   /api/chat/message   → Send message & get AI response
GET    /api/chat/history   → Retrieve chat history
POST   /api/chat/clear     → Clear historical messages

# Resume Routes
POST   /api/resume/upload  → Upload and process resume
GET    /api/resume/get     → Get resume information
GET    /api/resume/suggestions → Get improvement tips

# Career Routes
GET    /api/career/paths          → Get career options
GET    /api/career/resume-tips    → Get resume advice
GET    /api/career/interview-tips → Get interview prep
GET    /api/career/skill-paths    → Get learning paths
```

#### 2. **config.py** (Configuration)
Centralized configuration management:
- Database paths
- File upload settings
- JWT configuration
- Environment-specific settings (Development, Production, Testing)

#### 3. **database.py** (Data Persistence)
JSON-based database operations:
- **User Management**: Create, retrieve, update users
- **Chat History**: Save and retrieve conversations
- **Resume Storage**: Store resume metadata and extracted data

```python
Database Methods:
- create_user(email, name, password_hash)
- get_user(email)
- update_user(email, data)
- save_chat_message(user_email, role, content)
- get_chat_history(user_email, limit)
- save_resume(user_email, filename, extracted_data)
- get_resume(user_email)
```

#### 4. **resume_processor.py** (Resume Analysis)
Handles resume file processing and extraction:

```python
Key Features:
- extract_text_from_pdf(pdf_path)       → Extract PDF content
- extract_text_from_docx(docx_path)     → Extract DOCX content
- extract_resume_data(resume_text)      → Parse resume information
- get_improvement_suggestions(...)       → Generate recommendations

Extracts:
- Email & Phone number
- Skills
- Education
- Work Experience
```

#### 5. **ai_assistant.py** (AI Logic)
Intelligent response generation system:

```python
CareerAIAssistant Class:
- CAREER_PATHS: Dictionary of 5+ career options
- RESUME_TIPS: Formatting, content, and structure tips
- INTERVIEW_TIPS: Interview preparation advice
- SKILL_PATHS: Learning paths for different skills

Methods:
- get_response(message, email, resume_context)
- _handle_career_guidance(message)
- _handle_resume_advice(message, resume_data)
- _handle_interview_prep(message)
- _handle_skill_development(message)
- _get_resume_feedback(resume_context)
```

### Security Features
- **JWT Authentication**: Stateless token-based authentication
- **Password Hashing**: Werkzeug security for password storage
- **CORS Configuration**: Secure cross-origin requests
- **Input Validation**: File type and size validation
- **Token Expiration**: 30-day access token expiration

### File Upload Security
- File type validation (PDF, DOC, DOCX only)
- File size limit (16MB maximum)
- Secure filename handling
- Unique file naming with timestamps

## Frontend Architecture

### Project Structure

```
src/
├── components/
│   ├── CareerGuidancePanel.jsx   → Career paths display
│   ├── ProtectedRoute.jsx         → Route authentication wrapper
│   └── ResumeUploadModal.jsx      → Resume upload interface
│
├── context/
│   └── AuthContext.jsx            → Global authentication state
│
├── pages/
│   ├── Login.jsx                  → Login page
│   ├── Signup.jsx                 → Registration page
│   └── Dashboard.jsx              → Main application dashboard
│
├── services/
│   └── api.js                     → API client & endpoints
│
├── App.jsx                        → Main app component with routing
├── main.jsx                       → React entry point
└── index.css                      → Global styles (Tailwind)
```

### Key Components

#### 1. **AuthContext.jsx** (State Management)
Manages authentication state globally:
```javascript
useAuth() Hook provides:
- user: Current user object
- token: JWT access token
- isAuthenticated: Boolean auth status
- loading: Loading state
- signup(email, name, password): Registration
- login(email, password): Authentication
- logout(): Cleanup
```

#### 2. **Login.jsx & Signup.jsx** (Authentication Pages)
- Email and password validation
- Error handling and display
- Form submission with loading states
- Links between login and signup

#### 3. **Dashboard.jsx** (Main Application)
The core interface with multiple panels:

**Chat Panel:**
- Real-time message display
- User input with send button
- Auto-scrolling to latest message
- Welcome screen with quick suggestions
- Loading indicators

**Career Panel:**
- Interactive career cards
- Expandable career details
- Skills and education badges
- Learning resources

**Tips Panel:**
- Formatting guidelines
- Content improvement tips
- Resume structure guide
- Job search strategies

**Sidebar:**
- Navigation between panels
- Resume upload trigger
- Resume status display
- User profile info
- Logout button

#### 4. **API Service** (api.js)
Centralized API communication:
```javascript
apiInstance: Axios with:
  - JWT token injection
  - Error handling (401 redirects to login)
  - Error response mapping

API Functions:
- authAPI: signup, login, getProfile
- chatAPI: sendMessage, getHistory, clearHistory
- resumeAPI: upload, getResume, getSuggestions
- careerAPI: getPaths, getTips, getSkillPaths
```

### UI/UX Features
- **Responsive Design**: Mobile-first approach with Tailwind
- **Color Scheme**: Blue (primary), Green (secondary), Amber (accent)
- **Icons**: Lucide React icons for visual clarity
- **Loading States**: Spinners and animations for better UX
- **Error Messages**: Clear, user-friendly error displays
- **Accessibility**: Semantic HTML and ARIA labels

### State Management Flow
```
User Action
    ↓
React Component
    ↓
useAuth() or useState()
    ↓
API Service (axios)
    ↓
Backend (Flask)
    ↓
Database (JSON)
    ↓
Response
    ↓
Update State
    ↓
Re-render UI
```

## Data Flow Examples

### Login Flow
1. User enters email & password
2. Frontend calls `authAPI.login()`
3. Backend validates credentials
4. JWT token generated and returned
5. Token stored in localStorage
6. AuthContext updated
7. User redirected to dashboard
8. Token injected in subsequent API calls

### Chat Flow
1. User types message and sends
2. Message displayed immediately
3. API call sent with message
4. AI routes to appropriate handler
5. AI generates response based on intent
6. Messages saved in JSON database
7. Response returned to frontend
8. Both messages displayed in chat

### Resume Upload Flow
1. User selects resume file
2. Client-side validation (type, size)
3. File uploaded via multipart/form-data
4. Backend saves file to /uploads
5. File parsed (PDF/DOCX)
6. Text extracted and analyzed
7. Key data extracted (skills, education, etc.)
8. Improvement suggestions generated
9. Metadata saved to database
10. User receives feedback with suggestions

## Technology Decisions

### Why Flask?
- Lightweight and flexible
- Easy to learn and customize
- Great ecosystem for REST APIs
- Simple JWT integration
- Good for quick prototyping

### Why React?
- Component-based architecture
- Excellent for building interactive UIs
- Large ecosystem and community support
- Great developer tools and debugging

### Why Tailwind CSS?
- Utility-first approach
- No need to write custom CSS
- Responsive design made easy
- Large component library
- Great for rapid development

### Why JSON Database?
- No database setup required
- Easy to understand and debug
- Fast for development
- Can be easily migrated to SQL later

## Scalability Considerations

### Current Limitations
- JSON-based database (scales to ~10k users)
- Single process server
- No caching mechanism
- No database indexing

### Future Improvements
1. **Database Migration**
   - PostgreSQL or MongoDB
   - Proper indexing for faster queries
   - Connection pooling

2. **Backend Scaling**
   - Gunicorn/uWSGI for production
   - Load balancing
   - Redis for caching and sessions
   - Celery for async tasks

3. **Frontend Optimization**
   - Code splitting
   - Lazy loading
   - Service workers
   - PWA capabilities

4. **AI Enhancement**
   - OpenAI API integration
   - Machine learning models
   - Natural language processing
   - Context awareness

## Security Considerations

### Current Implementation
- JWT-based authentication
- Password hashing with Werkzeug
- CORS security headers
- Input validation

### Production Recommendations
- HTTPS/SSL enforcement
- Rate limiting
- CSRF protection
- SQL injection prevention (when using DB)
- XSS protection
- Secure headers (CSP, X-Frame-Options)
- Regular security audits

## Performance Metrics

### Optimization Strategies
1. **Frontend**
   - Gzip compression
   - Code splitting
   - Image optimization
   - Lazy loading

2. **Backend**
   - Response caching
   - Database query optimization
   - Connection pooling
   - File compression

3. **Network**
   - CDN for static assets
   - API response pagination
   - WebSocket for real-time chat

## Testing Strategy

### Recommended Tests
1. **Unit Tests**
   - Component rendering
   - AI response logic
   - Resume parsing

2. **Integration Tests**
   - API endpoints
   - Authentication flow
   - File upload process

3. **E2E Tests**
   - Complete user journeys
   - Chat functionality
   - Resume upload and analysis

## Deployment Checklist

- [ ] Environment variables configured
- [ ] Database setup (PostgreSQL/MySQL)
- [ ] SSL certificates installed
- [ ] CORS configured for production domain
- [ ] Logging and monitoring setup
- [ ] Backups configured
- [ ] Load balancer setup
- [ ] CDN configuration
- [ ] Security headers configured
- [ ] Rate limiting implemented
- [ ] Monitoring alerts setup
- [ ] Disaster recovery plan

## Future Feature Roadmap

### Phase 1 (Quick Wins)
- [ ] Email notifications
- [ ] Password reset functionality
- [ ] User profile customization
- [ ] Resume template download

### Phase 2 (Enhancement)
- [ ] OpenAI API integration
- [ ] Video interview simulator
- [ ] LinkedIn profile analysis
- [ ] Job recommendation engine

### Phase 3 (Advanced)
- [ ] Advanced analytics dashboard
- [ ] Peer matching for networking
- [ ] Certification tracking
- [ ] Mobile native app

### Phase 4 (Enterprise)
- [ ] Organization/university features
- [ ] Admin dashboard
- [ ] Advanced reporting
- [ ] API for third-party integrations

## Conclusion

VidyaGuide is a well-structured, modern web application that successfully combines:
- **Frontend Excellence**: Responsive, intuitive React interface
- **Backend Robustness**: Flexible Flask API with proper security
- **Data Management**: JSON storage with easy migration path
- **AI Integration**: Rule-based AI responses with personalization

The architecture is designed for easy maintenance, scalability, and future enhancements. The separation of concerns between frontend and backend allows for independent development and deployment.

---

**Project Status**: ✅ Complete and Ready for Deployment

**Last Updated**: February 6, 2026
