from app import db


class Playlist(db.Model):
    __tablename__ = 'playlist'
    playlist_id = db.Column(db.Integer, primary_key=True)
    playlist_name = db.Column(db.String(120), nullable=False)
    playlist_count = db.Column(db.String(), nullable=False)
    created_date = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f"Playlist('{self.playlist_name}')"
