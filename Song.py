class Song:
    def __init__(self, title, artist, album, url, id):
        self.title = title
        self.artist = artist
        self.album = album
        self.url = url
        self.id = id

    def __repr__(self):
        return f"{self.title} by {', '.join(self.artist)} - Album: {self.album}, url - {self.url}\n\n"