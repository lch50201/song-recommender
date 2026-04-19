from src.models import Track
from src.utils import pick_image, GENRES


def test_track_to_dict_formats_listeners():
    track = Track(
        title="Blue in Green", artist="Miles Davis",
        genre="Jazz", listeners="1500000",
        url="https://last.fm", image_url=None,
    )
    d = track.to_dict()
    assert d["listeners"] == "1,500,000"
    assert d["title"] == "Blue in Green"


def test_track_to_dict_unknown_listeners():
    track = Track("Song", "Artist", "Rock", None, "#", None)
    assert track.to_dict()["listeners"] == "Unknown"


def test_genres_list_not_empty():
    assert len(GENRES) > 0
    assert "rock" in GENRES
    assert "jazz" in GENRES


def test_pick_image_prefers_extralarge():
    images = [
        {"size": "medium",     "#text": "med.jpg"},
        {"size": "extralarge", "#text": "xl.jpg"},
        {"size": "large",      "#text": "lg.jpg"},
    ]
    assert pick_image(images) == "xl.jpg"


def test_pick_image_falls_back():
    images = [{"size": "large", "#text": "lg.jpg"}]
    assert pick_image(images) == "lg.jpg"


def test_pick_image_returns_none_if_empty():
    assert pick_image([]) is None
