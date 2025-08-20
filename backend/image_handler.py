import os
import requests

UNSPLASH_URL = "https://api.unsplash.com/photos/random"

def get_image_from_unsplash(query: str, unsplash_key: str):
    """
    Fetches a random image from Unsplash for a given query, saves it locally,
    and returns the path. Requires an Unsplash API key.
    """
    if not unsplash_key:
        print("Unsplash API key not provided. Skipping image fetch.")
        return None

    headers = {"Authorization": f"Client-ID {unsplash_key}"}
    params = {"query": query, "orientation": "landscape"}

    try:
        response = requests.get(UNSPLASH_URL, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        if not data.get("urls") or not data["urls"].get("regular"):
            print(f"No image found for query: {query}")
            return None

        image_url = data["urls"]["regular"]
        image_response = requests.get(image_url, stream=True, timeout=15)
        image_response.raise_for_status()

        # Save the image to a temporary file
        image_path = f"temp_image_{os.urandom(8).hex()}.jpg"
        with open(image_path, "wb") as f:
            for chunk in image_response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Successfully downloaded image for query '{query}' to {image_path}")
        return image_path

    except requests.exceptions.RequestException as e:
        print(f"Error fetching image from Unsplash: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while handling image: {e}")
        return None
