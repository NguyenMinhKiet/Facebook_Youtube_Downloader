import requests
import json
import progressbar
import urllib.request
import webbrowser

pbar = None


def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None

# Thêm access_token từ facebook

def getDataFB(ACCESS_TOKEN):
    getData = requests.get('https://graph.facebook.com/me?fields=accounts{access_token,id,name}&access_token='+ACCESS_TOKEN)
    if(getData.status_code != 200):
        print("ACCOUNT: TOKEN HẾT HẠN")
    else:
        print("Getting data...")
        print('---------------------\n')
        data_bytes = getData.content
        data_str = data_bytes.decode('utf-8')
        data = json.loads(data_str)
        listPages = []
        for page in data["accounts"]["data"]:
            page_ACCESS_TOKEN = page['access_token']
            page_ID = page['id']
            page_NAME = page['name']
            
            data = {
                'access_token' : page_ACCESS_TOKEN,
                'id' : page_ID,
                'name' : page_NAME
            }
            listPages.append(data)

        # Tạo list chưa data video từng page
        Pages = []


        for page in listPages:
            print(page['name']+ ":")
            print('\ngetting page data....\n')
            pageData = requests.get("https://graph.facebook.com/"+page['id']+"?fields=videos{source,id,description}&access_token="+page['access_token'])
            if(pageData.status_code != 200):
                print(page['name'] + " - Token hết hạn")
            else:
                page_data_bytes = pageData.content
                page_data_str = page_data_bytes.decode('utf-8')
                data = json.loads(page_data_str)
                
                listVideos = []
                count = 0

                for video in data["videos"]["data"]:
                    if 'source':
                        count+=1
                        print('video ' + str(count) + ": ")
                        x ={
                            'source':video['source'],
                            'id':video['id']
                        }

                        listVideos.append(x)
                    
                print("\nTotal Videos: " + str(count)+"\n")

                page_data = {
                    'id':page['id'],
                    'videos': listVideos
                }
                Pages.append(page_data)
        
        print('\n---------------------')
        print("Get data success")

        print('\nTotal Page: ' + str(len(Pages)))
        return Pages
    

    # print(Pages)    

# # Dữ liệu mẫu
# ListViews = [
#     {
#         'id': '123456789',  # ID của trang
#         'videos': [
#             {'source': 'video_source_url_1', 'id': 'video_id_1'},
#             {'source': 'video_source_url_2', 'id': 'video_id_2'},
#         ]
#     },
#     {
#         'id': '987654321',  # ID của trang khác
#         'videos': [
#             {'source': 'video_source_url_3', 'id': 'video_id_3'},
#             {'source': 'video_source_url_4', 'id': 'video_id_4'},
#             {'source': 'video_source_url_5', 'id': 'video_id_5'},
#             {'source': 'video_source_url_6', 'id': 'video_id_6'},
#         ]
#     },
# ]
def download(src, path):
    if(src == ''):
        print("Source video không tồn tại")
    else:
        print('\nStart Download....\n')
        urllib.request.urlretrieve(src, 'video_name.mp4',path) 
        print('\nDownload success')

def preview(src):
    if(src == ''):
        print("Source video không tồn tại")
    else:
        print('\nStart Preview....\n')
        webbrowser.open(src)

def getAllVideos(ACCESS_TOKEN):
    data = getDataFB(ACCESS_TOKEN)
    all_videos = []
    for listview in data:
        for video in listview['videos']:
            all_videos.append(video)
    return all_videos

