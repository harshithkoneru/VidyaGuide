# VidyaGuide - AI Agent for Career Planning & Resume Mentoring

VidyaGuide is an intelligent, user-friendly web application that acts as a personal career mentor and resume advisor. It helps students and young professionals with career guidance, resume improvement, and interview preparation through an AI-powered chatbot interface.

## Features

### ✨ Core Features
- **AI Chatbot**: Ask any career-related or resume-related questions and get intelligent responses
- **Resume Upload & Analysis**: Upload resumes (PDF, DOC, DOCX) for automated analysis and improvement suggestions
- **Career Guidance**: Explore different career paths, required skills, and educational requirements
- **Interview Preparation**: Get tips and guidance for interview preparation
- **Skill Development**: Learn about skill development paths for different careers
- **Chat History**: View and manage your conversation history with the AI mentor

### 🎨 User Interface
- Clean, modern, and student-friendly design
- Mobile-responsive interface
- Intuitive navigation with multiple content panels
- Professional color scheme with calm, approachable tones

### 🔐 Authentication
- Secure user registration and login
- JWT-based authentication
- User profile management
- Per-user chat history and resume data

## Project Structure

```
VidyaGuide-AI Agent/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration settings
│   ├── database.py            # JSON-based database operations
│   ├── resume_processor.py    # Resume parsing and analysis
│   ├── ai_assistant.py        # AI response generation
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables
│   └── .gitignore
│
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── context/           # React context (Auth)
│   │   ├── pages/             # Page components
│   │   ├── services/          # API service
│   │   ├── App.jsx            # Main App component
│   │   ├── main.jsx           # React entry point
│   │   └── index.css          # Global styles
│   ├── index.html             # HTML entry point
│   ├── package.json           # Node dependencies
│   ├── vite.config.js         # Vite configuration
│   ├── tailwind.config.js     # Tailwind CSS configuration
│   ├── postcss.config.js      # PostCSS configuration
│   └── .gitignore
│
└── README.md                  # This file
```

## Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Authentication**: Flask-JWT-Extended
- **File Handling**: PyPDF2, python-docx
- **CORS**: Flask-CORS
- **Database**: JSON-based (can be upgraded to SQL)

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Routing**: React Router DOM

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+ and npm
- pip (Python package manager)

### Backend Setup

1. **Navigate to the backend directory**
   ```bash
   cd "c:\VidyaGuide-AI Agent\backend"
   ```

2. **Create a Python virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create necessary directories**
   ```bash
   mkdir data uploads
   ```

6. **Run the Flask app**
   ```bash
   python app.py
   ```
   The backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to the frontend directory**
   ```bash
   cd "c:\VidyaGuide-AI Agent\frontend"
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:3000`

4. **Build for production**
   ```bash
   npm run build
   ```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register a new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile` - Get user profile (requires JWT)

### Chat
- `POST /api/chat/message` - Send a message to the AI (requires JWT)
- `GET /api/chat/history` - Get chat history (requires JWT)
- `POST /api/chat/clear` - Clear chat history (requires JWT)

### Resume
- `POST /api/resume/upload` - Upload resume (requires JWT)
- `GET /api/resume/get` - Get resume information (requires JWT)
- `GET /api/resume/suggestions` - Get resume improvement suggestions (requires JWT)

### Career Guidance
- `GET /api/career/paths` - Get available career paths
- `GET /api/career/resume-tips` - Get resume tips
- `GET /api/career/interview-tips` - Get interview tips
- `GET /api/career/skill-paths` - Get skill development paths

### Health
- `GET /api/health` - Health check endpoint

## Usage

### For Users

1. **Sign Up**: Create an account with your name and email
2. **Login**: Access your personalized dashboard
3. **Chat with AI**: Ask any career-related questions
4. **Upload Resume**: Upload your resume for automated analysis
5. **Explore Career Paths**: Browse different career options
6. **Read Tips**: Learn resume and interview preparation tips

### Example Questions to Ask the AI
- "Tell me about different career paths"
- "How do I improve my resume?"
- "What are the skills I need to become a software engineer?"
- "How do I prepare for a job interview?"
- "What certifications should I consider?"

## Features in Detail

### AI Chatbot
The AI assistant can respond to questions about:
- Career paths and job market
- Resume writing and improvements
- Interview preparation
- Skill development and learning paths
- General career guidance

### Resume Analysis
When you upload a resume, the system will:
- Extract key information (skills, education, experience)
- Provide formatting suggestions
- Suggest content improvements
- Recommend keywords to add
- Identify missing sections

### Career Paths
Explore 5+ major career paths including:
- Software Engineer
- Data Scientist
- Product Manager
- UX/UI Designer
- Marketing Manager

Each path includes:
- Job description
- Required skills
- Educational background
- Career development tips

## File Formats Supported

Resumes can be uploaded in the following formats:
- **PDF** (.pdf)
- **Microsoft Word** (.docx, .doc)

Maximum file size: 16MB

## Environment Variables

Create a `.env` file in the backend directory with:
```
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=jwt-secret-key-change-in-production
FLASK_ENV=development
FLASK_DEBUG=True
```

## Data Storage

The application uses a JSON-based database system for easy setup and development. For production, consider upgrading to:
- PostgreSQL
- MySQL
- MongoDB

The data is stored in the `backend/data` directory.

## Future Enhancements

- Integration with OpenAI API for more sophisticated AI responses
- SQL database instead of JSON
- Email notifications
- LinkedIn integration
- Video interview preparation
- Resume template downloads
- Advanced analytics and insights
- Mobile app

## Troubleshooting

### Backend won't start
- Ensure Python is installed: `python --version`
- Check if port 5000 is available
- Verify all dependencies are installed: `pip install -r requirements.txt`

### Frontend won't load
- Ensure Node.js is installed: `node --version`
- Clear node_modules and reinstall: `rm -r node_modules && npm install`
- Check if port 3000 is available

### API connection issues
- Ensure backend is running on http://localhost:5000
- Check CORS configuration in `backend/app.py`
- Verify the API base URL in `frontend/src/services/api.js`

### Resume upload fails
- Check file format (PDF, DOC, or DOCX only)
- Ensure file size is under 16MB
- Check backend `uploads/` directory has write permissions

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support and questions, please refer to the documentation or contact the development team.

## Acknowledgments

- Built with React, Flask, and Tailwind CSS
- Icons from Lucide React
- Inspired by modern career coaching platforms

---

**Happy Career Planning with VidyaGuide! 🚀**
