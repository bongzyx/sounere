from email.policy import default
from app import db
from .Song import Song, song_album
from .Artist import Song, artist_album
from datetime import datetime


class Album(db.Model):
    __tablename__ = 'album'
    album_id = db.Column(db.Integer, primary_key=True)
    album_name = db.Column(db.String(120), nullable=False)
    added = db.Column(db.DateTime, default=datetime.today())
    song = db.relationship('Song', secondary=song_album,
                           backref=db.backref('album', lazy=True))
    artist = db.relationship(
        'Artist', secondary=artist_album, backref=db.backref('album', lazy=True))

    def __repr__(self):
        return f"Album('{self.album_name}')"
