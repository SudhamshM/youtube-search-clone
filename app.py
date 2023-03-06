from flask import Flask, request, render_template, redirect
import requests, json, re
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_video_info(self) -> dict:
        base_url = 'https://www.youtube.com'
        video_info = {}
        video_info['title'] = self['videoRenderer']['title']['runs'][0]['text']
        video_info['duration'] = self['videoRenderer']['lengthText']['simpleText']
        video_info['uploaded'] = self['videoRenderer']['publishedTimeText']['simpleText']
    
        video_info['views'] = self['videoRenderer']['viewCountText']['simpleText']
        video_info['uploader'] = self['videoRenderer']['ownerText']['runs'][0]['text']
        video_info['thumbnail'] = self['videoRenderer']['thumbnail']['thumbnails'][0]['url'].split('?')[0]
        video_info['video_url'] = base_url + self['videoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
        video_info['uploader_icon'] = self['videoRenderer']['channelThumbnailSupportedRenderers']['channelThumbnailWithLinkRenderer']['thumbnail']['thumbnails'][0]['url']
        description_list:list[dict] = self['videoRenderer']['detailedMetadataSnippets'][0]['snippetText']['runs']
        description = ''
        for item in description_list:
            description += item.get('text')
        video_info['description'] = description
        return video_info
dictionary_video_list = []
def yt_search_parse(query_to_search:str) -> list:
    dictionary_video_list.clear()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    resp = requests.get('https://www.youtube.com/results?search_query={}'.format(query_to_search), headers=headers)
    print("we have ", resp.status_code)
    parsed_resp = BeautifulSoup(resp.text, 'lxml')
    #script = str(parsed_resp.find_all('script')[32])
    data_obj = re.search(r'>var ytInitialData = (.+);</script>', str(parsed_resp))
    obj = ''
    try:
        obj = json.loads(data_obj.groups()[0])
    except AttributeError:
        with open("yt-resp.html", "w+", encoding='utf-8') as log:
            log.write(resp.text)
            return
    list_of_videos = obj['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
    for item in list_of_videos:
        try:
            dictionary_video_list.append(get_video_info(item))
        except KeyError:
            # skip ad/promoted video
            continue
    return dictionary_video_list

@app.get('/')
def index():
    print(request.endpoint)
    return render_template('index.html')

@app.get('/search')
def search():
    search_term = request.args.get('query')
    if not search_term:
        return redirect('/')
    complete_video_list = yt_search_parse(search_term)
    print(complete_video_list)
    ## table list view
    #return render_template("results.html", query=search_term, video_list=complete_video_list)
    ## card list view
    return render_template('html-videos.html', video_list=complete_video_list)

@app.get('/watchlist')
def get_watchlist():
    return render_template("index.html")