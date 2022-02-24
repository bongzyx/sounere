from app import db
from .Song import Song, song_artist
# from .Artist import Song, artist_album
from datetime import datetime

artist_album = db.Table('artist_album',
                        db.Column('artist_id', db.Integer,
                                  db.ForeignKey('artist.artist_id')),
                        db.Column('album_id', db.Integer,
                                  db.ForeignKey('album.album_id'))
                        )


class Artist(db.Model):
    __tablename__ = 'artist'
    artist_id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(120), nullable=False)
    added = db.Column(db.DateTime, default=datetime.today())
    song = db.relationship('Song', secondary=song_artist,
                           backref=db.backref('artist', lazy=True))

    def __repr__(self):
        return f"Artist('{self.artist_name}')"
