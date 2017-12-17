import os
import time
from multiprocessing import Process

import spotipy
from spotipy import util

from Utils.file_utils import combine_files, create_file_if_not_exist
from Utils.utils import log

SONGS_PATH = "E:\Google_drive\Songs\songsList.txt"
FOLDER_PATH = "E:\Google_drive\Songs\\"
FILE_PATH = "E:\Google_drive\Songs\songsIDs.txt"


class SpotifyApi:

    def get_token(self, user_name, client_id, client_secret, redirect_uri):
        """https://developer.spotify.com/web-api/using-scopes/"""
        scope = 'playlist-modify-public'
        token = util.prompt_for_user_token(username=user_name, scope=scope, client_id=client_id,
                                           client_secret=client_secret, redirect_uri=redirect_uri)
        if token:
            return token

        else:
            log("Can't get token for", user_name)

    def __init__(self, user_name, client_id, client_secret, redirect_uri):
        self.user_name = user_name
        token = self.get_token(user_name, client_id, client_secret, redirect_uri)
        self.sp = spotipy.Spotify(auth=token)

    def get_playlists(self):
        return self.sp.current_user_playlists()

    def get_tracks_ids(self, tracks_list):
        id_map = map(self.sp.search, tracks_list)
        ids = []
        for track in list(id_map):
            try:
                ids.append(track['tracks']['items'][0]['id'])
            except Exception as ex:
                print(ex)
                continue
        return ids

    def save_tracks_ides_to_file(self, tracks_list, file_name):
        create_file_if_not_exist(file_name)
        with open(file_name, "a")as f1:
            for line in self.get_tracks_ids(tracks_list):
                f1.write(line + "\n")
                f1.flush()

    def create_playlist(self, name, public=True, ):
        return self.sp.user_playlist_create(user_name, name, public)

    def add_tracks(self, play_list_id, tracks_ides):
        self.sp.user_playlist_add_tracks(user=self.user_name, playlist_id=play_list_id, tracks=tracks_ides)


def distribution(parts, target, tracks_list, min_=1, max=1, ):
    rest = max % parts
    min = min_
    inc = (max - min_) // parts
    max = min_ + inc
    processes = []
    for i in range(1, parts + 1):
        tracks_list_siced = tracks_list[min: max]
        if i == parts: max = max + rest
        process = Process(target=target, args=(tracks_list_siced, FOLDER_PATH + "song_ides%s.txt" % str(i)))
        max = max + inc
        min = min + inc
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()


def songs_ides_distributed(sa):
    with open(SONGS_PATH) as songs_file:
        count = sum(1 for line in songs_file)
        songs_file.seek(0)
        songs = songs_file.readlines()

    ides = 1496
    songs_count = ides + 200
    while ides < count:
        distribution(pool_count, sa.save_tracks_ides_to_file, songs, min_=ides, max=songs_count)
        ides = songs_count
        songs_count = songs_count + 200
        time.sleep(5)

    combine_files(pool_count, FILE_PATH, FOLDER_PATH, "song_ides")


if __name__ == "__main__":
    with open('auth.txt') as aut:
        user_name = aut.readline().strip()
        client_id = aut.readline().strip()
        client_secret = aut.readline().strip()
        redirect_uri = aut.readline().strip()

    pool_count = 10
    sa = SpotifyApi(user_name, client_id, client_secret, redirect_uri)
    if not os.path.isfile(FILE_PATH):
        songs_ides_distributed(sa)

    # play_list_id = sa.create_playlist("My_all")