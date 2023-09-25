from flask import Flask, render_template, request, redirect, url_for
from lyricsgenius import Genius
import re
import json
import requests

# API STUFF
accessToken = "dBdNFFsh_ywi-VvikMkPjhpWsdH7kvHX_NLj4vDM07987oCDPwSpDIIIOflEsXX3"
genius = Genius(accessToken)


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/songs')
def songs():
    return render_template('base.html')

@app.route('/artists')
def artists():
    return render_template('artists.html')




# process user input
@app.route('/processUserInput', methods=['POST'])
def getInfo():
    song = request.form.get('userInput')
    geniusSearchURL = f"http://api.genius.com/search?q={song}&access_token={accessToken}"
    responce = requests.get(geniusSearchURL)
    json_data= responce.json()    

    # finds artist name (good)
    artistName = json_data["response"]["hits"][0]["result"]["artist_names"]


    # find and filter song name (make better later)
    songName = json_data["response"]["hits"][0]["result"]["full_title"]
    parts = songName.find("by")
    songName = songName[:parts]
    imageURL = json_data["response"]["hits"][0]["result"]["header_image_url"]

    # find lyrics   (implementing) (NOT FILTERED YET)
    songLyrics = None
    try:
        song = genius.search_song(song)
        if song:
            songLyrics = song.lyrics
            # print(f"lyrics:\n{songLyrics}")
        else:
            print(f"Song '{songName}' not found.")
    except Exception as e:
        print(f"error: {e}")
        songLyrics = "lyrics not available"

    if songLyrics is None:
        songLyrics = "lyrics not available"

    songLyrics = songLyrics.split('\n')
    print(songLyrics)  

    # verfity information
    print("ABOVE IS LYRICS")
    print(songName)
    print(artistName)

    return render_template('base.html', artistName=artistName, songName=songName, songLyrics=songLyrics, imageURL=imageURL)

if __name__ == '__main__':
    app.run(debug=True)
