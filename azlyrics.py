
# coding: utf-8

# In[ ]:


# AZLYRICS LIBRARY CAN BE USED TO SCRAPE THE AZLYRICS WEBSITE FOR THE LYRICS OF ANY ARTIST


# In[48]:


import csv
# Import beautiful soup
from bs4 import BeautifulSoup as bs
import requests as r
import re
import csv


# In[34]:


# Returns the artist's page which list's their songs
def get_artist_page(artist_name):
    query = "https://search.azlyrics.com/search.php?q="+artist_name
    # Use the `get` method of the requests library to fetch the page content
    page = r.get(query)
    # Use bs to parse the HTML returned
    soup = bs(page.content, "html.parser")
    # returns the first search result for the artist_name
    return (soup.td.a['href'])


# In[35]:


# Returns the links of all the songs of the artist
def get_song_links(song_list_link):
    query = song_list_link
    # Use the `get` method of the requests library to fetch the page content
    page = r.get(query)
    soup = bs(page.content, "html.parser")
    song_tags = soup.select('a[target="_blank"]')
    return ["https://www.azlyrics.com"+ (s.get('href'))[2:] for s in song_tags]


# In[36]:


# Returns the title from a soup of a song
def get_title(soup):
    return ((soup.h1.text)[1:-8])


# In[4]:


# Returns the album from a soup of a song
def get_album(soup):
    
    dirty_album = soup.findAll("div","panel songlist-panel noprint")

    # If list is empty, this means that is a single of the artist

    if not dirty_album:
        return "Artist Single - No Album Available"

    # If list not empty this means that the single exists
    else:
        return  dirty_album[0].b.text[1:-1]


# In[5]:


# Returns the lyrics from a soup of a song
def get_lyrics(soup):

    #d_lyrics is dirty messy lyrics data
    d_lyrics = soup.findAll("div",attrs={'class': None, 'id': None})
    
    # Cleaning the lyrics
    
    # Substituting out special characters and removing the break new line (\n) 

    cleaner = (((d_lyrics[0].text)[2:]).replace("\n"," ").replace("\r"," "))
    cleanest = re.sub('[(<.!,;?>/\-)]', " ", cleaner)


    return cleanest


# In[39]:


# Returns a list of songs for the artist
def get_songs(artist_name):
    
    artist_link = get_artist_page(artist_name)
    song_links = get_song_links(artist_link)
    
    song_list = []
    
    for link in song_links:
        
        page = r.get(link)
        soup = bs(page.content, "html.parser")
        
        title = get_title(soup)
        song_list.append(title)

    return song_list

#get_songs('Zane')


# In[7]:


# Returns a list of lyrics for a list of songs 
def get_lyrics_by_song_links(song_links):
    
    from bs4 import BeautifulSoup as bs    
    import requests as r
    from time import sleep
    
    # url needed to find artist name
    artist_link = song_links[0]
    
    artist = ((artist_link[32:]).split("/", 1)[0])
    
    lyrics_list = [] 
    
    for link in song_links:
        
        sleep(30) 
        page = r.get(link, proxies=proxies)
        soup = bs(page.content, "html.parser")
        title = get_title(soup)
        album = get_album(soup)
        lyrics = get_lyrics(soup)
        
        song = {"title": title, 
                "album": album,
                "lyrics": lyrics,
                "link": link}  

        lyrics_list.append(song)
        
    return lyrics_list        


# In[40]:


# returns a list of songs with their lyrics for a particular artist
# e.g. get_lyrics_for_artist("zane")
def get_lyrics_for_artist(artist_name):
    
    artist_link = get_artist_page(artist_name)
    song_links = get_song_links(artist_link)
    
    from time import sleep
    
    lyrics_list = [] 
    
    for link in song_links:
        sleep(5) 
       
        page = r.get(link)
        soup = bs(page.content, "html.parser")

        artist = artist_name
        title = get_title(soup)
        #print(title)
        album = get_album(soup)
        lyrics = get_lyrics(soup)

        song = {"title": title, 
                "album": album,
                "lyrics": lyrics,
                "link": link}  

        lyrics_list.append(song)
        
    return lyrics_list


# In[54]:


#zane_lyrics = get_lyrics_for_artist("zane")


# In[41]:


# returns the numbers of words in a list of lyrics
def lyric_counter(lyrics): 
    words = lyrics.split()
    return len(words)


# In[25]:


# returns a list of lyric words which are not stop words
def stop_word_remover(lyrics):
    import re
    import nltk
    nltk.download('punkt')
    from nltk.corpus import stopwords
    nltk.download("stopwords")
    from nltk.tokenize import word_tokenize 

    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(lyrics)
    new_list = [] 
    
    #print(word_tokens)
    
    for w in word_tokens:
        
        if not w.lower().replace("\'", "") in stop_words:
            clean = re.sub('[(<.!,;?>/\-)]', " ", w)
            if len(clean) > 1:
                new_list.append(clean) 
            
    return new_list

#stop_word_remover(hello_lyrics)


# In[42]:


# returns the most occuring word in the lyric
def most_occurring(words):
    return max(set(words), key=words.count)


# In[27]:


#stop_word_remover(hello_lyrics)


# In[46]:


# Returns a dataframe with the most occuring word in the lyrics and the most number of words
def process_song_lyrics(lyrics_list):
    
    import pandas as pd 
    
    for song in lyrics_list:
        
        lyrics_song = (song["lyrics"])
        song["number_of_words"] = lyric_counter(lyrics_song)
        lyrics_without_stop = stop_word_remover(lyrics_song)
        song["most_occurring_word"] = most_occurring(lyrics_without_stop)
    
    lyrics_df = pd.DataFrame(lyrics_list)
        
    return lyrics_df       


# In[52]:


#process_song_lyrics(zane_lyrics)


# In[53]:


# returns a dataframe for the artist provided with lyrics, lyrics count, and most occuring word
def get_lyrics_details(artist_name):
    lyrics_list = get_lyrics_for_artist(artist_name)
    lyrics_df = process_song_lyrics(lyrics_list)
    return lyrics_df

