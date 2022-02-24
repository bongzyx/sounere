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

search = Blueprint('search', __name__, url_prefix='/search')


@search.get("/any")
def searchAny():
    keyword = ""
    page = 1
    per_page = 20
    if request.args.get('keyword'):
        keyword = request.args.get('keyword')
    if request.args.get('page'):
        page = request.args.get('page')
    if request.args.get('per_page'):
        per_page = request.args.get('per_page')
    return searchAll(keyword, int(page), int(per_page))


def searchAll(keyword='', page=1, per_page=20):
    songs = Song.query.filter(Song.song_name.contains(
        keyword)).paginate(page, per_page=per_page)
    songs_list = []
    songs_dict = {}
    songs_total_pages = {
        'total_pages': songs.pages,
        'current_page': songs.page,
        'total_items': songs.total
    }

    for s in songs.items:
        art = []
        for a in s.artist:
            artist = {
                'artist_id': a.artist_id,
                'artist_name': a.artist_name
            }
            art.append(artist)
        alb = {
            'album_id': s.album[0].album_id,
            'album_name': s.album[0].album_name
        }
        songs_dict = {
            'song_id': s.song_id,
            'song_name': s.song_name,
            'song_length': s.song_length,
            'file_path': f'/request/{s.song_id}',
            'artists': art,
            'album': alb,
        }
        songs_list.append(songs_dict)

    artists = Artist.query.filter(Artist.artist_name.contains(
        keyword)).paginate(page, per_page=per_page)
    artists_list = []
    artists_dict = {}
    artists_total_pages = {
        'total_pages': artists.pages,
        'current_page': artists.page,
        'total_items': artists.total
    }
    for a in artists.items:
        artists_dict = {
            'artist_id': a.artist_id,
            'artist_name': a.artist_name,
        }
        artists_list.append(artists_dict)

    albums = Album.query.filter(Album.album_name.contains(
        keyword)).paginate(page, per_page=per_page)
    albums_list = []

    albums_total_pages = {
        'total_pages': albums.pages,
        'current_page': albums.page,
        'total_items': albums.total
    }
    for al in albums.items:
        al_song_list = []
        for _ in al.song:
            al_song_dict = {
                'song_id': _.song_id,
                'song_name': _.song_name,
            }
            al_song_list.append(al_song_dict)
        albums_dict = {
            'album_id': al.album_id,
            'album_name': al.album_name,
            'songs': al_song_list,
            'artist_id': al.song[0].artist[0].artist_id,
            'artist_name': al.song[0].artist[0].artist_name,
        }
        albums_list.append(albums_dict)

    return jsonify(
        songs={'total_pages': songs_total_pages, 'song_list': songs_list},
        artists={'total_pages': artists_total_pages,
                 'artist_list': artists_list},
        albums={'total_pages': albums_total_pages, 'album_list': albums_list})
