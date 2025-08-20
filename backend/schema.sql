-- Drop tables in reverse order of dependency to avoid foreign key constraints
DROP TABLE IF EXISTS posted_tweets;
DROP TABLE IF EXISTS content_queue;
DROP TABLE IF EXISTS threads;
DROP TABLE IF EXISTS schedule;
DROP TABLE IF EXISTS user;

-- User table remains the same
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    twitter_api_key TEXT,
    twitter_api_secret_key TEXT,
    twitter_access_token TEXT,
    twitter_access_token_secret TEXT,
    unsplash_access_key TEXT
);

-- Schedule table remains the same
CREATE TABLE schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    post_time TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

-- New table for threads
CREATE TABLE threads (
    id TEXT PRIMARY KEY, -- Using TEXT for UUIDs
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

-- Updated content queue table for threads
CREATE TABLE content_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    content TEXT NOT NULL,
    is_posted BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    -- Link to a thread (optional)
    thread_id TEXT,
    order_in_thread INTEGER, -- The order of the tweet in the thread (0, 1, 2...)
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (thread_id) REFERENCES threads (id) ON DELETE CASCADE
);

-- History of posted tweets
CREATE TABLE posted_tweets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    content_id INTEGER,
    tweet_text TEXT NOT NULL,
    tweet_id_str TEXT,
    posted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL,
    error_message TEXT,
    -- Add thread info for context
    thread_id TEXT,
    in_reply_to_tweet_id_str TEXT,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (content_id) REFERENCES content_queue (id)
);

-- Tables for Auto-Reply Feature
CREATE TABLE auto_reply_settings (
    user_id INTEGER PRIMARY KEY,
    is_active BOOLEAN NOT NULL DEFAULT 0,
    reply_frequency_minutes INTEGER NOT NULL DEFAULT 15,
    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
);

CREATE TABLE auto_reply_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    template_text TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
);

CREATE TABLE replied_to_tweets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    tweet_id_str TEXT UNIQUE NOT NULL,
    replied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
);
