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

metadata = Blueprint('metadata', __name__, url_prefix='/metadata')


@metadata.get("/allTracks")
def getAllTracks():
    keyword = ""
    page = 1
    per_page = 20
    if request.args.get('keyword'):
        keyword = request.args.get('keyword')
    if request.args.get('page'):
        page = request.args.get('page')
    if request.args.get('per_page'):
        per_page = request.args.get('per_page')
    return allTracks(keyword, int(page), int(per_page))


@metadata.get("/allArtists")
def getAllArtists():
    keyword = ""
    page = 1
    per_page = 20
    if request.args.get('keyword'):
        keyword = request.args.get('keyword')
    if request.args.get('page'):
        page = request.args.get('page')
    if request.args.get('per_page'):
        per_page = request.args.get('per_page')
    return allArtists(keyword, int(page), int(per_page))


@metadata.get("/allAlbums")
def getAllAlbums():
    keyword = ""
    page = 1
    per_page = 20
    if request.args.get('keyword'):
        keyword = request.args.get('keyword')
    if request.args.get('page'):
        page = request.args.get('page')
    if request.args.get('per_page'):
        per_page = request.args.get('per_page')
    return allAlbums(keyword, int(page), int(per_page))


@metadata.get("/singleArtist/<int:id>")
def getSingleArtist(id):
    return singleArtist(id)


@metadata.get("/singleAlbum/<int:id>")
def getSingleAlbum(id):
    return singleAlbum(id)


def allArtists(keyword='', page=1, per_page=20):

    artists = Artist.query.filter(Artist.artist_name.contains(
        keyword)).paginate(page, per_page=per_page)
    artists_list = []
    artists_dict = {}
    total_pages = {
        'total_pages': artists.pages,
        'current_page': artists.page,
        'total_items': artists.total
    }
    for a in artists.items:
        artists_dict = {
            'artist_id': a.artist_id,
            'artist_name': a.artist_name,
            'total_tracks': len(a.song)
        }
        artists_list.append(artists_dict)

    return jsonify(total_pages, artists_list)


def singleArtist(id):
    artist = Artist.query.filter_by(artist_id=id).first()
    album_list = []
    album_dict = {}

    artist_info = {
        'artist_name': artist.artist_name,
        'artist_id': artist.artist_id,
    }

    for al in artist.album:
        album_songs = []

        for al_song in al.song:
            song_artists = []
            for sa in al_song.artist:
                song_artists.append(
                    {'artist_id': sa.artist_id, 'artist_name': sa.artist_name})

            alb_song = {'song_id': al_song.song_id,
                        'song_name': al_song.song_name, 'artists': song_artists, }
            album_songs.append(alb_song)

        album_dict = {
            'album_id': al.album_id,
            'album_name': al.album_name,
            'album_songs': album_songs,
        }
        album_list.append(album_dict)

    return jsonify([artist_info, album_list])


def singleAlbum(id):
    album = Album.query.filter_by(album_id=id).first()
    album_dict = {}
    song_list = []

    for al in album.song:
        song_artists = []
        for song_artist in al.artist:
            song_artists.append(
                {'artist_id': song_artist.artist_id, 'artist_name': song_artist.artist_name})

        song_dict = {'song_id': al.song_id,
                     'song_name': al.song_name, 'artists': song_artists}
        song_list.append(song_dict)

    for ar in album.artist:
        artist_list = []
        artist_dict = {'artist_id': ar.artist_id,
                       'artist_name': ar.artist_name}
        artist_list.append(artist_dict)

    album_dict = {
        'artists': artist_list,
        'songs': song_list,
        'album_name': album.album_name,
        'album_id': album.album_id,
    }

    return jsonify(album_dict)


def allTracks(keyword='', page=1, per_page=20):
    songs = Song.query.filter(Song.song_name.contains(
        keyword)).paginate(page, per_page=per_page)
    songs_list = []
    songs_dict = {}
    total_pages = {
        'total_pages': songs.pages,
        'current_page': songs.page,
        'total_items': songs.total
    }

    for s in songs.items:
        art = []
        for a in s.artist:
            art_dict = {
                'artist_id': a.artist_id,
                'artist_name': a.artist_name,
            }
            art.append(art_dict)
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

    return jsonify(total_pages, songs_list)


def allAlbums(keyword='', page=1, per_page=20):
    albums = Album.query.filter(Album.album_name.contains(
        keyword)).paginate(page, per_page=per_page)
    album_list = []
    album_dict = {}
    total_pages = {
        'total_pages': albums.pages,
        'current_page': albums.page,
        'total_items': albums.total
    }

    for al in albums.items:
        art = []
        for a in al.artist:
            art_dict = {
                'artist_id': a.artist_id,
                'artist_name': a.artist_name,
            }
            art.append(art_dict)

        songs = []
        for s in al.song:
            song_dict = {
                'song_id': s.song_id,
                'song_name': s.song_name,
            }
            songs.append(song_dict)
        album_dict = {
            'album_id': al.album_id,
            'album_name': al.album_name,
            'artists': art,
            'songs': songs,
        }
        album_list.append(album_dict)

    return jsonify(total_pages, album_list)
