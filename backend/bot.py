from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user

from .database import get_db
from .encryption import encrypt_data, decrypt_data
from .bot_logic import post_tweet_for_user

bp = Blueprint('bot', __name__, url_prefix='/api/bot')

# --- Helper function for scheduling ---

def reschedule_jobs_for_user(user_id):
    """
    Removes all existing jobs for a user and adds new ones based on their
    current schedule in the database.
    """
    scheduler = current_app.scheduler
    db = get_db()

    # Remove existing jobs for this user
    for job in scheduler.get_jobs():
        if job.id.startswith(f"user_{user_id}_"):
            scheduler.remove_job(job.id)
            print(f"Removed existing job: {job.id}")

    # Add new jobs based on the current schedule
    schedules = db.execute(
        'SELECT post_time FROM schedule WHERE user_id = ? AND is_active = 1',
        (user_id,)
    ).fetchall()

    for schedule in schedules:
        hour, minute = map(int, schedule['post_time'].split(':'))
        job_id = f"user_{user_id}_time_{schedule['post_time'].replace(':', '')}"
        scheduler.add_job(
            func=post_tweet_for_user,
            trigger='cron',
            hour=hour,
            minute=minute,
            args=[user_id],
            id=job_id,
            replace_existing=True
        )
        print(f"Added new job: {job_id}")

# --- Twitter Endpoints ---

@bp.route('/twitter/connect', methods=['POST'])
@login_required
def connect_twitter():
    """Connect a user's Twitter account by saving their encrypted API credentials."""
    # ... (code remains the same)
    data = request.get_json()
    required_keys = ['api_key', 'api_secret_key', 'access_token', 'access_token_secret']
    if not all(key in data for key in required_keys):
        return jsonify({'error': 'Missing one or more required API credentials.'}), 400

    db = get_db()
    try:
        db.execute(
            """
            UPDATE user SET twitter_api_key = ?, twitter_api_secret_key = ?,
                           twitter_access_token = ?, twitter_access_token_secret = ?
            WHERE id = ?
            """,
            (
                encrypt_data(data['api_key']),
                encrypt_data(data['api_secret_key']),
                encrypt_data(data['access_token']),
                encrypt_data(data['access_token_secret']),
                current_user.id,
            ),
        )
        db.commit()
    except Exception as e:
        print(f"Error saving Twitter credentials: {e}")
        return jsonify({'error': 'An internal error occurred while saving credentials.'}), 500

    return jsonify({'message': 'Twitter account connected successfully.'})

@bp.route('/twitter/status', methods=['GET'])
@login_required
def twitter_status():
    """Check if the user has connected their Twitter account."""
    # ... (code remains the same)
    db = get_db()
    user_row = db.execute('SELECT twitter_api_key FROM user WHERE id = ?', (current_user.id,)).fetchone()
    is_connected = bool(user_row and user_row['twitter_api_key'])
    return jsonify({'is_connected': is_connected})

# --- Content Queue Endpoints ---
# ... (code remains the same)
@bp.route('/content', methods=['GET'])
@login_required
def get_content():
    """Fetch all content for the logged-in user."""
    db = get_db()
    content_rows = db.execute(
        'SELECT * FROM content_queue WHERE user_id = ? ORDER BY created_at DESC',
        (current_user.id,)
    ).fetchall()
    content_list = [dict(row) for row in content_rows]
    return jsonify(content_list)

@bp.route('/content', methods=['POST'])
@login_required
def add_content():
    """Add new content to the user's queue."""
    data = request.get_json()
    if not data or not data.get('content') or not data.get('category'):
        return jsonify({'error': 'Content and category are required.'}), 400

    db = get_db()
    db.execute(
        'INSERT INTO content_queue (user_id, category, content) VALUES (?, ?, ?)',
        (current_user.id, data['category'], data['content'])
    )
    db.commit()
    return jsonify({'message': 'Content added successfully.'}), 201

@bp.route('/content/<int:content_id>', methods=['PUT'])
@login_required
def update_content(content_id):
    """Update a piece of content in the user's queue."""
    data = request.get_json()
    if not data or not data.get('content') or not data.get('category'):
        return jsonify({'error': 'Content and category are required.'}), 400

    db = get_db()
    db.execute(
        'UPDATE content_queue SET category = ?, content = ? WHERE id = ? AND user_id = ?',
        (data['category'], data['content'], content_id, current_user.id)
    )
    db.commit()
    return jsonify({'message': 'Content updated successfully.'})

@bp.route('/content/<int:content_id>', methods=['DELETE'])
@login_required
def delete_content(content_id):
    """Delete a piece of content from the user's queue."""
    db = get_db()
    db.execute(
        'DELETE FROM content_queue WHERE id = ? AND user_id = ?',
        (content_id, current_user.id)
    )
    db.commit()
    return jsonify({'message': 'Content deleted successfully.'})

# --- Schedule Endpoints ---

@bp.route('/schedule', methods=['GET'])
@login_required
def get_schedule():
    """Fetch the posting schedule for the logged-in user."""
    # ... (code remains the same)
    db = get_db()
    schedule_rows = db.execute(
        'SELECT id, post_time, is_active FROM schedule WHERE user_id = ? ORDER BY post_time',
        (current_user.id,)
    ).fetchall()
    schedule_list = [dict(row) for row in schedule_rows]
    return jsonify(schedule_list)

@bp.route('/schedule', methods=['POST'])
@login_required
def set_schedule():
    """Set or update the posting schedule for the logged-in user."""
    data = request.get_json()
    times = data.get('times')
    if not isinstance(times, list):
        return jsonify({'error': 'A list of times is required.'}), 400

    db = get_db()
    db.execute('DELETE FROM schedule WHERE user_id = ?', (current_user.id,))

    for t in times:
        if isinstance(t, str) and len(t) == 5 and t[2] == ':':
            db.execute(
                'INSERT INTO schedule (user_id, post_time) VALUES (?, ?)',
                (current_user.id, t)
            )

    db.commit()

    # Update the actual scheduler jobs
    try:
        reschedule_jobs_for_user(current_user.id)
    except Exception as e:
        print(f"Error rescheduling jobs for user {current_user.id}: {e}")
        return jsonify({'error': 'Schedule saved, but failed to update running jobs.'}), 500

    return jsonify({'message': 'Schedule updated and jobs rescheduled successfully.'})

# --- Thread Endpoints ---
import uuid

@bp.route('/threads', methods=['POST'])
@login_required
def create_thread():
    """
    Create a new thread with a list of tweets.
    Expects: {"title": "My new thread", "tweets": ["Tweet 1", "Tweet 2"]}
    """
    data = request.get_json()
    title = data.get('title')
    tweets = data.get('tweets')

    if not title or not isinstance(tweets, list) or not tweets:
        return jsonify({'error': 'Title and a non-empty list of tweets are required.'}), 400

    db = get_db()
    thread_id = str(uuid.uuid4())

    # Create the thread entry
    db.execute(
        'INSERT INTO threads (id, user_id, title) VALUES (?, ?, ?)',
        (thread_id, current_user.id, title)
    )

    # Add each tweet to the content queue, linked to the thread
    for i, tweet_content in enumerate(tweets):
        db.execute(
            """
            INSERT INTO content_queue (user_id, category, content, thread_id, order_in_thread)
            VALUES (?, 'thread', ?, ?, ?)
            """,
            (current_user.id, tweet_content, thread_id, i)
        )

    db.commit()
    return jsonify({'message': 'Thread created successfully.', 'thread_id': thread_id}), 201

@bp.route('/threads', methods=['GET'])
@login_required
def get_threads():
    """Get all threads for the logged-in user."""
    db = get_db()
    threads = db.execute(
        'SELECT * FROM threads WHERE user_id = ? ORDER BY created_at DESC',
        (current_user.id,)
    ).fetchall()
    return jsonify([dict(row) for row in threads])

@bp.route('/threads/<string:thread_id>', methods=['GET'])
@login_required
def get_thread_details(thread_id):
    """Get the details and content of a specific thread."""
    db = get_db()
    thread = db.execute(
        'SELECT * FROM threads WHERE id = ? AND user_id = ?',
        (thread_id, current_user.id)
    ).fetchone()

    if not thread:
        return jsonify({'error': 'Thread not found.'}), 404

    tweets = db.execute(
        'SELECT * FROM content_queue WHERE thread_id = ? ORDER BY order_in_thread ASC',
        (thread_id,)
    ).fetchall()

    return jsonify({
        'thread': dict(thread),
        'tweets': [dict(row) for row in tweets]
    })
