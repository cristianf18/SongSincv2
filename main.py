from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

import lyricsgenius
import re
import json
import requests

accessToken = "dBdNFFsh_ywi-VvikMkPjhpWsdH7kvHX_NLj4vDM07987oCDPwSpDIIIOflEsXX3"
genius = lyricsgenius.Genius(accessToken)




@app.route('/')
def home():
    return render_template('mainWebsite.html')



@app.route('/processUserInput', methods=['POST'])
def getInfo():
    song = request.form.get('userInput')
    genius_search_url = f"http://api.genius.com/search?q={song}&access_token={accessToken}"
    responce = requests.get(genius_search_url)
    json_data= responce.json()    
    artistName = json_data["response"]["hits"][0]["result"]["artist_names"]

    songName = json_data["response"]["hits"][0]["result"]["full_title"]
    parts = songName.find("by")
    songName = songName[:parts]
    imageURL = json_data["response"]["hits"][0]["result"]["header_image_url"]

    print(songName)
    print(artistName)

    return render_template('base.html', artistName=artistName, songName=songName, song=song, imageURL=imageURL)

if __name__ == '__main__':
    app.run(debug=True)
"""

@app.route('/processUserInput', methods=['POST'])
def processUserInput():
    userinput = request.form.get('userInput')
    songName = genius.search_song(userinput)
    artistName = genius.search_artist(userinput)
    print(songName)
    print(artistName)
    
    print(songName)
    if songName:
        artistName = songName.artist
        return render_template('base.html', songName=songName, songLyrics='These are the lyrics for "Nights."', userInput=userinput)
    else:
        errorMessage = f'Song "{userinput}" not found.'
        return render_template('error.html', errorMessage=errorMessage)






"""
