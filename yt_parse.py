import requests
import re
from bs4 import BeautifulSoup
import json

query = 'spider-man+no+way+home+trailer'
resp = requests.get('https://www.youtube.com/results?search_query={}'.format(query))
print(resp.status_code)
# with open("youtube.html", "w+", encoding='utf-8') as file:
#     file.write(resp.text)
parsed_resp = BeautifulSoup(resp.text, 'lxml')
script = str(parsed_resp.find_all('script')[33])
data_obj = re.search(r'var ytInitialData = (.+);</script>', script)
obj = json.loads(data_obj.groups()[0])
list_of_videos = obj['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']

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
    return video_info


for item in list_of_videos:
    try:
        print(get_video_info(item))
    except KeyError:
        # skip ad/promoted video
        continue

