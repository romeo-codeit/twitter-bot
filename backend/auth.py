from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user, UserMixin

from .database import get_db

# Create a blueprint for authentication routes
bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# --- User Model and Loader ---

class User(UserMixin):
    """A user model for Flask-Login."""
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

def get_user_by_username(username):
    """Get a user from the database by username."""
    db = get_db()
    user_row = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()
    return user_row

def load_user(user_id):
    """Load a user from the database by user ID for Flask-Login."""
    db = get_db()
    user_row = db.execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()
    if user_row:
        return User(id=user_row['id'], username=user_row['username'], password_hash=user_row['password'])
    return None

# --- Auth Routes ---

@bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required.'}), 400

    username = data['username']
    password = data['password']
    db = get_db()

    if get_user_by_username(username) is not None:
        return jsonify({'error': f"User '{username}' is already registered."}), 409

    db.execute(
        'INSERT INTO user (username, password) VALUES (?, ?)',
        (username, generate_password_hash(password))
    )
    db.commit()
    return jsonify({'message': f'User {username} created successfully.'}), 201

@bp.route('/login', methods=['POST'])
def login():
    """Log a user in."""
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required.'}), 400

    username = data['username']
    password = data['password']

    user_row = get_user_by_username(username)

    if user_row is None or not check_password_hash(user_row['password'], password):
        return jsonify({'error': 'Invalid username or password.'}), 401

    user = User(id=user_row['id'], username=user_row['username'], password_hash=user_row['password'])
    login_user(user)
    return jsonify({
        'message': 'Logged in successfully.',
        'user': {'id': user.id, 'username': user.username}
    })

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Log the current user out."""
    logout_user()
    return jsonify({'message': 'Logged out successfully.'})

@bp.route('/status')
@login_required
def status():
    """Check the login status and get current user info."""
    return jsonify({
        'logged_in': True,
        'user': {
            'id': current_user.id,
            'username': current_user.username
        }
    })
