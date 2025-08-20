import random
from .database import get_db
from .encryption import decrypt_data
from . import twitter_api as twitter
from . import image_handler

def post_tweet_for_user(user_id):
    """
    The core logic for posting a single tweet for a given user.
    This function is designed to be called by the scheduler.
    """
    print(f"--- Running tweet job for user_id: {user_id} ---")
    db = get_db()

    # 1. Get user's credentials
    user = db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
    if not user:
        print(f"Job failed: User with id {user_id} not found.")
        return

    try:
        api_key = decrypt_data(user['twitter_api_key'])
        api_secret = decrypt_data(user['twitter_api_secret_key'])
        access_token = decrypt_data(user['twitter_access_token'])
        access_secret = decrypt_data(user['twitter_access_token_secret'])
        unsplash_key = user['unsplash_access_key'] # Assuming this is not encrypted
    except (TypeError, ValueError) as e:
        print(f"Job failed for user {user_id}: Could not decrypt credentials. Error: {e}")
        # Log this failure to the database
        # db.execute(...)
        return

    # 2. Get a piece of content from the user's queue
    content_item = db.execute(
        'SELECT * FROM content_queue WHERE user_id = ? AND is_posted = 0 ORDER BY RANDOM() LIMIT 1',
        (user_id,)
    ).fetchone()

    if not content_item:
        print(f"Job failed for user {user_id}: No available content in queue.")
        return

    tweet_text = content_item['content']
    category = content_item['category']

    # 3. Get an image
    image_path = None
    if unsplash_key:
        # We can use the category as the query for the image
        image_path = image_handler.get_image_from_unsplash(category, unsplash_key)

    # 4. Post the tweet
    try:
        # We need to refactor the twitter_api to accept credentials
        response = twitter.post_tweet_with_creds(
            keys={
                'api_key': api_key,
                'api_secret': api_secret,
                'access_token': access_token,
                'access_secret': access_secret,
            },
            content=tweet_text,
            image_path=image_path
        )

        # 5. Log success to database
        db.execute(
            """
            INSERT INTO posted_tweets (user_id, content_id, tweet_text, tweet_id_str, status)
            VALUES (?, ?, ?, ?, 'Success')
            """,
            (user_id, content_item['id'], tweet_text, response.data['id'])
        )
        # Mark content as posted
        db.execute('UPDATE content_queue SET is_posted = 1 WHERE id = ?', (content_item['id'],))
        db.commit()
        print(f"Successfully posted tweet for user {user_id}.")

    except Exception as e:
        print(f"Job failed for user {user_id}: Error posting tweet. Error: {e}")
        # 5b. Log failure to database
        db.execute(
            """
            INSERT INTO posted_tweets (user_id, content_id, tweet_text, status, error_message)
            VALUES (?, ?, ?, 'Failed', ?)
            """,
            (user_id, content_item['id'], tweet_text, str(e))
        )
        db.commit()

    finally:
        # 6. Clean up image if it was downloaded
        if image_path and os.path.exists(image_path):
            os.remove(image_path)


def check_and_reply_to_mentions(user_id):
    """
    Checks for recent mentions and replies with a random template.
    """
    print(f"--- Running auto-reply job for user_id: {user_id} ---")
    db = get_db()

    # 1. Get user's credentials
    user = db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
    if not user or not user['twitter_api_key']:
        print(f"Job failed: User {user_id} not found or has no Twitter credentials.")
        return

    try:
        keys = {
            'api_key': decrypt_data(user['twitter_api_key']),
            'api_secret': decrypt_data(user['twitter_api_secret_key']),
            'access_token': decrypt_data(user['twitter_access_token']),
            'access_secret': decrypt_data(user['twitter_access_token_secret']),
        }
        client = twitter.get_twitter_client_v2(keys)
        me = client.get_me().data
        my_user_id = me.id
    except Exception as e:
        print(f"Job failed for user {user_id}: Could not get Twitter client. Error: {e}")
        return

    # 2. Get user's reply templates
    templates = db.execute(
        'SELECT template_text FROM auto_reply_templates WHERE user_id = ? AND is_active = 1',
        (user_id,)
    ).fetchall()
    if not templates:
        print(f"Job failed for user {user_id}: No active reply templates found.")
        return

    # 3. Get recent mentions
    try:
        # This fetches tweets where the user was mentioned.
        mentions = client.get_users_mentions(id=my_user_id, expansions=["author_id"]).data
        if not mentions:
            print(f"No new mentions found for user {user_id}.")
            return

        for mention in mentions:
            # 4. Check if we've already replied
            already_replied = db.execute(
                'SELECT id FROM replied_to_tweets WHERE tweet_id_str = ?', (mention.id,)
            ).fetchone()

            if not already_replied:
                # 5. Select a random template and post the reply
                reply_text = f"@{mention.author.username} {random.choice(templates)['template_text']}"

                client.create_tweet(text=reply_text, in_reply_to_tweet_id=mention.id)

                # 6. Log the reply to our database
                db.execute(
                    'INSERT INTO replied_to_tweets (user_id, tweet_id_str) VALUES (?, ?)',
                    (user_id, str(mention.id))
                )
                db.commit()
                print(f"Replied to tweet {mention.id} for user {user_id}.")

    except Exception as e:
        print(f"Job failed for user {user_id}: Error fetching or replying to mentions. Error: {e}")
