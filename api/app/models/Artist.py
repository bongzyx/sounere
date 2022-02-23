from app import db


class Artist(db.Model):
    __tablename__ = 'artist'
    artist_id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(120), nullable=False)
    added = db.Column(db.Time, nullable=False)
    song = db.relationship('Song', secondary=song_artist,
                           backref=db.backref('artist', lazy=True))

    def __repr__(self):
        return f"Artist('{self.artist_name}')"
