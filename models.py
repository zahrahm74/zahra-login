"""
Database Models
Defines the database schema and models for the Flask application.
"""

from datetime import datetime
import bcrypt
import re

def create_user_model(db):
    """Create User model with SQLAlchemy"""
    class User(db.Model):
        """
        User model for authentication and user management.
        Includes password hashing and validation methods.
        """
        
        __tablename__ = 'users'
        
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password_hash = db.Column(db.String(255), nullable=False)
        first_name = db.Column(db.String(50), nullable=True)
        last_name = db.Column(db.String(50), nullable=True)
        is_active = db.Column(db.Boolean, default=True)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        def __init__(self, username, email, password, first_name=None, last_name=None):
            """Initialize user with hashed password"""
            self.username = username
            self.email = email
            self.password_hash = self._hash_password(password)
            self.first_name = first_name
            self.last_name = last_name
        
        def _hash_password(self, password):
            """Hash password using bcrypt"""
            salt = bcrypt.gensalt()
            return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        
        def verify_password(self, password):
            """Verify password against stored hash"""
            return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
        
        @staticmethod
        def validate_email(email):
            """Validate email format"""
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return re.match(pattern, email) is not None
        
        @staticmethod
        def validate_password(password):
            """Validate password strength"""
            if len(password) < 8:
                return False, "Password must be at least 8 characters long"
            if not re.search(r'[A-Z]', password):
                return False, "Password must contain at least one uppercase letter"
            if not re.search(r'[a-z]', password):
                return False, "Password must contain at least one lowercase letter"
            if not re.search(r'\d', password):
                return False, "Password must contain at least one digit"
            return True, "Password is valid"
        
        @staticmethod
        def validate_username(username):
            """Validate username format"""
            if len(username) < 3 or len(username) > 20:
                return False, "Username must be between 3 and 20 characters"
            if not re.match(r'^[a-zA-Z0-9_]+$', username):
                return False, "Username can only contain letters, numbers, and underscores"
            return True, "Username is valid"
        
        def to_dict(self):
            """Convert user object to dictionary (excluding sensitive data)"""
            return {
                'id': self.id,
                'username': self.username,
                'email': self.email,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'is_active': self.is_active,
                'created_at': self.created_at.isoformat() if self.created_at else None,
                'updated_at': self.updated_at.isoformat() if self.updated_at else None
            }
        
        def __repr__(self):
            return f'<User {self.username}>'
    
    return User