from apiclient.discovery import build
import os
import sys

DEVELOPER_KEY = ""
try:
    print(os.environ['API_TOKEN'])
    DEVELOPER_KEY = str(os.environ['API_TOKEN'])
except:
    DEVELOPER_KEY = ""
    print("Invalid token")
    sys.exit()
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def fetch_all_youtube_videos(playlistId):
    """
    Fetches a playlist of videos from youtube
    We splice the results together in no particular order

    Parameters:
        parm1 - (string) playlistId
    Returns:
        playListItem Dict
    """
    youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    res = youtube.playlistItems().list(
    part="snippet",
    playlistId=playlistId,
    maxResults="50"
    ).execute()

    nextPageToken = res.get('nextPageToken')
    while ('nextPageToken' in res):
        nextPage = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlistId,
        maxResults="50",
        pageToken=nextPageToken
        ).execute()
        res['items'] = res['items'] + nextPage['items']

        if 'nextPageToken' not in nextPage:
            res.pop('nextPageToken', None)
        else:
            nextPageToken = nextPage['nextPageToken']

    return res

def getURL(play_list_url):  
    url_disection = play_list_url.split("list=")
    videos = fetch_all_youtube_videos(url_disection[1])
    video_urls = []
    print(len(videos["items"]))
    for music in videos["items"]:
        video_urls.append("https://www.youtube.com/watch?v={}".format(music["snippet"]["resourceId"]["videoId"]))
    
    return video_urls