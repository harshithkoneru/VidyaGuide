from typing import Dict, List, Optional
import random
import re
import difflib

class CareerAIAssistant:
    """AI Assistant for career guidance and resume mentoring"""
    
    # Career paths and requirements
    CAREER_PATHS = {
        'Software Engineer': {
            'skills': ['Programming', 'Problem Solving', 'Data Structures', 'System Design'],
            'education': ['Computer Science', 'Engineering', 'Information Technology'],
            'description': 'Develop and maintain software applications'
        },
        'Data Scientist': {
            'skills': ['Python', 'Statistics', 'Machine Learning', 'SQL'],
            'education': ['Mathematics', 'Statistics', 'Computer Science'],
            'description': 'Analyze complex data sets to help organizations make decisions'
        },
        'Product Manager': {
            'skills': ['Communication', 'Leadership', 'Analytics', 'Strategy'],
            'education': ['Business', 'Engineering', 'Economics'],
            'description': 'Lead product development and strategy'
        },
        'UX/UI Designer': {
            'skills': ['Design', 'Communication', 'Problem Solving', 'Empathy'],
            'education': ['Design', 'Psychology', 'Computer Science'],
            'description': 'Create beautiful and user-friendly interfaces'
        },
        'Marketing Manager': {
            'skills': ['Communication', 'Creativity', 'Analytics', 'Leadership'],
            'education': ['Marketing', 'Business', 'Communications'],
            'description': 'Drive marketing strategy and brand growth'
        }
    }
    
    # Resume tips
    RESUME_TIPS = {
        'formatting': [
            "Use a clean, simple font (Arial, Calibri, or Times New Roman) in 10-12pt size",
            "Keep margins between 0.5 and 1 inch on all sides",
            "Use consistent spacing and bullet points for readability",
            "Limit your resume to 1-2 pages maximum",
            "Use a professional email address and phone number",
            "Avoid using images, graphics, or colored text (unless you're a designer)"
        ],
        'content': [
            "Start with a professional summary or objective statement",
            "List your most recent experience first (reverse chronological order)",
            "Use action verbs like 'developed', 'managed', 'implemented', 'created'",
            "Include quantifiable achievements (e.g., 'increased sales by 20%')",
            "Tailor your resume for each job application",
            "Proofread carefully for spelling and grammar mistakes",
            "Include a LinkedIn profile URL if you have one"
        ],
        'structure': [
            "Contact Information: Name, Email, Phone, City/State, LinkedIn URL",
            "Professional Summary: 2-3 lines highlighting your key strengths",
            "Skills: Organized by category (Technical, Leadership, Languages)",
            "Work Experience: Job title, Company, Duration, Key achievements",
            "Education: Degree, University, Graduation date, Relevant coursework",
            "Certifications & Awards: Industry certifications and achievements"
        ]
    }
    
    # Interview tips
    INTERVIEW_TIPS = [
        "Research the company thoroughly before the interview",
        "Practice common interview questions like 'Tell me about yourself'",
        "Use the STAR method (Situation, Task, Action, Result) for behavioral questions",
        "Prepare 2-3 thoughtful questions to ask the interviewer",
        "Dress professionally and arrive 10-15 minutes early",
        "Make eye contact, smile, and give a firm handshake",
        "Speak clearly and avoid filler words like 'um' and 'uh'",
        "Follow up with a thank-you email within 24 hours of the interview"
    ]
    
    # Skill development paths
    SKILL_PATHS = {
        'Programming': {
            'beginner': ['Python', 'JavaScript', 'HTML/CSS'],
            'intermediate': ['Django', 'React', 'SQL'],
            'advanced': ['System Design', 'Microservices', 'Cloud Architecture']
        },
        'Data Science': {
            'beginner': ['Python', 'Statistics', 'Pandas'],
            'intermediate': ['Machine Learning', 'TensorFlow', 'Data Visualization'],
            'advanced': ['Deep Learning', 'NLP', 'Reinforcement Learning']
        },
        'Design': {
            'beginner': ['UI Principles', 'Color Theory', 'Typography'],
            'intermediate': ['Figma', 'Prototyping', 'User Research'],
            'advanced': ['Design Systems', 'Interaction Design', 'A/B Testing']
        }
    }
    
    def __init__(self):
        self.conversation_context = {}

    def get_job_requirements(self, job_title: str, company: str = '', resume_data: Optional[Dict] = None, provided_skills: Optional[list] = None) -> Dict:
        """Return suggested skills and improvement areas for a target job (simple heuristic)."""
        job_title_norm = job_title.strip()
        # Find best matching career path with simple keyword heuristics
        best_match = None
        role_lower = job_title_norm.lower()

        # Keyword-based mapping for common roles
        if 'full stack' in role_lower or 'full-stack' in role_lower or 'fullstack' in role_lower or 'full stack developer' in role_lower:
            best_match = 'Software Engineer'
        elif 'software' in role_lower or 'engineer' in role_lower or 'developer' in role_lower:
            best_match = 'Software Engineer'
        elif 'intern' in role_lower or 'internship' in role_lower:
            # Heuristic: internships at tech/finance firms often map to software or data roles
            if 'data' in role_lower:
                best_match = 'Data Scientist'
            else:
                best_match = 'Software Engineer'
        elif 'data' in role_lower or 'data scientist' in role_lower or 'machine learning' in role_lower:
            best_match = 'Data Scientist'
        elif 'product' in role_lower:
            best_match = 'Product Manager'
        elif 'ux' in role_lower or 'ui' in role_lower or 'designer' in role_lower:
            best_match = 'UX/UI Designer'
        elif 'marketing' in role_lower:
            best_match = 'Marketing Manager'
        else:
            for career in self.CAREER_PATHS:
                if career.lower() in role_lower or role_lower in career.lower():
                    best_match = career
                    break

        requirements = {
            'job_title': job_title,
            'company': company,
            'required_skills': [],
            'missing_skills': [],
            'advice': []
        }

        # Base required skills from CAREER_PATHS when available
        if best_match:
            base_skills = self.CAREER_PATHS[best_match].get('skills', [])
            requirements['required_skills'] = base_skills
        else:
            # fallback generic skills
            requirements['required_skills'] = ['Communication', 'Problem Solving', 'Teamwork']

        # Merge provided_skills and resume_data skills to assess gaps
        current_skills = set()
        if provided_skills:
            current_skills.update([s.strip().lower() for s in provided_skills if s])
        if resume_data and resume_data.get('skills'):
            current_skills.update([s.strip().lower() for s in resume_data.get('skills')])

        # Determine missing skills
        missing = []
        for req in requirements['required_skills']:
            if req.lower() not in current_skills:
                missing.append(req)

        requirements['missing_skills'] = missing

        # Provide actionable advice
        if missing:
            requirements['advice'].append(f"To be competitive for {job_title}, consider learning: {', '.join(missing)}.")
            # Suggest learning paths when known
            for skill in missing:
                # find skill path
                for path_name, levels in self.SKILL_PATHS.items():
                    if skill.lower() in ' '.join(levels.get('beginner', [])).lower() or skill.lower() in path_name.lower():
                        requirements['advice'].append(f"Learning path for {skill}: Beginner -> {', '.join(levels.get('beginner', [])[:3])}; Intermediate -> {', '.join(levels.get('intermediate', [])[:3])}.")
                        break
        else:
            requirements['advice'].append(f"Your current skills look well-aligned for {job_title}! Focus on demonstrating them with projects and achievements.")

        # Company-specific hints (very lightweight)
        if company:
            requirements['advice'].append(f"For roles at {company}, research their tech stack and tailor your resume to include relevant technologies and keywords used by the company.")
            # Add company-specific suggested skills when known
            comp_lower = company.lower()
            company_skills = []
            if 'amazon' in comp_lower:
                company_skills = ['AWS', 'Distributed Systems', 'Microservices', 'Scalability', 'React', 'Node.js']
            elif 'jpm' in comp_lower or 'jp morgan' in comp_lower or 'jpmorgan' in comp_lower:
                company_skills = ['SQL', 'Java', 'Low-latency Systems', 'Data Structures', 'Finance Domain Knowledge']
            elif 'google' in comp_lower or 'meta' in comp_lower or 'facebook' in comp_lower:
                company_skills = ['System Design', 'Distributed Systems', 'Algorithms', 'Large-scale Systems']

            if company_skills:
                requirements['advice'].append(f"Company-specific skills to focus on: {', '.join(company_skills)}.")
                # Also suggest adding missing company skills to missing_skills if not present
                for cs in company_skills:
                    if cs.lower() not in current_skills and cs not in requirements['missing_skills']:
                        requirements['missing_skills'].append(cs)

        # Add interview and resume tips
        requirements['advice'].append("Highlight measurable achievements and use concise bullet points on your resume.")

        return requirements
    
    def get_response(self, user_message: str, user_email: str, resume_context: Optional[Dict] = None) -> Dict:
        """Generate AI response to user message"""
        
        user_message_lower = user_message.lower()
        # update conversation context with recent resume if provided
        if resume_context:
            # resume_context may be a resume record from the DB (with extracted_data, provided_skills)
            self.conversation_context['last_resume'] = resume_context
        
        # Detect user intent
        if any(keyword in user_message_lower for keyword in ['career path', 'career', 'job', 'profession']):
            response = self._handle_career_guidance(user_message)
        elif any(keyword in user_message_lower for keyword in ['resume', 'cv', 'application']):
            response = self._handle_resume_advice(user_message, resume_context)
        elif any(keyword in user_message_lower for keyword in ['interview', 'preparation', 'prepare']):
            response = self._handle_interview_prep(user_message)
        elif any(keyword in user_message_lower for keyword in ['skill', 'learn', 'education']):
            response = self._handle_skill_development(user_message)
        else:
            response = self._handle_general_career_question(user_message)
        
        return {
            'role': 'assistant',
            'content': response,
            'type': 'text'
        }

    def generate_career_path(self, skills: Optional[list] = None, interests: Optional[str] = '') -> Dict:
        """Given user skills and interests, suggest matching career paths and next steps."""
        # Normalize and expand common abbreviations / short forms
        def normalize_skill(s: str) -> str:
            s0 = s.strip()
            if not s0:
                return s0
            s_low = s0.lower()
            aliases = {
                'ml': 'Machine Learning',
                'ai': 'Machine Learning',
                'ds': 'Data Science',
                'js': 'JavaScript',
                'py': 'Python',
                'sql': 'SQL',
                'reactjs': 'React',
                'react.js': 'React',
                'node': 'Node.js',
                'nodejs': 'Node.js'
            }
            if s_low in aliases:
                return aliases[s_low]
            # common tokens mapping
            for k, v in aliases.items():
                if k in s_low.split():
                    return v
            # Capitalize common tech words
            return s0

        skills = [normalize_skill(s) for s in (skills or []) if s]
        interest_text = (interests or '').lower()

        # Score career paths by matching skills and interests
        matches = []
        for career, details in self.CAREER_PATHS.items():
            score = 0
            # skills match (fuzzy/inclusion)
            for req in details.get('skills', []):
                req_low = req.lower()
                for user_skill in skills:
                    user_low = user_skill.lower()
                    # direct inclusion
                    if user_low and (user_low in req_low or req_low in user_low):
                        score += 2
                        break
                    # fuzzy match by close words
                    req_words = req_low.split()
                    match = difflib.get_close_matches(user_low, req_words, n=1, cutoff=0.8)
                    if match:
                        score += 1
                        break
            # interest keyword match
            if any(word in interest_text for word in career.lower().split()):
                score += 1
            # partial interest match on description
            if any(word in interest_text for word in details.get('description', '').lower().split()):
                score += 1

            matches.append((career, score, details))

        # Sort by score desc
        matches.sort(key=lambda x: x[1], reverse=True)

        # Build suggestions
        suggestions = []
        for career, score, details in matches[:4]:
            suggestions.append({
                'career': career,
                'score': score,
                'description': details.get('description'),
                'key_skills': details.get('skills', []),
                'education': details.get('education', [])
            })

        next_steps = [
            'Compare the top suggested career paths and choose one to explore in depth.',
            'Tailor your resume to emphasize relevant skills and projects for the chosen path.',
            'Build 1-2 focused projects demonstrating the required technical skills.',
            'Use mock interviews and study system design (for engineering roles) or statistics (for data roles).'
        ]

        return {
            'suggestions': suggestions,
            'next_steps': next_steps
        }
    
    def _handle_career_guidance(self, message: str) -> str:
        """Handle career guidance questions"""
        response = "I'd be happy to help you explore career options! Here are some exciting paths you might consider:\n\n"
        
        for career, details in list(self.CAREER_PATHS.items())[:3]:
            response += f"**{career}**\n"
            response += f"• Description: {details['description']}\n"
            response += f"• Key Skills: {', '.join(details['skills'][:2])}\n"
            response += f"• Educational Background: {', '.join(details['education'][:1])}\n\n"
        
        response += "Which of these interests you? I can provide more detailed information about any career path, including:\n"
        response += "• Required skills and qualifications\n"
        response += "• Steps to get started\n"
        response += "• Job market outlook and salary ranges\n"
        response += "• Companies hiring for these roles\n\n"
        response += "Feel free to ask follow-up questions!"
        
        return response
    
    def _handle_resume_advice(self, message: str, resume_context: Optional[Dict] = None) -> str:
        """Handle resume-related questions"""
        response = "Great! I'm here to help improve your resume. "
        
        if resume_context:
            response += "Based on your uploaded resume, here are some personalized suggestions:\n\n"
            response += self._get_resume_feedback(resume_context)
        else:
            response += "Here are some essential resume tips:\n\n"
            response += "**Formatting Tips:**\n"
            for tip in self.RESUME_TIPS['formatting'][:3]:
                response += f"• {tip}\n"
            
            response += "\n**Content Tips:**\n"
            for tip in self.RESUME_TIPS['content'][:3]:
                response += f"• {tip}\n"
            
            response += "\n**Resume Structure:**\n"
            for tip in self.RESUME_TIPS['structure'][:3]:
                response += f"• {tip}\n"
        
        response += "\n\nWould you like more specific advice on any section? You can also upload your resume for personalized feedback!"
        
        return response
    
    def _handle_interview_prep(self, message: str) -> str:
        """Handle interview preparation questions"""
        response = "Preparing for an interview? Here are some essential tips:\n\n"
        
        for tip in self.INTERVIEW_TIPS[:4]:
            response += f"• {tip}\n"
        
        response += "\n**Common Interview Questions to Practice:**\n"
        response += "1. 'Tell me about yourself' - Focus on your professional journey\n"
        response += "2. 'Why are you interested in this position?' - Show you've researched the company\n"
        response += "3. 'What are your strengths and weaknesses?' - Be honest and constructive\n"
        response += "4. 'Tell me about a challenge you overcame' - Use the STAR method\n"
        response += "5. 'Why should we hire you?' - Highlight unique value you bring\n\n"
        response += "Remember: Most interviews test both your technical knowledge and your communication skills. "
        response += "Practice speaking clearly and confidently about your experience!"
        
        return response
    
    def _handle_skill_development(self, message: str) -> str:
        """Handle skill development questions"""
        # Detect queries asking about a specific job and company, e.g. "skills for full stack developer at Amazon"
        msg = message.strip()
        pattern = re.compile(r"(?P<role>[\w\s\-+]+?)\s+(?:in|at|for)\s+(?P<company>[A-Za-z0-9 &.\-]+)", re.IGNORECASE)
        m = pattern.search(msg)

        if m:
            role = m.group('role').strip()
            company = m.group('company').strip()

            # Try to obtain resume context from conversation context if previously stored
            resume_data = None
            provided_skills = None
            last_resume = self.conversation_context.get('last_resume')
            if last_resume:
                resume_data = last_resume.get('extracted_data')
                provided_skills = last_resume.get('provided_skills')

            req = self.get_job_requirements(role, company, resume_data=resume_data, provided_skills=provided_skills)

            response = f"Targeted guidance for {role}{' at ' + company if company else ''}:\n\n"
            if req.get('required_skills'):
                response += f"• Required Skills: {', '.join(req.get('required_skills'))}\n"
            if req.get('missing_skills'):
                response += f"• Missing Skills: {', '.join(req.get('missing_skills'))}\n"
            if req.get('advice'):
                response += "\nRecommendations:\n"
                for a in req.get('advice'):
                    response += f"• {a}\n"

            return response

        # Fallback generic paths if no role/company detected
        response = "Developing new skills is key to career growth! Here's a learning path for popular skills:\n\n"
        for skill, levels in list(self.SKILL_PATHS.items())[:2]:
            response += f"**{skill} Learning Path:**\n"
            response += f"• Beginner: {', '.join(levels['beginner'])}\n"
            response += f"• Intermediate: {', '.join(levels['intermediate'])}\n"
            response += f"• Advanced: {', '.join(levels['advanced'])}\n\n"

        response += "**Tips for Skill Development:**\n"
        response += "• Start with fundamentals and practice consistently\n"
        response += "• Build real projects to apply what you've learned\n"
        response += "• Learn from others through blogs, courses, and communities\n"
        response += "• Don't be afraid to fail - it's part of the learning process\n\n"
        response += "What skill would you like to develop? I can provide specific learning resources and career paths!"

        return response
    
    def _handle_general_career_question(self, message: str) -> str:
        """Handle general career questions"""
        response = "That's a great question about your career! I can help you with:\n\n"
        response += "💼 **Career Guidance** - Explore different career paths and choose the right one for you\n"
        response += "📄 **Resume Help** - Improve your resume with formatting and content tips\n"
        response += "🎤 **Interview Prep** - Prepare for interviews with tips and practice questions\n"
        response += "🎓 **Skill Development** - Learn what skills you need and how to develop them\n"
        response += "📊 **Career Analytics** - Understand job market trends and salary insights\n\n"
        response += "Feel free to ask me anything career-related, and I'll do my best to provide helpful, friendly advice. "
        response += "What would you like to focus on today?"
        
        return response
    
    def _get_resume_feedback(self, resume_context: Dict) -> str:
        """Generate personalized resume feedback based on extracted data"""
        feedback = ""
        
        extracted = resume_context.get('extracted_data', {})
        
        # Skills feedback
        if extracted.get('skills'):
            feedback += f"**Your Skills:**\n"
            feedback += f"Great! You've listed {len(extracted['skills'])} skills. Make sure they're:\n"
            feedback += f"• Relevant to the jobs you're applying for\n"
            feedback += f"• Organized by category (Technical, Professional, Languages)\n"
            feedback += f"Current skills: {', '.join(extracted['skills'][:5])}\n\n"
        else:
            feedback += "**Add a Skills Section:** Create a dedicated section highlighting your technical and professional abilities.\n\n"
        
        # Education feedback
        if extracted.get('education'):
            feedback += f"**Education:**\n"
            feedback += f"Good! You have {len(extracted['education'])} educational qualification(s).\n\n"
        
        # Experience feedback
        if extracted.get('experience'):
            feedback += f"**Experience:**\n"
            feedback += f"You've documented {len(extracted['experience'])} work experience(s). "
            feedback += f"Make sure each includes:\n"
            feedback += f"• Job title, Company, and Duration\n"
            feedback += f"• 3-4 achievement bullets with quantifiable results\n"
            feedback += f"• Action verbs like 'developed', 'managed', 'improved'\n\n"
        else:
            feedback += "**Add Work Experience:** Highlight your previous roles and key achievements with measurable results.\n\n"
        
        feedback += "**Next Steps:**\n"
        feedback += "1. Tailor your resume for each job application\n"
        feedback += "2. Ask colleagues or mentors for feedback\n"
        feedback += "3. Keep it to 1-2 pages\n"
        feedback += "4. Proofread carefully for any errors\n"
        
        return feedback
