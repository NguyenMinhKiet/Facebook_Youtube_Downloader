import tkinter as tk
from tkinter import ttk
import getVideoFacebook
import getVideoYoutube
from tkinter import messagebox
from tkinter import filedialog

# Thiết lập số lượng dòng trên mỗi trang
ROWS_PER_PAGE = 10

# Biến toàn cục lưu trữ trang hiện tại
current_page = 0
FB_Video = []
YT_Video = []


# Hàm để cập nhật dữ liệu lên bảng với phân trang
def update_table_FB(page_num):
    # Xóa dữ liệu cũ trước khi cập nhật
    for widget in table_frame_fb.winfo_children():
        widget.destroy()
    # Tiêu đề cột
    ttk.Label(table_frame_fb, text="STT",width=30).grid(row=0, column=0)
    ttk.Label(table_frame_fb, text="ID_VIDEO",width=30).grid(row=0, column=1)
    ttk.Label(table_frame_fb, text="SOURCE",width=50).grid(row=0, column=2)
    ttk.Label(table_frame_fb, text="Tải Xuống",width=30).grid(row=0, column=3)  # Cột trống
    ttk.Label(table_frame_fb, text="Xem trước",width=30).grid(row=0, column=4)  # Cột trống
    # Tính toán chỉ mục bắt đầu và kết thúc của trang
    start_index = page_num * ROWS_PER_PAGE
    end_index = min((page_num + 1) * ROWS_PER_PAGE, len(FB_Video))
    # Hiển thị dữ liệu của trang hiện tại
    for i in range(start_index, end_index):
        video = FB_Video[i]
        id_video = video['id']
        source = video['source']

        # Hiển thị dữ liệu trên bảng
        ttk.Label(table_frame_fb, text=i - start_index + 1, width= 30).grid(row=i % ROWS_PER_PAGE + 1, column=0)
        ttk.Label(table_frame_fb, text=id_video, width= 30).grid(row=i % ROWS_PER_PAGE + 1, column=1)
        ttk.Label(table_frame_fb, text=source, width= 50).grid(row=i % ROWS_PER_PAGE + 1, column=2)
        

        # Tạo nút Tải xuống và Xem trước
        download_button = ttk.Button(table_frame_fb, text="Tải xuống",width=30, command=lambda src=source: download_video_FB(src))
        preview_button = ttk.Button(table_frame_fb, text="Xem trước",width=30, command=lambda src=source: preview_video_FB(src))
        download_button.grid(row=i % ROWS_PER_PAGE + 1, column=3)
        preview_button.grid(row=i % ROWS_PER_PAGE + 1, column=4)


def update_table_YT(page_num):
    # Xóa dữ liệu cũ trước khi cập nhật
    for widget in table_frame_yt.winfo_children():
        widget.destroy()
    # Tiêu đề cột
    ttk.Label(table_frame_yt, text="STT",width=30).grid(row=0, column=0)
    ttk.Label(table_frame_yt, text="TÊN",width=30).grid(row=0, column=1)
    ttk.Label(table_frame_yt, text="SOURCE",width=50).grid(row=0, column=2)
    ttk.Label(table_frame_yt, text="Tải Xuống",width=30).grid(row=0, column=3)  # Cột trống
    ttk.Label(table_frame_yt, text="Xem trước",width=30).grid(row=0, column=4)  # Cột trống
    # Tính toán chỉ mục bắt đầu và kết thúc của trang
    start_index = page_num * ROWS_PER_PAGE
    end_index = min((page_num + 1) * ROWS_PER_PAGE, len(YT_Video))
    # Hiển thị dữ liệu của trang hiện tại
    for i in range(start_index, end_index):
        video = YT_Video[i]
        id_video = video['title']
        source = video['video_id']

        # Hiển thị dữ liệu trên bảng
        ttk.Label(table_frame_yt, text=i - start_index + 1, width= 30).grid(row=i % ROWS_PER_PAGE + 1, column=0)
        ttk.Label(table_frame_yt, text=id_video, width= 30).grid(row=i % ROWS_PER_PAGE + 1, column=1)
        ttk.Label(table_frame_yt, text=source, width= 50).grid(row=i % ROWS_PER_PAGE + 1, column=2)
        

        # Tạo nút Tải xuống và Xem trước
        download_button = ttk.Button(table_frame_yt, text="Tải xuống",width=30, command=lambda src=source: download_video_YT(src))
        preview_button = ttk.Button(table_frame_yt, text="Xem trước",width=30, command=lambda src=source: preview_video_YT(src))
        download_button.grid(row=i % ROWS_PER_PAGE + 1, column=3)
        preview_button.grid(row=i % ROWS_PER_PAGE + 1, column=4)

# Hàm xử lý sự kiện chuyển trang
def next_page(choice):
    global current_page
    current_page += 1
    if(choice == 0):
        update_table_FB(current_page)
    else:
        update_table_YT(current_page)

def prev_page(choice):
    global current_page
    current_page -= 1
    if(choice == 0):
        update_table_FB(current_page)
    else:
        update_table_YT(current_page)

choice = 1

# Tạo cửa sổ
root = tk.Tk()
root.title("Ứng dụng tải video Facebook Youtube")
# Thiết lập kích thước cửa sổ
root.geometry("1368x786")

# Tạo frame chứa tiêu đề "YOUTUBE" và frame chứa bảng
title_frame = ttk.Frame(root)
title_frame.pack(padx=10, pady=10)

table_frame_main = ttk.Frame(root)
table_frame_main.pack(padx=10, pady=10)


# Khung bảng
table_frame_fb = ttk.Frame(table_frame_main)
table_frame_fb.grid(row=1, column=0, padx=10, pady=10)

table_frame_yt = ttk.Frame(table_frame_main)
table_frame_yt.grid(row=1, column=0, padx=10, pady=10)

# Nút chuyển trang
nav_frame = ttk.Frame(table_frame_main)
nav_frame.grid(row=2, column=0, padx=10, pady=5)

prev_button = ttk.Button(nav_frame, text="Trang trước",command=lambda: next_page(choice))
prev_button.grid(row=0, column=0, padx=5)
next_button = ttk.Button(nav_frame, text="Trang sau",command=lambda: prev_page(choice))
next_button.grid(row=0, column=1, padx=5)

# Nút chuyển layout

switch_frame = ttk.Frame(table_frame_main)
switch_frame.grid(row=3, column=0, padx=10, pady=5)

btnFacebook = ttk.Button(switch_frame, text="FACEBOOK",command=lambda: switchToFB())
btnYoutube = ttk.Button(switch_frame, text="YOUTUBE",command=lambda: switchToYT())

btnFacebook.grid(row=0, column=0, padx=5)
btnYoutube.grid(row=0, column=1, padx=5)


def switchToFB():
    global choice
    choice = 0
    init()
    
def switchToYT():
    global choice
    choice = 1
    init()


def download_video_YT(id_video):
    try:
        print("Downloading YOUTUBE video: " + id_video)
        path = filedialog.askdirectory()
        getVideoYoutube.download(id_video, path)
    except:
        print("YOUTUBE DOWNLOAD FAILED")

def preview_video_YT(id_video):
    try:
        print("Previewing YOUTUBE video: " + id_video)
        getVideoYoutube.preview(id_video)
    except:
        print("YOUTUBE DOWNLOAD FAILED")

def download_video_FB(id_video):
    try:
        print("Downloading YOUTUBE video: " + id_video)
        path = filedialog.askdirectory()
        getVideoFacebook.download(id_video , path)
    except:
        print("YOUTUBE DOWNLOAD FAILED")

def preview_video_FB(id_video):
    try:
        print("Previewing YOUTUBE video: " + id_video)
        getVideoFacebook.preview(id_video)
    except:
        print("YOUTUBE DOWNLOAD FAILED")

def searchYT(ID_CHANEL,API_KEY):
    global YT_Video
    if(ID_CHANEL == ''):
        messagebox.showinfo("Lỗi nhập liệu",'Vui lòng nhập ID Chanel!!!')
    else:
        YT_Video = getVideoYoutube.getAllVideos(ID_CHANEL,API_KEY)
        update_table_YT(current_page)

def searchFB(ACCESS_TOKEN):
    global FB_Video
    if(ACCESS_TOKEN == ''):
        messagebox.showinfo("Lỗi nhập liệu",'Vui lòng nhập access token!!!')
    else:
        FB_Video = getVideoFacebook.getAllVideos(ACCESS_TOKEN)
        update_table_FB(current_page)

# FACEBOOK
titleFB = ttk.Label(title_frame, text="FACEBOOK", font=("Arial", 30))
access_token_label = ttk.Label(title_frame, text="NHẬP ACCESS TOKEN FB: ")
inputFB = ttk.Entry(title_frame,width=100)
button = ttk.Button(title_frame,text='lấy dữ liệu',width=50,command=lambda: searchFB(inputFB.get()))


# YOUTUBE
titleYT = ttk.Label(title_frame, text="YOUTUBE", font=("Arial", 30))
label_id_chanel = ttk.Label(title_frame,text="NHẬP ID CHANEL: ")
ID_CHANEL_YT_INPUT = ttk.Entry(title_frame,width=100)
API_KEY = 'AIzaSyBhoX0C8UX8gbiaPeF1ykn7xhnT6u8M8T4'

buttonYT = ttk.Button(title_frame,text='lấy dữ liệu',width=50,command=lambda: searchYT(ID_CHANEL_YT_INPUT.get(),API_KEY))


def hide_frame_elements():
    table_frame_fb.grid_forget()
    titleFB.grid_forget()
    access_token_label.grid_forget()
    inputFB.grid_forget()
    button.grid_forget()

def hide_youtube_frame_elements():
    table_frame_yt.grid_forget()
    titleYT.grid_forget()
    label_id_chanel.grid_forget()
    ID_CHANEL_YT_INPUT.grid_forget()
    buttonYT.grid_forget()

def show_facebook_elements():
    hide_youtube_frame_elements()
    titleFB.grid(row=1, column=0, padx=10, pady=10)
    access_token_label.grid(row=2,column=0, padx=10, pady=10)
    inputFB.grid(row=3,column=0, padx=10, pady=10)
    button.grid(row=4, column=0, padx=10, pady=10)
    table_frame_fb.grid(row=1, column=0, padx=10, pady=10)

def show_youtube_elements():
    hide_frame_elements()
    titleYT.grid(row=1, column=0, padx=10, pady=10)
    label_id_chanel.grid(row=2,column=0, padx=10, pady=10)
    ID_CHANEL_YT_INPUT.grid(row=3,column=0, padx=10, pady=10)
    buttonYT.grid(row=4,column=0, padx=10, pady=10)
    table_frame_yt.grid(row=1, column=0, padx=10, pady=10)

def init():
    if(choice == 0):
        # ACCESS_TOKEN = 'EAAumy3iY7mYBO7MMMNPaYoLEBr5r9kpsAfZCQRVeTdwN2SNzlPPHjq07DYavQl5KEGZBIvJcDjCZCbGRp2u3tcMlNBXagduM1ZB3QNRCMsxzlDCUSSkAMX9nUafvSzzcLlquScMwScW0edJlFNcwMYVVp11ClhTu2MRRE6nPTEFJN5QTNtu1eABZC'
        show_facebook_elements()
    else:
        # ID_CHANEL = 'UCA_23dkEYToAc37hjSsCnXA'
        show_youtube_elements()
init()

# Hiển thị cửa sổ
root.mainloop()