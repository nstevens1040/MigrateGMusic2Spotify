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

print("We need your Spotify username. By default, it is a random string of letters and numbers. \nIf you don't know what it is, then visit:\n    https://www.spotify.com/us/account/overview/\nand then find the value next to 'username'")
spuser = input("Enter your Spotify user id and strike 'Enter': ")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="dc0fc73dadcc4ddbbfd275a695e7a380",
                                               client_secret="844b859597ec4bbca0eb3c7d1ccb397d",
                                               redirect_uri="https://nstevens1040.github.io/OAuth2CodeParser/",
                                               scope="playlist-modify-public playlist-modify-private user-library-modify user-library-read"))

if not sys.platform == 'win32':
    gmlog = open(os.path.expanduser('~') + '/Desktop/GMusic.txt','w')
    splog = open(os.path.expanduser('~') + '/Desktop/Spotify.txt','w')
    csvlog = open(os.path.expanduser('~') + '/Desktop/Spotify_Playlist_Track_Log.csv','w')

if sys.platform == 'win32':
    gmlog = open(os.environ.get('userprofile') + "\\Desktop\\GMusic.txt", 'w')
    splog = open(os.environ.get('userprofile') + "\\Desktop\\Spotify.txt", 'w')
    csvlog = open(os.environ.get('userprofile') + "\\Desktop\\Spotify_Playlist_Track_Log.csv",'w')

csvlog.write("sep=\t\nPlaylist Name\tTrack Name\t\n")
songs = api.get_all_songs()
splaray = []
trxids = []
for i in sp.current_user_playlists(limit=None)['items']:
    splaray.append(i['name'])

for i in sp.current_user_saved_tracks(limit=None)['items']:
    trxids.append(i['track']['id'])

for i in api.get_all_user_playlist_contents():
    if not i['name'] in splaray:
        playlist=sp.user_playlist_create(spuser,i['name'],False)
        splog.write("created playlist: " + i['name'] + "\n")
        print("created playlist: " + i['name'])
    else:
        for p in sp.current_user_playlists(limit=None)['items']:
            if p['name'] == i['name']:
                playlist=sp.user_playlist(spuser, p['id'])
                splog.write("playlist exists: " + i['name'] + "\n")
                print("playlist exists: " + i['name'])
    gmlog.write("Playlist: " + i['name'] + "\n")
    trx = []
    for a in i['tracks']:
        for b in songs:
            if b['id'] == a['trackId']:
                track = b['title']
                gmlog.write("    " + track + "\n")
                print("performing Spotify search for: " + track)
                if track.endswith('mp3') and re.findall("\d\d\d\d\d\d\d\d\d\d\d\d\d",track):
                    track = track.strip('-').split('-')[0]
                if track.endswith('mp3'):
                    track = track.replace(".mp3","")
                results = sp.search(q=track,limit=50,offset=0,type='track')
                if results['tracks']['items']:
                    fullname=results['tracks']['items'][0]['name'] + " by " + results['tracks']['items'][0]['artists'][0]['name']
                    csvlog.write(playlist['name'] + "\t" + fullname + "\t\n")
                    trkid=results['tracks']['items'][0]['id']
                    splog.write("    " + fullname + "\n")
                    print("    found track on Spotify: " + fullname)
                    trx.append(trkid)
                    if not trkid in trxids:
                        sp.current_user_saved_tracks_add([trkid])
                        print("        Added track to library: " + fullname)
                        splog.write("        Added track to library: " + fullname + "\n")
                    else:
                        print("        Not adding duplicate to library: " + fullname)
                        splog.write("        Not adding duplicate to library: " + fullname + "\n")
                if not results['tracks']['items']:
                    splog.write("    No search results for: " + track + "\n")
                    print("    No search results for: " + track)
        pladded = []
        for z in sp.user_playlist_tracks(spuser,playlist['id'],fields=None,limit=None)['items']:
            pladded.append(z['track']['id'])
        if trx:
            for t in trx:
                if not t in pladded:
                    sp.user_playlist_add_tracks(spuser, playlist['id'], [t])
                    print("            Added: "  + fullname + "\n                to playlist: " + playlist['name'])
                    splog.write("            Added: "  + fullname + "\n                to playlist: " + playlist['name'] + "\n")
                else:
                    print("            Skipping track: " + fullname + "\n                already exists in playlist: " + playlist['name'])
                    splog.write("            Skipping track: " + fullname + "\n                already exists in playlist: " + playlist['name'] + "\n")
gmlog.close()
splog.close()
csvlog.close()