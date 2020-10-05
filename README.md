# MigrateGMusic2Spotify
Python script that effectively copies all playlists and music from Google Play Music to Spotify

## Requirements  
  **Python 3**  
*   **macOS**  
paste the code below into bash  
```
cd ~/
wget "https://www.python.org/ftp/python/3.8.6/python-3.8.6-macosx10.9.pkg"
sudo installer -pkg ~/python-3.8.6-macosx10.9.pkg -target /
```  
*   **Windows**  
paste the code below into an elevated PowerShell prompt  
```
([System.Net.WebClient]@{Proxy=$null;}).DownloadFile(
    "https://www.python.org/ftp/python/3.8.6/python-3.8.6.exe",
    "$($ENV:USERPROFILE)\Downloads\python-3.8.6.exe"
)
while(![System.IO.File]::Exists("$($ENV:USERPROFILE)\Downloads\python-3.8.6.exe")){
    sleep -m 500
}
. "$($ENV:USERPROFILE)\Downloads\python-3.8.6.exe" /passive InstallAllUsers=1 PrependPath=1 Include_debug=1 Include_symbols=1
```
*   **spotipy**  
```
       pip3 install spotipy
```
*   **gmusicapi**  
```
       pip3 install gmusicapi
```
