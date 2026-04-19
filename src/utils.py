import os
from dotenv import load_dotenv

load_dotenv()

GENRES = [
    "rock", "pop", "hip-hop", "jazz", "classical",
    "electronic", "metal", "r&b", "indie", "folk",
    "blues", "punk", "soul", "reggae", "country",
    "latin", "ambient", "disco", "funk", "alternative",
]


def get_api_key():
    key = os.getenv("LASTFM_API_KEY")
    if not key or key == "your_api_key_here":
        raise ValueError(
            "No API key found. Please edit your .env file.\n"
            "Get a free key at: https://www.last.fm/api/account/create"
        )
    return key


def pick_image(images):
    """Return the largest available image URL from a Last.fm image list."""
    for size in ("extralarge", "large", "medium"):
        for img in images:
            if img.get("size") == size and img.get("#text"):
                return img["#text"]
    return None
