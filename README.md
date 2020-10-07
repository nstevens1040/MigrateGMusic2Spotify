# MigrateGMusic2Spotify
Python script that parses your Google Play Music playlist names along with the titles of the songs in those playlists, creates Spotify playlists with the same names as your Google playlists, and then uses the song titles to search for your music on Spotify. If the search returns a result list, then the very first search result is added to the correct Spotify playlist. Ymmv with regard to whether the search will return accurate results.  

## I have confirmed that this script works on:
*   **Windows 10**  
*   **Windows Server 2016**  
*   **macOS Mojave**  
*   **Debian (KALI) Linux**  

## Requirements  
**Python 3**  
*   **macOS**  
paste the code below into bash  
```
cd ~/
curl "https://www.python.org/ftp/python/3.8.6/python-3.8.6-macosx10.9.pkg" --output "python-3.8.6-macosx10.9.pkg"
sudo installer -pkg ~/python-3.8.6-macosx10.9.pkg -target /
python3 -m pip install --upgrade pip
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
exit
```  
then, once the installation has completed, open another elevated PowerShell prompt and update pip to the latest version
```
python -m pip install --upgrade pip
```  
*   **Debian**  
paste the code below into bash  
```
cd ~/
sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get dist-upgrade -y && sudo apt-get autoremove -y
sudo apt-get install python3 -y
python3 -m pip install --upgrade pip
```  

**spotipy**  
```
pip3 install spotipy
```  
**gmusicapi**  
```
pip3 install gmusicapi
```  
To install both spotipy and gmusicapi at once. Use **Git** to clone this repository.  
```
git clone "https://github.com/nstevens1040/MigrateGMusic2Spotify.git"
cd MigrateGMusic2Spotify
pip3 install -r requirements.txt
```  

