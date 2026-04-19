class Track:
    """Represents a recommended music track."""

    def __init__(self, title, artist, genre, listeners, url, image_url):
        self.title     = title
        self.artist    = artist
        self.genre     = genre
        self.listeners = listeners
        self.url       = url
        self.image_url = image_url

    def to_dict(self):
        return {
            "title":     self.title,
            "artist":    self.artist,
            "genre":     self.genre,
            "listeners": f"{int(self.listeners):,}" if self.listeners else "Unknown",
            "url":       self.url,
            "image_url": self.image_url,
        }
