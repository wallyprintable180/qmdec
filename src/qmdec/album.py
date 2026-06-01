"""Batch album download with concurrent workers."""

import json
import sys
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def get_singer_albums(singer_mid: str, cookie: str, uin: str) -> list[dict]:
    url = "https://u.y.qq.com/cgi-bin/musicu.fcg"
    albums = []
    page = 0
    while True:
        data = {
            "comm": {"cv": 4747474, "ct": 24, "format": "json", "uin": int(uin)},
            "req_1": {
                "module": "music.musichallAlbum.AlbumListServer",
                "method": "GetAlbumList",
                "param": {"singerMid": singer_mid, "begin": page * 80, "num": 80,
                          "order": 0, "songNumTag": 0},
            },
        }
        req = urllib.request.Request(url, json.dumps(data).encode(), method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Cookie", cookie)
        resp = urllib.request.urlopen(req, timeout=15)
        result = json.loads(resp.read())
        album_list = result.get("req_1", {}).get("data", {}).get("albumList", [])
        if not album_list:
            break
        for a in album_list:
            albums.append({"mid": a["albumMid"], "name": a["albumName"]})
        if len(album_list) < 80:
            break
        page += 1
    return albums


def get_album_songs(album_mid: str, cookie: str, uin: str) -> list[dict]:
    url = "https://u.y.qq.com/cgi-bin/musicu.fcg"
    songs = []
    page = 0
    while True:
        data = {
            "comm": {"cv": 4747474, "ct": 24, "format": "json", "uin": int(uin)},
            "req_1": {
                "module": "music.musichallAlbum.AlbumSongList",
                "method": "GetAlbumSongList",
                "param": {"albumMid": album_mid, "begin": page * 100, "num": 100, "order": 2},
            },
        }
        req = urllib.request.Request(url, json.dumps(data).encode(), method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Cookie", cookie)
        resp = urllib.request.urlopen(req, timeout=15)
        result = json.loads(resp.read())
        song_list = result.get("req_1", {}).get("data", {}).get("songList", [])
        if not song_list:
            break
        for s in song_list:
            info = s.get("songInfo", s)
            file_info = info.get("file", {})
            if not file_info.get("size_flac", 0):
                continue
            songs.append({
                "title": info.get("title", ""),
                "singer": "/".join(x.get("title", "") for x in info.get("singer", [])),
                "song_mid": info.get("mid", ""),
                "media_mid": file_info.get("media_mid", ""),
                "song_info": info,
            })
        if len(song_list) < 100:
            break
        page += 1
    return songs
