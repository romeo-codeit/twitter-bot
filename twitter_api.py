# This module will handle all interactions with the Twitter API.
import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

# Add your Twitter API keys to the .env file
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET_KEY = os.getenv("TWITTER_API_SECRET_KEY")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

def get_twitter_api_v1():
    """
    Returns an authenticated Tweepy API object for v1.1 endpoint (used for media uploads).
    """
    auth = tweepy.OAuth1UserHandler(
        TWITTER_API_KEY, TWITTER_API_SECRET_KEY, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
    )
    return tweepy.API(auth)

def get_twitter_client_v2():
    """
    Returns an authenticated Tweepy Client object for v2 endpoint (used for creating tweets).
    """
    client = tweepy.Client(
        consumer_key=TWITTER_API_KEY,
        consumer_secret=TWITTER_API_SECRET_KEY,
        access_token=TWITTER_ACCESS_TOKEN,
        access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
    )
    return client

def post_tweet(content, image_path=None):
    """
    Posts a tweet with the given content and optional image.
    """
    if not all([TWITTER_API_KEY, TWITTER_API_SECRET_KEY, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET]):
        print("Twitter API credentials not found. Skipping tweet.")
        # In a real scenario, you might want to log this or handle it differently
        # For this project, we'll just print a message and not post.
        return

    try:
        client = get_twitter_client_v2()
        media_id = None
        if image_path:
            api_v1 = get_twitter_api_v1()
            media = api_v1.media_upload(filename=image_path)
            media_id = media.media_id

        if media_id:
            response = client.create_tweet(text=content, media_ids=[media_id])
        else:
            response = client.create_tweet(text=content)

        print(f"Successfully posted tweet: {content}")
        print(f"Tweet ID: {response.data['id']}")

    except tweepy.errors.TweepyException as e:
        print(f"Error posting tweet with Tweepy: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
