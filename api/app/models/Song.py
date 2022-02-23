from app import db


class Song(db.Model):
    __tablename__ = 'song'
    song_id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String(120), nullable=False)
    song_length = db.Column(db.String(), nullable=False)
    file_path = db.Column(db.String, nullable=False)
    added = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f"Song('{self.song_name}')"
