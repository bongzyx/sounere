from email.mime import base
from flask import Blueprint, request, jsonify, url_for, abort, send_from_directory

from app import db, app
from ..models.User import User
from ..models.Song import Song, song_album, song_artist
from ..models.Album import Album
from ..models.Artist import Artist, artist_album
from pathlib import Path
import os
import glob


from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user

from ..utils.mp3_reader import SongReader

from tinytag import TinyTag

tools = Blueprint('tools', __name__, url_prefix='/tools')


@tools.get('/startScan')
def startScan():
    db.drop_all()
    db.create_all()

    path = "/Users/brandonong/Desktop/projects/sounere/api/app/test_mp3/"
    all_files = glob.glob(path + '**/*.mp3', recursive=True)

    for filepath in all_files:
        filename = os.path.basename(filepath)
        if not filename.startswith("._"):
            try:
                tag = TinyTag.get(filepath, image=True)
                print(f"{tag}\n\n")
            except:
                jsonify(error=len(all_files))
            print(type(tag.get_image()))

            # handle song
            add_song = Song(tag=tag, filepath=filepath, filename=filename)
            db.session.add(add_song)

            # handle album
            if Album.query.filter_by(album_name=tag.album if tag.album else "unknown").first():
                add_album = Album.query.filter_by(
                    album_name=tag.album if tag.album else "unknown").first()
                add_song.album.append(add_album)
            else:
                add_album = Album(
                    album_name=tag.album if tag.album else "unknown")
                db.session.add(add_album)
                add_song.album.append(add_album)

            # handle artists
            all_artists = tag.artist.split('; ') if tag.artist else filename.replace(
                ".mp3", '').split(" - ")[0]

            for artist in all_artists:
                if Artist.query.filter_by(artist_name=artist).first():
                    add_artist = Artist.query.filter_by(
                        artist_name=artist).first()
                    add_song.artist.append(
                        Artist.query.filter_by(artist_name=artist).first())
                    add_album.artist.append(
                        Artist.query.filter_by(artist_name=artist).first())
                else:
                    add_artist = Artist(artist_name=artist)
                    db.session.add(add_artist)
                    add_song.artist.append(add_artist)
                    add_album.artist.append(add_artist)

            db.session.commit()
    return jsonify(total_files=len(all_files))
