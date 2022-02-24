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

requests = Blueprint('requests', __name__, url_prefix='/requests')


@requests.get("/song/<int:id>")
def request_song(id):
    song_url = (Song.query.get_or_404(id)).file_path
    p = Path(song_url)
    print(p)
    return send_from_directory(p.parent, p.name, mimetype='audio/mpeg')


@requests.route("/albumArt/<int:id>")
def get_album_art(id):
    print(request)
    size = int(request.args.get('size')) if request.args.get('size') else 256

    filepath = (Song.query.get_or_404(id)).file_path
    tags = TinyTag.get(filepath, image=True)

    album_art = tags.get_image()

    if album_art:
        pict = Image.open(io.BytesIO(album_art))
    else:
        pict = Image.open('music.png', mode='r')

    imgByteArr = io.BytesIO()
    pict.thumbnail((size, size))
    pict.save(imgByteArr, format='PNG')
    pict = imgByteArr.getvalue()

    response = make_response(pict)
    response.headers.set('Content-Type', 'image/jpeg')

    return response
