import sys
from googleapiclient.discovery import build
import isodate
from config import api_key

input_link = sys.argv[1]
playlistId = input_link.split('list=')[1]
service = build('youtube', 'v3', developerKey=api_key)
total_secs = 0
NextPageToken = None

while True:
    playlist_request = service.playlistItems().list(
        part = 'contentDetails',
        playlistId = playlistId,
        maxResults = 50,
        pageToken = NextPageToken
    )

    playlist_response = playlist_request.execute()
    videos = []

    for i in playlist_response['items']:
        videos.append(i['contentDetails']['videoId'])

    durations = []

    video_request = service.videos().list(
        part = 'contentDetails',
        id = ",".join(videos)
        )
        
    video_response = video_request.execute()
    for item in video_response['items']:
        durations.append((item['contentDetails']['duration']))
    for iso_timestamp in durations:
        total_secs += int(isodate.parse_duration(iso_timestamp).total_seconds())
    
    NextPageToken = playlist_response.get('nextPageToken')
    if not NextPageToken:
        break

minutes, seconds = divmod(total_secs, 60)
hours, minutes = divmod(minutes, 60)
print(f'{hours}:{minutes}:{seconds}')
