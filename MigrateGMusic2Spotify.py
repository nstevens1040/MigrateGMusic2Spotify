from gmusicapi import Mobileclient
import tkinter as tk
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import re
import sys
import io

def dialog1(message):
    master = tk.Tk()
    master.title("GoogleMusic2Spotify")
    tk.Label(master,
        text=message).grid(row=0)
    tk.Button(master,
        text="Ok",command=master.destroy).grid(row=1)
    master.attributes("-topmost", True)

api = Mobileclient()
if not api.oauth_login(api.FROM_MAC_ADDRESS):
    ret = dialog1("Once you have authorized access to Google Music you will be given a code. \nCopy the code, return to the shell that is running your Python script, \npaste the code, and strike Enter.")
    if sys.platform == 'darwin':
        os.system('open "https://accounts.google.com/o/oauth2/v2/auth?client_id=228293309116.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fskyjam&access_type=offline&response_type=code"')
    if sys.platform == 'win32':
        os.system('if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" ( "C:\Program Files\Google\Chrome\Application\chrome.exe" "https://accounts.google.com/o/oauth2/v2/auth?client_id=228293309116.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fskyjam&access_type=offline&response_type=code" ) else ( "C:\Program Files (x86)\Internet Explorer\iexplore.exe" "https://accounts.google.com/o/oauth2/v2/auth?client_id=228293309116.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fskyjam&access_type=offline&response_type=code")')
    login=api.perform_oauth()
    api.oauth_login(api.FROM_MAC_ADDRESS)

spuser = input("Enter your Spotify user id and strike 'Enter'(it's a random string of letters and numbers and not your email address): ")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="dc0fc73dadcc4ddbbfd275a695e7a380",
                                               client_secret="844b859597ec4bbca0eb3c7d1ccb397d",
                                               redirect_uri="https://nanick.org",
                                               scope="playlist-modify-public playlist-modify-private"))

if not sys.platform == 'win32':
    gmlog = open(os.path.expanduser('~') + '/Desktop/GMusic.txt','w')
    splog = open(os.path.expanduser('~') + '/Desktop/Spotify.txt','w')

if sys.platform == 'win32':
    gmlog = open(os.environ.get('userprofile') + "\\Desktop\\GMusic.txt", 'w')
    splog = open(os.environ.get('userprofile') + "\\Desktop\\Spotify.txt", 'w')

songs = api.get_all_songs()
for i in api.get_all_user_playlist_contents():
    playlist=sp.user_playlist_create(spuser,i['name'])
    gmlog.write("Playlist: " + i['name'] + "\n")
    splog.write("created playlist: " + i['name'] + "\n")
    print("created playlist: " + i['name'])
    trx = []
    for a in i['tracks']:
        for b in songs:
            if b['id'] == a['trackId']:
                track = b['title']
                gmlog.write("    " + track + "\n")
                print("performing Spotify search for: " + track)
                if track.endswith('mp3') and re.findall("\d\d\d\d\d\d\d\d\d\d\d\d\d",track):
                    track = track.strip('-').split('-')[0]
                results = sp.search(q=track,limit=50,offset=0,type='track')
                if results:
                    splog.write("    " + results['tracks']['items'][0]['name'] + " by " + results['tracks']['items'][0]['artists'][0]['name'])
                    print("found track on Spotify: " + results['tracks']['items'][0]['name'] + " by " + results['tracks']['items'][0]['artists'][0]['name'])
                    trx.append(results['tracks']['items'][0]['id'])
    sp.current_user_saved_tracks_add(trx)
    sp.user_playlist_add_tracks(spuser, playlist['id'], trx)

gmlog.close()
splog.close()


