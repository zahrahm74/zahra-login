"""
Application Routes
Defines all API endpoints for authentication and user management.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import re

def create_routes(db, User):
    """Create route blueprints"""
    # Create blueprints
    auth_bp = Blueprint('auth', __name__)
    user_bp = Blueprint('users', __name__)

    # Authentication Routes
    @auth_bp.route('/register', methods=['POST'])
    def register():
        """
        Register a new user
        Expected JSON: {
            "username": "string",
            "email": "string", 
            "password": "string",
            "first_name": "string" (optional),
            "last_name": "string" (optional)
        }
        """
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['username', 'email', 'password']
            for field in required_fields:
                if not data or field not in data:
                    return jsonify({'error': f'Missing required field: {field}'}), 400
            
            username = data['username'].strip()
            email = data['email'].strip().lower()
            password = data['password']
            first_name = data.get('first_name', '').strip()
            last_name = data.get('last_name', '').strip()
            
            # Validate input data
            if not User.validate_username(username):
                return jsonify({'error': 'Invalid username format'}), 400
            
            if not User.validate_email(email):
                return jsonify({'error': 'Invalid email format'}), 400
            
            is_valid, message = User.validate_password(password)
            if not is_valid:
                return jsonify({'error': message}), 400
            
            # Check if user already exists
            if User.query.filter_by(username=username).first():
                return jsonify({'error': 'Username already exists'}), 409
            
            if User.query.filter_by(email=email).first():
                return jsonify({'error': 'Email already exists'}), 409
            
            # Create new user
            user = User(
                username=username,
                email=email,
                password=password,
                first_name=first_name if first_name else None,
                last_name=last_name if last_name else None
            )
            
            db.session.add(user)
            db.session.commit()
            
            # Create access token
            access_token = create_access_token(identity=user.id)
            
            return jsonify({
                'message': 'User registered successfully',
                'user': user.to_dict(),
                'access_token': access_token
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Registration failed'}), 500

    @auth_bp.route('/login', methods=['POST'])
    def login():
        """
        Authenticate user and return JWT token
        Expected JSON: {
            "username": "string" or "email": "string",
            "password": "string"
        }
        """
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            # Accept either username or email
            identifier = data.get('username') or data.get('email')
            password = data.get('password')
            
            if not identifier or not password:
                return jsonify({'error': 'Username/email and password are required'}), 400
            
            # Find user by username or email
            user = None
            if '@' in identifier:
                user = User.query.filter_by(email=identifier.lower()).first()
            else:
                user = User.query.filter_by(username=identifier).first()
            
            if not user or not user.verify_password(password):
                return jsonify({'error': 'Invalid credentials'}), 401
            
            if not user.is_active:
                return jsonify({'error': 'Account is deactivated'}), 401
            
            # Create access token
            access_token = create_access_token(identity=user.id)
            
            return jsonify({
                'message': 'Login successful',
                'user': user.to_dict(),
                'access_token': access_token
            }), 200
            
        except Exception as e:
            return jsonify({'error': 'Login failed'}), 500

    @auth_bp.route('/profile', methods=['GET'])
    @jwt_required()
    def get_profile():
        """Get current user profile"""
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            return jsonify({
                'user': user.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({'error': 'Failed to retrieve profile'}), 500

    # User Management Routes
    @user_bp.route('/', methods=['GET'])
    @jwt_required()
    def get_users():
        """Get all users (admin only)"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            
            # Simple admin check (you might want to add an admin field to User model)
            if not current_user:
                return jsonify({'error': 'User not found'}), 404
            
            users = User.query.all()
            return jsonify({
                'users': [user.to_dict() for user in users]
            }), 200
            
        except Exception as e:
            return jsonify({'error': 'Failed to retrieve users'}), 500

    @user_bp.route('/<int:user_id>', methods=['GET'])
    @jwt_required()
    def get_user(user_id):
        """Get specific user by ID"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            
            if not current_user:
                return jsonify({'error': 'User not found'}), 404
            
            # Users can only view their own profile or if they're admin
            if current_user.id != user_id:
                return jsonify({'error': 'Access denied'}), 403
            
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            return jsonify({
                'user': user.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({'error': 'Failed to retrieve user'}), 500

    @user_bp.route('/<int:user_id>', methods=['PUT'])
    @jwt_required()
    def update_user(user_id):
        """
        Update user profile
        Expected JSON: {
            "first_name": "string" (optional),
            "last_name": "string" (optional),
            "email": "string" (optional)
        }
        """
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            
            if not current_user:
                return jsonify({'error': 'User not found'}), 404
            
            # Users can only update their own profile
            if current_user.id != user_id:
                return jsonify({'error': 'Access denied'}), 403
            
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            # Update allowed fields
            if 'first_name' in data:
                current_user.first_name = data['first_name'].strip() if data['first_name'] else None
            
            if 'last_name' in data:
                current_user.last_name = data['last_name'].strip() if data['last_name'] else None
            
            if 'email' in data:
                new_email = data['email'].strip().lower()
                if not User.validate_email(new_email):
                    return jsonify({'error': 'Invalid email format'}), 400
                
                # Check if email is already taken by another user
                existing_user = User.query.filter_by(email=new_email).first()
                if existing_user and existing_user.id != current_user.id:
                    return jsonify({'error': 'Email already exists'}), 409
                
                current_user.email = new_email
            
            db.session.commit()
            
            return jsonify({
                'message': 'User updated successfully',
                'user': current_user.to_dict()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to update user'}), 500

    @user_bp.route('/<int:user_id>', methods=['DELETE'])
    @jwt_required()
    def delete_user(user_id):
        """Delete user account"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            
            if not current_user:
                return jsonify({'error': 'User not found'}), 404
            
            # Users can only delete their own account
            if current_user.id != user_id:
                return jsonify({'error': 'Access denied'}), 403
            
            db.session.delete(current_user)
            db.session.commit()
            
            return jsonify({
                'message': 'User deleted successfully'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to delete user'}), 500

    return auth_bp, user_bp