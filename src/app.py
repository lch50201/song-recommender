import random
import requests
from flask import Flask, render_template, request, jsonify
from .models import Track
from .utils import get_api_key, pick_image, GENRES

app = Flask(__name__, template_folder="../ui/templates", static_folder="../ui/static")

BASE_URL = "https://ws.audioscrobbler.com/2.0/"


def fetch_recommendation(genre):
    """Fetch top tracks for a genre, return one at random as a Track."""
    try:
        api_key = get_api_key()
    except ValueError as e:
        return None, str(e)

    # Pick a random page (1–3) so results vary each time
    page = random.randint(1, 3)

    resp = requests.get(BASE_URL, params={
        "method":  "tag.gettoptracks",
        "tag":     genre,
        "api_key": api_key,
        "format":  "json",
        "limit":   50,
        "page":    page,
    })

    if resp.status_code == 403:
        return None, "Invalid API key. Check your .env file."
    if resp.status_code != 200:
        return None, f"API error ({resp.status_code}). Try again."

    data = resp.json()
    tracks_data = data.get("tracks", {}).get("track", [])

    if not tracks_data:
        return None, f"No tracks found for genre '{genre}'. Try another one."

    # Pick a random track from the results
    raw = random.choice(tracks_data)

    # Fetch richer track info (includes album art)
    info_resp = requests.get(BASE_URL, params={
        "method":  "track.getInfo",
        "artist":  raw["artist"]["name"],
        "track":   raw["name"],
        "api_key": api_key,
        "format":  "json",
    })

    image_url = None
    if info_resp.status_code == 200:
        info = info_resp.json().get("track", {})
        album_images = info.get("album", {}).get("image", [])
        image_url = pick_image(album_images)

    track = Track(
        title     = raw["name"],
        artist    = raw["artist"]["name"],
        genre     = genre.title(),
        listeners = raw.get("listeners", 0),
        url       = raw.get("url", "#"),
        image_url = image_url,
    )
    return track, None


@app.route("/")
def index():
    return render_template("index.html", genres=GENRES)


@app.route("/recommend", methods=["POST"])
def recommend():
    """AJAX endpoint — returns JSON so the page updates without a full reload."""
    genre = request.json.get("genre", "").strip().lower()
    if not genre:
        return jsonify({"error": "Please select a genre."}), 400

    track, error = fetch_recommendation(genre)
    if error:
        return jsonify({"error": error}), 500

    return jsonify(track.to_dict())


def run_app():
    print("\n  Song Recommender is running!")
    print("  Open your browser and go to: http://127.0.0.1:5000\n")
    app.run(debug=True)
