from email.policy import default
from app import db
from datetime import datetime
import time

song_artist = db.Table('song_artist',
                       db.Column('song_id', db.Integer,
                                 db.ForeignKey('song.song_id')),
                       db.Column('artist_id', db.Integer,
                                 db.ForeignKey('artist.artist_id'))
                       )

song_album = db.Table('song_album',
                      db.Column('song_id', db.Integer,
                                db.ForeignKey('song.song_id')),
                      db.Column('album_id', db.Integer,
                                db.ForeignKey('album.album_id'))
                      )


class Song(db.Model):
    __tablename__ = 'song'
    song_id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String, nullable=False)
    song_length = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=True)
    lyrics = db.Column(db.String, nullable=True)
    filesize = db.Column(db.Integer, nullable=False)
    bitrate = db.Column(db.Integer, nullable=False)
    file_path = db.Column(db.String, nullable=False)
    album_art = db.Column(db.Boolean, nullable=False, default=False)
    added = db.Column(db.DateTime, default=datetime.today())

    def __repr__(self):
        return f"Song('{self.song_name}')"

    def __init__(self, tag, filepath, filename):
        self.song_name = tag.title if tag.title else filename.replace(
            ".mp3", '').split(" - ")[1]
        self.song_length = time.strftime(
            '%M:%S', time.gmtime(int(tag.duration)))
        self.year = tag.year
        self.lyrics = tag.extra.get('lyrics')
        self.filesize = tag.filesize
        self.bitrate = tag.bitrate
        self.file_path = filepath
        self.album_art = True if tag.get_image() else False
