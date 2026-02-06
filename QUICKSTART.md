# VidyaGuide - Quick Start Guide

Get VidyaGuide running in 5 minutes! 🚀

## Prerequisites
- Python 3.8+ installed
- Node.js 16+ installed
- Two terminal windows open

## Quick Start

### Terminal 1: Backend (Flask)

```bash
# Navigate to backend
cd "c:\VidyaGuide-AI Agent\backend"

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create required directories
mkdir data uploads

# Run the server
python app.py
```

**Expected output:**
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

✅ Backend is running on `http://localhost:5000`

---

### Terminal 2: Frontend (React)

```bash
# Navigate to frontend
cd "c:\VidyaGuide-AI Agent\frontend"

# Install dependencies
npm install

# Start development server
npm run dev
```

**Expected output:**
```
VITE v4.x.x ready in xxx ms

➜  Local: http://localhost:3000
```

✅ Frontend is running on `http://localhost:3000`

---

## Access the Application

1. Open your browser
2. Go to: **http://localhost:3000**
3. Sign up with a test account
4. Start using VidyaGuide!

---

## Test the Features

### 1. Chat with AI
- Send: "Tell me about career paths"
- Receive: AI response about careers

### 2. Upload Resume
- Click "Upload Resume" button
- Select a PDF, DOC, or DOCX file
- Get instant feedback and suggestions

### 3. Explore Career Paths
- Click "Career Paths" button in sidebar
- Expand careers to see details

### 4. Read Resume Tips
- Click "Resume Tips" button
- Get formatting and content advice

---

## File Structure
```
VidyaGuide-AI Agent/
├── backend/         → Flask API server
│   ├── app.py      → Main application
│   └── ...other files
├── frontend/        → React UI
│   ├── src/        → React components
│   └── ...config files
└── README.md       → Full documentation
```

---

## Troubleshooting

### Backend won't start?
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt

# Check if port 5000 is available
netstat -ano | findstr :5000
```

### Frontend won't load?
```bash
# Check Node version
node --version  # Should be 16+

# Reinstall dependencies
npm cache clean --force
npm install

# Check if port 3000 is available
netstat -ano | findstr :3000
```

### Can't connect to backend?
- Make sure both servers are running in separate terminals
- Check if API URL in frontend is correct: `http://localhost:5000/api`
- Check browser console for errors (F12)

---

## Common Commands

### Start Development
```bash
# Terminal 1 - Backend
cd backend && .\venv\Scripts\Activate.ps1 && python app.py

# Terminal 2 - Frontend
cd frontend && npm run dev
```

### Stop Servers
```bash
# Terminal 1: Ctrl+C
# Terminal 2: Ctrl+C
```

### Rebuild Frontend
```bash
cd frontend
npm run build
npm run preview
```

### Check Backend Health
```bash
# In a new terminal:
curl http://localhost:5000/api/health
```

---

## Example Test Credentials

When signing up, you can use:
- **Name**: John Doe
- **Email**: john@example.com
- **Password**: Test123456

---

## Documentation

- **Full Setup Guide**: See `SETUP_GUIDE.md`
- **Project Overview**: See `PROJECT_SUMMARY.md`
- **Complete README**: See `README.md`

---

## Next Steps

1. ✅ Get it running (This guide)
2. 📚 Read the documentation
3. 🧪 Test all features
4. 🎨 Customize UI/styling
5. 🔧 Modify AI responses in `backend/ai_assistant.py`
6. 🚀 Deploy to production

---

## API Quick Reference

### Chat
```bash
POST /api/chat/message
{
  "message": "Tell me about careers"
}
# Response: AI generated answer
```

### Resume
```bash
POST /api/resume/upload
# Form data with file

GET /api/resume/suggestions
# Response: Improvement suggestions
```

### Career Paths
```bash
GET /api/career/paths
# Response: All available careers with details
```

---

## Tips

💡 **For Development**:
- Keep both terminals visible
- Use VS Code or your favorite IDE
- Check browser console (F12) for frontend errors
- Check terminal output for backend errors

💡 **For Testing**:
- Try different resume files
- Test various chat prompts
- Check all career path cards
- Verify error handling

💡 **For Customization**:
- Edit AI responses in `backend/ai_assistant.py`
- Modify styles in `frontend/src/index.css`
- Add new features in components
- Customize career paths and tips

---

## Need Help?

1. Check `SETUP_GUIDE.md` for detailed instructions
2. Review `PROJECT_SUMMARY.md` for architecture
3. Check browser console (F12) for errors
4. Check backend terminal for server errors
5. Refer to README.md for full documentation

---

**Enjoy VidyaGuide! Happy Career Planning! 🎉**

Questions? Check the documentation files in the project root!
