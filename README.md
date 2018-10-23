# AZ Lyrics Web scraping

The azlyrics.py file is a file you can import into your jupyter notebook to extract artist and lyrics data.

Please do not misuse these files. This is a demonstration of how to do web scraping and use Beautiful Soup. Please do not use it to make calls for artistis with more than 10 songs. (see below to see which artists to use this for)

**Functions**

Look at the azlyrics.py file to get an indepth understanding of how each function works.

Here is a demonstration of the azlyrics library. It has the following functions:

- ```get_songs(artist_name)```: returns the links of all the songs of the artist

- ```get_lyrics_for_artist(artist_name)``` returns the lyrics for each song, along with song title, album and artist information

- ```get_lyrics_details(artist_name)``` returns the lyrics for each song, along with song title, album and artist information and statistics - most occurring word and number of words

- ```process_song_lyrics(lyrics)``` where lyrics is a list returned by ```get_lyrics_for_artist(artist_name)```

**Other functions which do exist are:**


- ```get_song_links(song_list_link)``` where song_list_link is the link of an artist on azlyrics.com

- ```lyric_counter(lyrics)``` where lyrics is a list returned by get_lyrics_for_artist


## Artists to demonstrate with

Use:

- Zane 
- Priyanka Chopra 

Do not use artists like:

- Drake 
- Eminem
- Adele 