import sqlite3
import click
from flask import current_app, g

def get_db():
    """
    Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config.get('DATABASE', 'tweets.db'),
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """
    If this request connected to the database, close the
    connection.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Clear existing data and create new tables."""
    db = get_db()
    # The schema will be expanded later for users, etc.
    with current_app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())

@click.command('init-db')
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    """Register database functions with the Flask app."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

# --- Functions from the old bot logic ---
# These will be adapted to use the new get_db() function

def add_tweet_to_db(content):
    """Adds a tweet to the database."""
    db = get_db()
    db.execute("INSERT INTO posted_tweets (content) VALUES (?)", (content,))
    db.commit()

def is_duplicate_in_db(content):
    """Checks if a tweet with the same content has already been posted."""
    db = get_db()
    result = db.execute(
        "SELECT id FROM posted_tweets WHERE content = ?", (content,)
    ).fetchone()
    return result is not None
