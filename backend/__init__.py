import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from . import database

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=os.path.join(app.instance_path, 'tweets.db'),
        FERNET_KEY=os.environ.get('FERNET_KEY'),
        SCHEDULER_JOBSTORES={
            'default': SQLAlchemyJobStore(url=f"sqlite:///{os.path.join(app.instance_path, 'tweets.db')}")
        },
        SCHEDULER_API_ENABLED=True
    )

    # Set up CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register database functions
    database.init_app(app)

    # Initialize Flask-Login
    from .auth import load_user
    login_manager = LoginManager()
    login_manager.init_app(app)
    @login_manager.user_loader
    def user_loader(user_id):
        return load_user(user_id)
    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({"error": "Authentication required."}), 401

    # Register blueprints
    from . import auth, bot, autoreply
    app.register_blueprint(auth.bp)
    app.register_blueprint(bot.bp)
    app.register_blueprint(autoreply.bp)

    # Initialize scheduler
    scheduler = BackgroundScheduler(jobstores=app.config['SCHEDULER_JOBSTORES'])
    if not scheduler.running:
        scheduler.start()
        print("Scheduler started.")

    # Function to load jobs into the scheduler
    def load_jobs(app_context):
        with app_context:
            from .bot_logic import post_tweet_for_user, check_and_reply_to_mentions
            db = database.get_db()

            # Load tweet posting jobs
            schedules = db.execute('SELECT user_id, post_time FROM schedule WHERE is_active = 1').fetchall()
            print(f"Found {len(schedules)} schedules to load.")
            for schedule in schedules:
                hour, minute = map(int, schedule['post_time'].split(':'))
                job_id = f"user_{schedule['user_id']}_post_{schedule['post_time'].replace(':', '')}"
                scheduler.add_job(func=post_tweet_for_user, trigger='cron', hour=hour, minute=minute, args=[schedule['user_id']], id=job_id, replace_existing=True)

            # Load auto-reply jobs
            reply_settings = db.execute('SELECT user_id, reply_frequency_minutes FROM auto_reply_settings WHERE is_active = 1').fetchall()
            print(f"Found {len(reply_settings)} auto-reply settings to load.")
            for setting in reply_settings:
                job_id = f"user_{setting['user_id']}_autoreply"
                scheduler.add_job(func=check_and_reply_to_mentions, trigger='interval', minutes=setting['reply_frequency_minutes'], args=[setting['user_id']], id=job_id, replace_existing=True)

            print("Finished loading all jobs.")

    # Load initial jobs
    load_jobs(app.app_context())

    # Make the scheduler available to the rest of the app
    app.scheduler = scheduler

    return app
