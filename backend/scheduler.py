# This module will handle the scheduling of the tweets.
import schedule
import time
import random
import os

from content_generator import get_random_category, generate_content
from image_handler import get_image
from twitter_api import post_tweet
from database import init_db, add_tweet, is_duplicate

# A mapping from our content categories to broader Unsplash search queries
CATEGORY_TO_IMAGE_QUERY = {
    "my_journey": "programming, laptop",
    "apps_built": "software development, code",
    "tech_tips": "code, computer",
    "tech_news": "technology, news",
    "tech_stories": "history, technology",
    "ethical_hacking": "hacker, cybersecurity",
    "cracked_apps": "security, warning sign",
    "general_tech": "future technology, innovation",
}

def post_new_tweet_job():
    """
    The main job to be scheduled. Generates content, fetches an image,
    and posts a tweet.
    """
    print("\n--- Starting new tweet job ---")

    max_retries = 5
    for i in range(max_retries):
        category = get_random_category()
        content = generate_content(category)

        if not is_duplicate(content):
            print(f"Generated unique content from category '{category}':\n{content}")

            # Get an image for the tweet
            image_query = CATEGORY_TO_IMAGE_QUERY.get(category, "technology")
            image_path = get_image(image_query)

            # Post the tweet
            post_tweet(content, image_path)

            # Add to database to prevent duplicates
            add_tweet(content)

            # Clean up the downloaded image file
            if image_path and os.path.exists(image_path):
                try:
                    os.remove(image_path)
                    print(f"Removed temporary image file: {image_path}")
                except OSError as e:
                    print(f"Error removing temporary image file: {e}")

            print("--- Tweet job finished successfully ---")
            return # Exit the function after a successful post
        else:
            print(f"Content is a duplicate, retrying... ({i + 1}/{max_retries})")
            time.sleep(1) # Wait a second before retrying

    print(f"--- Tweet job failed after {max_retries} retries to find unique content ---")


def run_scheduler():
    """
    Sets up the schedule and runs the main loop.
    """
    print("Scheduler started. Initializing database...")
    init_db()

    # Schedule the job at different times of the day as requested
    schedule.every().day.at("09:00").do(post_new_tweet_job)
    schedule.every().day.at("15:00").do(post_new_tweet_job)
    schedule.every().day.at("21:00").do(post_new_tweet_job)

    print("Jobs scheduled for 09:00, 15:00, and 21:00 daily.")

    # For demonstration, you might want to run a job immediately
    # print("Running a test job now...")
    # post_new_tweet_job()

    while True:
        schedule.run_pending()
        time.sleep(60) # Check every minute
