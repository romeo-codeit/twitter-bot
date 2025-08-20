# This module will handle fetching or generating images for the tweets.
import os
import requests
from dotenv import load_dotenv

load_dotenv()

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
UNSPLASH_URL = "https://api.unsplash.com/photos/random"

def get_image(query):
    """
    Fetches a random image from Unsplash for a given query, saves it locally,
    and returns the path.
    """
    if not UNSPLASH_ACCESS_KEY:
        print("Unsplash API key not found. Skipping image fetch.")
        return None

    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }
    params = {
        "query": query,
        "orientation": "landscape",
    }

    try:
        response = requests.get(UNSPLASH_URL, headers=headers, params=params, timeout=15)
        response.raise_for_status()  # Raise an exception for bad status codes

        data = response.json()
        if not data.get("urls") or not data["urls"].get("regular"):
            print(f"No image found for query: {query}")
            return None

        image_url = data["urls"]["regular"]

        # Download the image
        image_response = requests.get(image_url, stream=True, timeout=15)
        image_response.raise_for_status()

        # Save the image to a file
        image_path = "temp_image.jpg"
        with open(image_path, "wb") as f:
            for chunk in image_response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Successfully downloaded image for query '{query}' to {image_path}")
        return image_path

    except requests.exceptions.Timeout:
        print("Request to Unsplash API timed out.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image from Unsplash: {e}")
        return None
    except KeyError:
        # This can happen if Unsplash doesn't find a matching image and returns a different structure
        print(f"Could not find a relevant image for query: {query}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while handling image: {e}")
        return None
