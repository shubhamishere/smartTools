"""   Use Python 3 to run script.
REFERENCES-> youtube_dl: https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py
          -> BeautifulSoup4: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
          -> requests: https://realpython.com/python-requests/ & https://www.geeksforgeeks.org/get-post-requests-using-python/
          -> ffprobe3: https://github.com/DheerendraRathor/ffprobe3   """


from __future__ import unicode_literals
from configparser import ConfigParser
import bs4
import requests
import os
import sys
import time
import youtube_dl

parser = ConfigParser()
parser.read('input.ini')

home_url = "https://www.youtube.com"

os.makedirs("Music", exist_ok=True)
url = "https://www.youtube.com/results?search_query=" + parser.get('default', 'search_term')

res = requests.get(url)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text)

search_results = soup.select("h3 a")
video_title = search_results[0].get("title")
video_url = home_url + search_results[0].get("href")

print("This is video URL: " + search_results[0].get("href"))
print("Downloading audio from %s" % video_url)

os.chdir("Music")
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

print("Download Complete.")
