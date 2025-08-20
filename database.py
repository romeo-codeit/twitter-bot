# This module will manage the database for storing posted tweets to avoid duplicates.
import sqlite3

def init_db():
    """
    Initializes the database.
    """
    conn = sqlite3.connect("tweets.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS posted_tweets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_tweet(content):
    """
    Adds a tweet to the database.
    """
    conn = sqlite3.connect("tweets.db")
    c = conn.cursor()
    c.execute("INSERT INTO posted_tweets (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()

def is_duplicate(content):
    """
    Checks if a tweet with the same content has already been posted.
    """
    conn = sqlite3.connect("tweets.db")
    c = conn.cursor()
    c.execute("SELECT * FROM posted_tweets WHERE content = ?", (content,))
    result = c.fetchone()
    conn.close()
    return result is not None
