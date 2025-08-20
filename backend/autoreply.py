from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from .database import get_db

bp = Blueprint('autoreply', __name__, url_prefix='/api/autoreply')

@bp.route('/settings', methods=['GET'])
@login_required
def get_settings():
    """Get the auto-reply settings for the current user."""
    db = get_db()
    settings = db.execute(
        'SELECT * FROM auto_reply_settings WHERE user_id = ?', (current_user.id,)
    ).fetchone()
    if not settings:
        # If no settings exist, return default values
        return jsonify({'is_active': False, 'reply_frequency_minutes': 15})
    return jsonify(dict(settings))

@bp.route('/settings', methods=['POST'])
@login_required
def set_settings():
    """Update the auto-reply settings for the current user."""
    data = request.get_json()
    is_active = data.get('is_active', False)
    frequency = data.get('reply_frequency_minutes', 15)

    db = get_db()
    # Use INSERT OR REPLACE (UPSERT) to handle both creation and update
    db.execute(
        """
        INSERT INTO auto_reply_settings (user_id, is_active, reply_frequency_minutes)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
        is_active = excluded.is_active,
        reply_frequency_minutes = excluded.reply_frequency_minutes;
        """,
        (current_user.id, is_active, frequency)
    )
    db.commit()

    # Update the scheduler job for this user
    from .bot_logic import check_and_reply_to_mentions
    from flask import current_app
    scheduler = current_app.scheduler
    job_id = f"user_{current_user.id}_autoreply"

    if is_active:
        # Add or modify the job
        scheduler.add_job(
            func=check_and_reply_to_mentions,
            trigger='interval',
            minutes=frequency,
            args=[current_user.id],
            id=job_id,
            replace_existing=True
        )
        print(f"Upserted auto-reply job for user {current_user.id}.")
    else:
        # Remove the job if it exists
        if scheduler.get_job(job_id):
            scheduler.remove_job(job_id)
            print(f"Removed auto-reply job for user {current_user.id}.")

    return jsonify({'message': 'Settings updated successfully.'})

@bp.route('/templates', methods=['GET'])
@login_required
def get_templates():
    """Get all auto-reply templates for the user."""
    db = get_db()
    templates = db.execute(
        'SELECT * FROM auto_reply_templates WHERE user_id = ?', (current_user.id,)
    ).fetchall()
    return jsonify([dict(row) for row in templates])

@bp.route('/templates', methods=['POST'])
@login_required
def add_template():
    """Add a new reply template."""
    data = request.get_json()
    template_text = data.get('template_text')
    if not template_text:
        return jsonify({'error': 'Template text is required.'}), 400

    db = get_db()
    db.execute(
        'INSERT INTO auto_reply_templates (user_id, template_text) VALUES (?, ?)',
        (current_user.id, template_text)
    )
    db.commit()
    return jsonify({'message': 'Template added successfully.'}), 201

@bp.route('/templates/<int:template_id>', methods=['DELETE'])
@login_required
def delete_template(template_id):
    """Delete a reply template."""
    db = get_db()
    db.execute(
        'DELETE FROM auto_reply_templates WHERE id = ? AND user_id = ?',
        (template_id, current_user.id)
    )
    db.commit()
    return jsonify({'message': 'Template deleted successfully.'})
