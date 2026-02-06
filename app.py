from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime

from config import DevelopmentConfig
from database import Database
from resume_processor import ResumeProcessor
from ai_assistant import CareerAIAssistant

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize JWT
jwt = JWTManager(app)

# Initialize database
db = Database(app.config['DATABASE_PATH'])

# Initialize AI Assistant
ai_assistant = CareerAIAssistant()

# Create upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# ==================== Authentication Routes ====================

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    """User signup endpoint"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('name') or not data.get('password'):
        return jsonify({'error': 'Missing required fields: email, name, password'}), 400
    
    email = data['email'].strip().lower()
    name = data['name'].strip()
    password = data['password']
    
    # Validate email format
    if '@' not in email or '.' not in email:
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Check if user already exists
    if db.get_user(email):
        return jsonify({'error': 'Email already registered'}), 400
    
    # Hash password and create user
    password_hash = generate_password_hash(password)
    if db.create_user(email, name, password_hash):
        # Create access token
        access_token = create_access_token(identity=email)
        return jsonify({
            'message': 'Signup successful',
            'access_token': access_token,
            'user': {
                'email': email,
                'name': name
            }
        }), 201
    
    return jsonify({'error': 'Error creating user'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint - simplified with just email and name"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('name'):
        return jsonify({'error': 'Missing email or name'}), 400
    
    email = data['email'].strip().lower()
    name = data['name'].strip()
    
    # Validate email format
    if '@' not in email or '.' not in email:
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Get or create user
    user = db.get_user(email)
    if not user:
        # Create new user if doesn't exist
        db.create_user(email, name, '')
        user = db.get_user(email)
    
    # Create access token
    access_token = create_access_token(identity=email)
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': {
            'email': user['email'],
            'name': user['name']
        }
    }), 200

@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    email = get_jwt_identity()
    user = db.get_user(email)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Don't expose password hash
    user_data = {
        'email': user['email'],
        'name': user['name'],
        'has_resume': user.get('resume') is not None,
        'created_at': user.get('created_at')
    }
    
    return jsonify(user_data), 200

# ==================== Chat Routes ====================

@app.route('/api/chat/message', methods=['POST'])
@jwt_required()
def chat_message():
    """Send a chat message and get AI response"""
    email = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('message'):
        return jsonify({'error': 'Message is required'}), 400
    
    user_message = data['message'].strip()
    
    # Get user's resume context if available
    resume_context = db.get_resume(email)
    
    # Save user message
    db.save_chat_message(email, 'user', user_message, resume_context=resume_context['filename'] if resume_context else None)
    
    # Get AI response
    ai_response = ai_assistant.get_response(user_message, email, resume_context)
    
    # Save AI response
    db.save_chat_message(email, 'assistant', ai_response['content'])
    
    return jsonify(ai_response), 200

@app.route('/api/chat/history', methods=['GET'])
@jwt_required()
def get_chat_history():
    """Get chat history for current user"""
    email = get_jwt_identity()
    limit = request.args.get('limit', default=50, type=int)
    
    messages = db.get_chat_history(email, limit=limit)
    
    return jsonify({
        'messages': messages,
        'count': len(messages)
    }), 200

@app.route('/api/chat/clear', methods=['POST'])
@jwt_required()
def clear_chat():
    """Clear chat history for current user"""
    email = get_jwt_identity()
    
    # Reinitialize chat history by creating new entry
    db._write_json(db.chats_file, {})
    
    return jsonify({'message': 'Chat history cleared'}), 200

# ==================== Resume Routes ====================

@app.route('/api/resume/upload', methods=['POST'])
@jwt_required()
def upload_resume():
    """Upload and process resume"""
    email = get_jwt_identity()
    
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': f'File type not allowed. Allowed: {", ".join(app.config["ALLOWED_EXTENSIONS"])}'}), 400
    
    try:
        # Save file
        filename = secure_filename(file.filename)
        filename = f"{email}_{datetime.now().timestamp()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text based on file type
        file_ext = filename.rsplit('.', 1)[1].lower()
        
        if file_ext == 'pdf':
            resume_text = ResumeProcessor.extract_text_from_pdf(filepath)
        elif file_ext == 'docx':
            resume_text = ResumeProcessor.extract_text_from_docx(filepath)
        elif file_ext == 'doc':
            resume_text = ResumeProcessor.extract_text_from_doc(filepath)
        else:
            return jsonify({'error': 'Unsupported file type'}), 400
        
        # Extract resume data
        extracted_data = ResumeProcessor.extract_resume_data(resume_text)

        # Read optional provided qualifications/skills from the form
        provided_qualifications_raw = request.form.get('provided_qualifications', '')
        provided_skills_raw = request.form.get('provided_skills', '')

        provided_qualifications = [q.strip() for q in provided_qualifications_raw.split(',') if q.strip()] if provided_qualifications_raw else []
        provided_skills = [s.strip() for s in provided_skills_raw.split(',') if s.strip()] if provided_skills_raw else []

        # Merge provided skills into extracted_data for richer suggestions
        merged_skills = list({*(extracted_data.get('skills', [])), *provided_skills})
        extracted_data['skills'] = merged_skills

        # Get improvement suggestions
        suggestions = ResumeProcessor.get_improvement_suggestions(extracted_data, resume_text)

        # Save to database (store provided fields too)
        db.save_resume(email, filename, extracted_data, provided_qualifications=provided_qualifications, provided_skills=provided_skills)
        
        return jsonify({
            'message': 'Resume uploaded successfully',
            'filename': filename,
            'extracted_data': extracted_data,
            'suggestions': suggestions
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Error processing resume: {str(e)}'}), 500


@app.route('/api/career/job-requirements', methods=['POST'])
@jwt_required()
def job_requirements():
    """Given a target job title and optional company, suggest required skills and gaps"""
    email = get_jwt_identity()
    data = request.get_json() or {}

    job_title = data.get('job_title')
    company = data.get('company', '')
    user_skills_str = data.get('user_skills', '')

    if not job_title:
        return jsonify({'error': 'job_title is required'}), 400

    # Get saved resume context
    resume = db.get_resume(email) or {}
    resume_data = resume.get('extracted_data', {})
    provided_skills = resume.get('provided_skills', [])
    
    # Merge user-entered skills with provided skills
    user_entered = [s.strip() for s in user_skills_str.split(',') if s.strip()] if user_skills_str else []
    all_provided = list(set(provided_skills + user_entered))

    requirements = ai_assistant.get_job_requirements(job_title, company=company, resume_data=resume_data, provided_skills=all_provided)

    return jsonify(requirements), 200

@app.route('/api/resume/get', methods=['GET'])
@jwt_required()
def get_resume():
    """Get uploaded resume information"""
    email = get_jwt_identity()
    
    resume = db.get_resume(email)
    
    if not resume:
        return jsonify({'message': 'No resume uploaded yet'}), 404
    
    return jsonify(resume), 200

@app.route('/api/resume/suggestions', methods=['GET'])
@jwt_required()
def get_resume_suggestions():
    """Get resume improvement suggestions"""
    email = get_jwt_identity()
    
    resume = db.get_resume(email)
    
    if not resume:
        return jsonify({'error': 'No resume uploaded yet'}), 404
    
    extracted_data = resume.get('extracted_data', {})
    
    # Read resume file to get full text for suggestions
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], resume['filename'])
    
    try:
        file_ext = resume['filename'].rsplit('.', 1)[1].lower()
        
        if file_ext == 'pdf':
            resume_text = ResumeProcessor.extract_text_from_pdf(filepath)
        elif file_ext == 'docx':
            resume_text = ResumeProcessor.extract_text_from_docx(filepath)
        else:
            resume_text = ResumeProcessor.extract_text_from_doc(filepath)
        
        suggestions = ResumeProcessor.get_improvement_suggestions(extracted_data, resume_text)
        
        return jsonify(suggestions), 200
    
    except Exception as e:
        return jsonify({'error': f'Error generating suggestions: {str(e)}'}), 500

# ==================== Career Guidance Routes ====================

@app.route('/api/career/paths', methods=['GET'])
def get_career_paths():
    """Get available career paths"""
    career_paths = {}
    
    for career, details in CareerAIAssistant.CAREER_PATHS.items():
        career_paths[career] = {
            'description': details['description'],
            'skills': details['skills'],
            'education': details['education']
        }
    
    return jsonify(career_paths), 200

@app.route('/api/career/resume-tips', methods=['GET'])
def get_resume_tips():
    """Get resume tips"""
    tips = CareerAIAssistant.RESUME_TIPS
    return jsonify(tips), 200

@app.route('/api/career/interview-tips', methods=['GET'])
def get_interview_tips():
    """Get interview preparation tips"""
    tips = CareerAIAssistant.INTERVIEW_TIPS
    return jsonify({'tips': tips}), 200

@app.route('/api/career/skill-paths', methods=['GET'])
def get_skill_paths():
    """Get skill development paths"""
    paths = CareerAIAssistant.SKILL_PATHS
    return jsonify(paths), 200


@app.route('/api/career/generate-path', methods=['POST'])
@jwt_required()
def generate_career_path():
    """Generate career suggestions from user skills and interests"""
    email = get_jwt_identity()
    data = request.get_json() or {}

    skills = data.get('skills', [])
    interests = data.get('interests', '')

    # Normalize skills if string provided
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(',') if s.strip()]

    result = ai_assistant.generate_career_path(skills=skills, interests=interests)
    return jsonify(result), 200

# ==================== Health Check ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }), 200

# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
