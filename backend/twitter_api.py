import tweepy

def get_twitter_api_v1(keys):
    """Returns an authenticated Tweepy API object for v1.1 (media uploads)."""
    auth = tweepy.OAuth1UserHandler(
        keys['api_key'], keys['api_secret'], keys['access_token'], keys['access_secret']
    )
    return tweepy.API(auth)

def get_twitter_client_v2(keys):
    """Returns an authenticated Tweepy Client object for v2 (creating tweets)."""
    client = tweepy.Client(
        consumer_key=keys['api_key'],
        consumer_secret=keys['api_secret'],
        access_token=keys['access_token'],
        access_token_secret=keys['access_secret'],
    )
    return client

def post_tweet_with_creds(keys, content, image_path=None):
    """
    Posts a tweet with the given content and optional image, using provided credentials.
    """
    if not all(keys.values()):
        raise ValueError("All Twitter API credentials are required.")

    client_v2 = get_twitter_client_v2(keys)
    media_id = None
    if image_path:
        api_v1 = get_twitter_api_v1(keys)
        try:
            media = api_v1.media_upload(filename=image_path)
            media_id = media.media_id
        except tweepy.errors.TweepyException as e:
            print(f"Error uploading media to Twitter: {e}")
            raise  # Re-raise the exception to be caught by the caller

    # The create_tweet method returns a Response object
    # The data attribute is a dict containing the tweet's ID and text
    if media_id:
        response = client_v2.create_tweet(text=content, media_ids=[media_id])
    else:
        response = client_v2.create_tweet(text=content)

    print(f"Tweet posted via Twitter API. ID: {response.data.get('id')}")
    return response
