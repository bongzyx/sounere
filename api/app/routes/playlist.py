from email.mime import base
from flask import Blueprint, request, jsonify, url_for, abort, send_from_directory, make_response

from app import db, app
from ..models.User import User
from ..models.Song import Song, song_album, song_artist
from ..models.Album import Album
from ..models.Artist import Artist, artist_album
from pathlib import Path
import io
from tinytag import TinyTag
from PIL import Image

from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user

import random


playlist = Blueprint('playlist', __name__, url_prefix='/playlist')


@playlist.get("/random")
def randomSongs():
    count = int(request.args.get('count')) if request.args.get('count') else 50
    songs = Song.query.all()
    playlist = random.sample(songs, min(count, len(songs)))
    songs_list = []
    for s in playlist:
        art = []
        for a in s.artist:
            ia = {'artist_id': a.artist_id, 'artist_name': a.artist_name}
            art.append(ia)

        alb = s.album[0]
        songs_dict = {
            'song_id': s.song_id,
            'song_name': s.song_name,
            'song_length': s.song_length,
            'file_path': f'/request/{s.song_id}',
            'artists': art,
            'album_id': alb.album_id,
            'album_name': alb.album_name,
        }
        songs_list.append(songs_dict)

    return jsonify(songs_list)
