# VidyaGuide - Complete Setup Guide

This guide will walk you through setting up and running the VidyaGuide application on your system.

## Prerequisites & System Requirements

Before you begin, ensure you have the following installed:

### Required Software
1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - Verify installation: `python --version`

2. **Node.js 16+ and npm**
   - Download from: https://nodejs.org/
   - Verify installation: `node --version` and `npm --version`

3. **Git** (optional, for version control)
   - Download from: https://git-scm.com/

## Step-by-Step Setup Instructions

### Part 1: Backend Setup (Flask/Python)

#### Step 1: Navigate to Backend Directory
```bash
cd "c:\VidyaGuide-AI Agent\backend"
```

#### Step 2: Create Python Virtual Environment
```bash
python -m venv venv
```

#### Step 3: Activate Virtual Environment

**On Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```bash
venv\Scripts\activate.bat
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt after activation.

#### Step 4: Install Python Dependencies
```bash
pip install -r requirements.txt
```

This will install all required packages:
- Flask 2.3.3
- Flask-CORS 4.0.0
- Flask-JWT-Extended 4.5.2
- PyPDF2 3.0.1
- python-docx 0.8.11
- And other dependencies

#### Step 5: Create Required Directories
```bash
mkdir data
mkdir uploads
```

#### Step 6: Verify Backend Configuration
Check that `.env` file exists in the backend directory with:
```
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=jwt-secret-key-change-in-production
FLASK_ENV=development
FLASK_DEBUG=True
```

#### Step 7: Run the Backend Server
```bash
python app.py
```

You should see output like:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

The backend is now running! Leave this terminal open.

---

### Part 2: Frontend Setup (React/Node.js)

#### Step 1: Open a New Terminal/PowerShell Window

Keep the backend running in the first terminal.

#### Step 2: Navigate to Frontend Directory
```bash
cd "c:\VidyaGuide-AI Agent\frontend"
```

#### Step 3: Install Node Dependencies
```bash
npm install
```

This will install all required packages listed in `package.json`:
- React 18.2.0
- React Router DOM 6.15.0
- Axios 1.5.0
- Tailwind CSS 3.3.0
- And other dependencies

This may take a few minutes.

#### Step 4: Verify Configuration Files
Check that these files exist:
- `package.json` - Node package configuration
- `vite.config.js` - Vite build configuration
- `tailwind.config.js` - Tailwind CSS configuration
- `.env` - Environment variables

The `.env` file should contain:
```
REACT_APP_API_URL=http://localhost:5000/api
```

#### Step 5: Start the Development Server
```bash
npm run dev
```

You should see output like:
```
  VITE v4.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5000
  ➜  press h to show help
```

---

## Accessing the Application

Once both servers are running:

1. **Open your web browser** and navigate to: `http://localhost:3000`

2. **You should see the VidyaGuide login page**

3. **Create an account:**
   - Click "Sign up here"
   - Enter your name, email, and password
   - Click "Sign Up"

4. **Login:**
   - Enter your email and password
   - Click "Login"

5. **Start using the application:**
   - Chat with the AI mentor
   - Upload your resume
   - Explore career paths
   - Read resume tips

---

## Troubleshooting Guide

### Backend Issues

#### Python not found
```bash
# Verify Python is installed
python --version

# If not installed, download from https://www.python.org/downloads/
```

#### Virtual environment not activating
```bash
# Try alternative activation method
.\venv\Scripts\activate.bat

# Or on PowerShell with execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

#### Pip packages won't install
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Then install requirements
pip install -r requirements.txt
```

#### Port 5000 already in use
```bash
# Find what's using port 5000 (Windows)
netstat -ano | findstr :5000

# Kill the process or change port in app.py:
# app.run(debug=True, host='0.0.0.0', port=5001)
```

### Frontend Issues

#### Node/npm not found
```bash
# Verify installation
node --version
npm --version

# If not installed, download from https://nodejs.org/
```

#### Dependencies won't install
```bash
# Clear npm cache and reinstall
npm cache clean --force
rm -r node_modules
npm install
```

#### Port 3000 already in use
```bash
# The app will suggest an alternative port, or you can:
# Update vite.config.js server.port to a different port
```

#### Build/Compilation errors
```bash
# Clear cache and rebuild
npm cache clean --force
rm -r dist
npm run build
```

### Connection Issues

#### Frontend can't connect to backend
1. **Verify backend is running** - Check terminal shows Flask running on :5000
2. **Check API URL** - In `frontend/src/services/api.js`:
   ```javascript
   const API_BASE_URL = 'http://localhost:5000/api';
   ```
3. **Check CORS** - Backend should have CORS enabled
4. **Browser console** - Open DevTools (F12) to see exact error

### Resume Upload Issues

#### File upload not working
1. Check file format - must be PDF, DOC, or DOCX
2. Check file size - must be under 16MB
3. Check `backend/uploads/` directory exists and is writable
4. Check Python dependencies: `pip install PyPDF2 python-docx`

---

## Development Commands

### Backend
```bash
# Activate virtual environment (if not already active)
venv\Scripts\activate

# Run the server
python app.py

# Deactivate virtual environment
deactivate
```

### Frontend
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code (if configured)
npm run lint
```

---

## Project Structure Check

Before starting, verify you have these files:

**Backend:**
```
backend/
├── app.py ✓
├── config.py ✓
├── database.py ✓
├── resume_processor.py ✓
├── ai_assistant.py ✓
├── requirements.txt ✓
├── .env ✓
└── .gitignore ✓
```

**Frontend:**
```
frontend/
├── src/
│   ├── components/
│   │   ├── ProtectedRoute.jsx ✓
│   │   ├── ResumeUploadModal.jsx ✓
│   │   └── CareerGuidancePanel.jsx ✓
│   ├── context/
│   │   └── AuthContext.jsx ✓
│   ├── pages/
│   │   ├── Login.jsx ✓
│   │   ├── Signup.jsx ✓
│   │   └── Dashboard.jsx ✓
│   ├── services/
│   │   └── api.js ✓
│   ├── App.jsx ✓
│   ├── main.jsx ✓
│   └── index.css ✓
├── index.html ✓
├── package.json ✓
├── vite.config.js ✓
├── tailwind.config.js ✓
├── postcss.config.js ✓
├── .env ✓
└── .gitignore ✓
```

---

## Testing the Application

### 1. Test User Registration
- Go to landing page
- Click "Sign up"
- Enter test details
- Verify account is created

### 2. Test Login
- Use credentials from sign up
- Verify successful login

### 3. Test Chat
- Send a message: "Tell me about career paths"
- Verify AI response appears

### 4. Test Resume Upload
- Click "Upload Resume"
- Select a PDF/DOC/DOCX file
- Verify upload succeeds and suggestions appear

### 5. Test Career Paths Panel
- Click "Career Paths"
- Expand a career
- Verify information displays correctly

### 6. Test Resume Tips
- Click "Resume Tips"
- Verify tips are displayed

---

## Production Deployment

For deploying to production:

1. **Backend:**
   - Use a production WSGI server (Gunicorn, uWSGI)
   - Set up environment variables securely
   - Use a database (PostgreSQL, MySQL)
   - Enable HTTPS

2. **Frontend:**
   - Build production bundle: `npm run build`
   - Deploy `dist/` directory to CDN or static host
   - Configure API endpoints for production

3. **Database:**
   - Migrate from JSON to SQL database
   - Set up proper backups and recovery

---

## Getting Help

If you encounter issues:

1. **Check the troubleshooting section** above
2. **Read error messages carefully** - they often indicate the exact problem
3. **Check browser console** (F12) for frontend errors
4. **Check terminal output** for backend errors
5. **Verify all prerequisites** are installed correctly

---

## Next Steps

Once everything is running:

1. **Customize the AI responses** in `backend/ai_assistant.py`
2. **Add more resume tips** in `backend/ai_assistant.py`
3. **Connect to OpenAI API** for more advanced AI responses
4. **Deploy to cloud** (AWS, Azure, Heroku, etc.)
5. **Add more features** (video interviews, certifications, etc.)

---

## Useful Resources

- Flask Documentation: https://flask.palletsprojects.com/
- React Documentation: https://react.dev/
- Tailwind CSS: https://tailwindcss.com/
- Vite Documentation: https://vitejs.dev/
- JWT Authentication: https://flask-jwt-extended.readthedocs.io/

---

**Enjoy using VidyaGuide! Your personal AI career mentor! 🚀**
