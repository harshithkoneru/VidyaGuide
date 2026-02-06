import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class Database:
    """Simple JSON-based database for user data and chat history"""
    
    def __init__(self, database_path: str):
        self.database_path = database_path
        self.users_file = os.path.join(database_path, 'users.json')
        self.chats_file = os.path.join(database_path, 'chats.json')
        self.resumes_file = os.path.join(database_path, 'resumes.json')
        
        os.makedirs(database_path, exist_ok=True)
        self._initialize_files()
    
    def _initialize_files(self):
        """Initialize JSON files if they don't exist"""
        if not os.path.exists(self.users_file):
            self._write_json(self.users_file, {})
        if not os.path.exists(self.chats_file):
            self._write_json(self.chats_file, {})
        if not os.path.exists(self.resumes_file):
            self._write_json(self.resumes_file, {})
    
    def _read_json(self, filepath: str) -> Dict:
        """Read JSON file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _write_json(self, filepath: str, data: Dict):
        """Write JSON file"""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    # User operations
    def create_user(self, email: str, name: str, password_hash: str) -> bool:
        """Create a new user"""
        users = self._read_json(self.users_file)
        if email in users:
            return False
        
        users[email] = {
            'email': email,
            'name': name,
            'password_hash': password_hash,
            'created_at': datetime.now().isoformat(),
            'resume': None
        }
        self._write_json(self.users_file, users)
        return True
    
    def get_user(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        users = self._read_json(self.users_file)
        return users.get(email)
    
    def update_user(self, email: str, data: Dict) -> bool:
        """Update user data"""
        users = self._read_json(self.users_file)
        if email not in users:
            return False
        users[email].update(data)
        self._write_json(self.users_file, users)
        return True
    
    # Chat operations
    def save_chat_message(self, user_email: str, role: str, content: str, resume_context: Optional[str] = None) -> Dict:
        """Save a chat message"""
        chats = self._read_json(self.chats_file)
        
        if user_email not in chats:
            chats[user_email] = []
        
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'resume_context': resume_context
        }
        chats[user_email].append(message)
        self._write_json(self.chats_file, chats)
        return message
    
    def get_chat_history(self, user_email: str, limit: int = 50) -> List[Dict]:
        """Get chat history for a user"""
        chats = self._read_json(self.chats_file)
        messages = chats.get(user_email, [])
        return messages[-limit:]
    
    # Resume operations
    def save_resume(self, user_email: str, filename: str, extracted_data: Dict, provided_qualifications: Optional[list] = None, provided_skills: Optional[list] = None) -> bool:
        """Save resume information and any provided qualifications/skills"""
        resumes = self._read_json(self.resumes_file)
        
        resumes[user_email] = {
            'filename': filename,
            'uploaded_at': datetime.now().isoformat(),
            'extracted_data': extracted_data,
            'provided_qualifications': provided_qualifications or [],
            'provided_skills': provided_skills or []
        }
        self._write_json(self.resumes_file, resumes)
        
        # Update user record
        self.update_user(user_email, {'resume': filename})
        return True
    
    def get_resume(self, user_email: str) -> Optional[Dict]:
        """Get resume information for a user"""
        resumes = self._read_json(self.resumes_file)
        return resumes.get(user_email)
