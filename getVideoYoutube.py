import requests
import json
from pytube import YouTube
from pytube.cli import on_progress
import webbrowser

API_KEY = 'AIzaSyBhoX0C8UX8gbiaPeF1ykn7xhnT6u8M8T4'

ID_CHANEL = 'UCA_23dkEYToAc37hjSsCnXA'


# // link lấy danh sách playlist từ channel id (thay id của channel vào %s dưới là ok)

# // link lấy danh sách video từ playlist id
# linkPlaylist = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId="+ID_PLAYLIST+"&fields=items(snippet(title,thumbnails(high(url),default),resourceId(videoId))),nextPageToken,pageInfo&key="+ API_KEY

# # // link lấy thông tin chi tiết của 1 video youtbe
# linkVideo = "https://www.googleapis.com/youtube/v3/videos?part=id,snippet,contentDetails,statistics&id="+ID_VIDEO+"&maxResults=50&fields=items(id,contentDetails(duration),snippet(title,thumbnails(high(url))),statistics(viewCount,likeCount))&key=" + API_KEY


PLAYLIST_VIDEOS = []
CHANEL_PLAYLIST = []

def preview(video_id):
    if(video_id == ''):
        print("ID video không tồn tại")
    else:
        print('\nStart Preview....\n')
        url = 'https://www.youtube.com/watch?v='+video_id
        webbrowser.open(url)
       
def download(video_id , path):
    if video_id == '':
        print("ID video không tồn tại")
    else:
        print('\nStart Download....\n')
        url = 'https://www.youtube.com/watch?v=' + video_id
        print(url)
        yt = YouTube(url, on_progress_callback=on_progress)
        try: 
            mp4_streams = yt.streams.filter(file_extension='mp4').get_highest_resolution()
            mp4_streams.download(output_path=path)
            print('Video ' + video_id + ' downloaded successfully!')
        except: 
            print("Some Error!")

# output_directory = os.getcwd()+"/videos/"
# if not os.path.exists(output_directory):
#     os.makedirs(output_directory)

def getDataFB(ID_CHANEL,API_KEY):
    linkChannel = "https://www.googleapis.com/youtube/v3/playlists?part=snippet,contentDetails&maxResults=50&channelId="+ID_CHANEL+"&fields=items(contentDetails,id,snippet(title,thumbnails(high(url),default))),nextPageToken,pageInfo&key="+ API_KEY
    DataChanel = requests.get(linkChannel)
    if(DataChanel.status_code != 200):
        print("CHANEL: TOKEN API LỖI")
    else:
        print("Getting data...")
        print('---------------------\n')
        data_bytes = DataChanel.content
        data_str = data_bytes.decode('utf-8')
        data = json.loads(data_str)
        listPlayList = []
        
        PLAYLIST_VIDEOS = []
        CountVideos = 0

        for playlista in data['items']:
            pl = {
                'playlist_id': playlista['id'],
                'chanel_id': ID_CHANEL,
                'num_playlist_video':playlista['contentDetails']['itemCount']
            }
            listPlayList.append(pl)
            
        
        for playlist in listPlayList:
            listVideo = []
            # // link lấy danh sách video từ playlist id
            linkPlaylist = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId="+playlist['playlist_id']+"&fields=items(snippet(title,thumbnails(high(url),default),resourceId(videoId))),nextPageToken,pageInfo&key="+ API_KEY
            DataPlayList = requests.get(linkPlaylist)
            if(DataPlayList.status_code != 200):
                print("PLAYLIST: TOKEN API LỖI")
            else:
                playlist_data_bytes = DataPlayList.content
                playlist_data_str = playlist_data_bytes.decode('utf-8')
                playlist_data = json.loads(playlist_data_str)

                for video in playlist_data['items']:
                    vd = {
                    'title':video['snippet']['title'],
                    'video_id': video['snippet']['resourceId']['videoId'],
                    }
                    CountVideos += 1
                    listVideo.append(vd)
                # for a in listVideo:
                #     print(a['playlist_id'] + ' - '+ a['video_id'])

                PLAYLIST = {
                    'playlist_id': playlist['playlist_id'],
                    'videos':listVideo,
                    'total_video':playlist['num_playlist_video']
                }
                PLAYLIST_VIDEOS.append(PLAYLIST)

        CHANEL = {
            'chanel_id': ID_CHANEL,
            'data': PLAYLIST_VIDEOS,
            'total_playlist':data['pageInfo']['totalResults'],
        }
        CHANEL_PLAYLIST.append(CHANEL)
        print('\n---------------------')
        print("Get data success")
    return CHANEL_PLAYLIST

# CHANEL_PLAYlIST[0]['data'][PHẦN TỬ PLAYLIST ĐẦU TIÊN]['playlist][PHẦN TỬ VIDEO ĐẦU TIÊN]['video_id']
    # print(CHANEL_PLAYLIST[0]['data'][0]['videos'][0]['video_id'])
    # print(CHANEL)
    # test download video
    # download('https://www.youtube.com/watch?v=mzqvF_rIOx8')

def getAllVideos(CHANEL_ID,API_KEY):
    data = getDataFB(CHANEL_ID,API_KEY)
    all_videos = []
    for playlist in data[0]['data']:
        for video in playlist['videos']:
            all_videos.append(video)
    return all_videos