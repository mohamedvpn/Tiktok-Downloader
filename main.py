import flet as ft
import json
import requests
import re,os
from fake_useragent import UserAgent


class Tiktok_List_Video(ft.View):
    def __init__(self,page):
        super().__init__()
        self.page = page
        self.route = "/Tiktok_Window_list"
        self.auto_scroll = True
        self.session = requests.Session()
        self.bgcolor = ft.Colors.TRANSPARENT
        # self.padding = 5
        self.bgcolor = "transparent"
        self.status_text_pr = ft.Text(style="headlineSmall",size=15)
        self.ProgressBar_Don = ft.ProgressBar(
            value=0, 
            height=5,
            color="green", 
            bgcolor="#eeeeee",
            visible=False,
            border_radius=20,
            width=350,
        )
        

        self.num_target = ft.TextField(
                                label="عدد",
                                width=50,
                                value="1",
                                border=ft.InputBorder.NONE,
                                label_style=ft.TextStyle(color="white"),
                                input_filter=ft.NumbersOnlyInputFilter(),
                            )
        self.Text_msg = ft.TextField(
                                label="أدخل يوزر الحساب هنا",
                                rtl=True,
                                # border=ft.InputBorder.NONE,
                                # multiline=True,
                                expand=True,
                                # value="abo.3aid",
                                # on_change=on_change_msg
                                label_style=ft.TextStyle(color="white"),
                                # border_radius=20,
                                border="underline"
                                )
        

        
       
        
        self.type_mp4_or_mp3 = ft.Dropdown(
            # editable=True,
            value="MP4",  # تعيين القيمة الافتراضية لتطابق أحد الخيارات
            options=[
                ft.DropdownOption(
                    key="MP4",
                    content=ft.Text("MP4"),
                ),
                ft.DropdownOption(
                    key="MP3",
                    content=ft.Text("MP3"),
                ),
            ],
            on_change=self.dropdown_changed,
            border=ft.InputBorder.NONE,
            # menu_height=30
        )
        
        
        self.chat = ft.ListView(auto_scroll=True,height=300,padding=20,spacing=5)
        self.root = ft.Container(
            content=ft.Column([
                

                # chat
                self.chat,

                ft.Container(
                    ft.Column([
                        self.status_text_pr,
                        self.ProgressBar_Don,
                        #type
                        ft.Container(
                            #type
                            self.type_mp4_or_mp3,
                        alignment=ft.alignment.top_left
                        ),
                        
                    ]),
                alignment=ft.alignment.center,
                ),
                
                
                # bt msg
                ft.Container(
                    content=ft.Container(
                        ft.Row([

                            self.num_target,

                            self.Text_msg,


                        ],alignment=ft.MainAxisAlignment.CENTER,)
                    ),
                padding=ft.padding.only(left=5),
                
                ),
            ]),
            padding=ft.padding.only(right=15),
            alignment=ft.alignment.center,
            # border=ft.border.all(1,"#000000"),
            border_radius=20,
        )

        # self.controls = [self.root]
        self.page.on_keyboard_event = self.on_keyboard

        self.controls = [
            ft.AppBar(
                    # title=ft.Text("Tiktok 1"),
                    center_title=True,
                    # bgcolor = "transparent",
                    #color="white",
                    actions=[
                        #ft.PopupMenuButton(#icon=ft.Icons.MENU,icon_size=25,
                            ft.Container(
                                ft.IconButton(icon=ft.Icons.CLOSE,icon_color="red",bgcolor="#1b263b",icon_size=18,width=35,height=35,on_click=self.fun_close),
                            margin=ft.Margin(0,0,5,0)
                            )
                            # items=[
                            #     # ft.PopupMenuItem(icon=ft.Icons.DARK_MODE,text="theme", checked=False, on_click=change_theme),
                            #     ft.PopupMenuItem(),  # divider
                            #     ft.PopupMenuItem(icon=ft.Icons.INFO_OUTLINE,text="About",checked=False, on_click=lambda _: self.page.go("/About")),                
                            
                            ],
                            
                        # )
                    # ],
                    leading=ft.IconButton(icon=ft.Icons.ARROW_BACK_IOS_ROUNDED,on_click=lambda _: self.page.go("/")),
                    bgcolor = ft.Colors.TRANSPARENT
                    
            ),

            self.root,
        ]
    
    
    def on_keyboard(self,e: ft.KeyboardEvent):
        #print(e)
            if e.key == "Enter":
                print("Enter")
                self.Send_user()






    def Send_user(self):
        msg_user = self.Text_msg.value
        ret_msg = ft.Column([ft.ProgressRing(width=30, height=30, stroke_width = 6,color="green")])
        
        if self.num_target.value == "" or self.num_target.value == "0": 
            ret_msg.controls.clear()
            self.chat.controls.append(
                ft.Text("قم بتحديد عدد الفيديوهات .",rtl=True)
            )
            self.page.update()
            return
        

        if msg_user != "":
            self.chat.controls.append(
                ft.Text(msg_user,rtl=True)
            )
            self.chat.controls.append(
                ret_msg
            )
            
            

            # self.Text_msg.value = ""
            self.Text_msg.focus()
            self.page.update()
            
            
            ret_msg.controls.clear()
        else:
            ret_msg.controls.clear()
            self.chat.controls.append(
                ft.Text("لم يتم العثور على فيديوهات.",rtl=True)
            )
            self.page.update()
            return

        
        try:
            self.status_text_pr.value = "Waiting to upload..."
            self.status_text_pr.update()







            
            # url = f'https://www.tiktok.com/@{msg_user}'
            
            profile_url = f"https://www.tiktok.com/@{str(msg_user)}"
            headers = {
                # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "User-Agent": f"{UserAgent.random}",
                "Referer": profile_url
            }

            response = self.session.get(profile_url, headers=headers)
            html = response.text
            
            # البحث عن sec_user_id باستخدام تعبير منتظم أكثر دقة
            sec_user_id_match = re.search(r'"secUid":"([^"]+)"', html)
            if not sec_user_id_match:
                # print("Error user_id")
                self.chat.controls.append(
                    ft.Text("لم يتم العثور على فيديوهات.",rtl=True)
                )
                    
                self.page.update()

                # with open("index.html","w",encoding="utf-8") as f:
                #     f.write(str(html))
                return ["فشل في الحصول على sec_user_id"]
            sec_user_id = sec_user_id_match.group(1)
            video_links = []
            downloaded_count = 0
            cursor = "0"
            # collected = 0

            download_folder = os.path.join(os.getcwd(), f"Downloads/{msg_user}/{self.type_mp4_or_mp3.value}")
            os.makedirs(download_folder, exist_ok=True)
            existing_videos = {f.split('.')[0] for f in os.listdir(download_folder)}
            
            while downloaded_count < int(self.num_target.value):
                
                if len(video_links) >= int(self.num_target.value):
                    break
                # حساب العدد المتبقي لطلبه
                # remaining = int(self.num_target.value) - collected
                # count = min(remaining, 30)  # الحد الأقصى لكل طلب هو 30
                
                # 3. طلب API مع الترحيل
                api_url = "https://www.tiktok.com/api/post/item_list/"
                params = {
                    "aid": "1988",
                    "secUid": sec_user_id,
                    "count": "10",
                    "cursor": cursor
                }
                
                response = self.session.get(api_url, headers=headers, params=params)
                data = response.json()
                if not data.get("itemList"):
                    break
                # استخراج الروابط وتحديث المؤشرات
                for video in data["itemList"]:
                    if len(video_links) >= int(self.num_target.value):
                        break
                

                    title = video.get("desc", None)
                    id_video = video.get("id", None)

                    video_mp3 = video.get("music", None)
                    if video_mp3:
                        video_mp3 = video_mp3.get("playUrl", None)
                            
                    ##
                    video_info = video.get("video", None)
                    if video_info:
                        video_mp4 = video_info.get("playAddr", None)
                        cover = video_info.get("cover", None)
                    
                    stats = video.get("stats", None)
                    if stats:
                        # comment_Count = stats.get("commentCount", None)
                        like_Count = stats.get("diggCount", None)
                        # share_Count = stats.get("shareCount", None)
                    

                    # print("*"*50)
                    #download
                    if self.type_mp4_or_mp3.value == "MP4":
                        url = video_mp4
                    else:
                        url = video_mp3


                    if id_video in existing_videos:
                        print("الفيديو موجود",f"{id_video}")
                        ret_msg.controls.append(
                            ft.Text(f"تم التحميل مسبقًا {id_video}",rtl=True,text_align= "center")
                        )
                        self.page.update()
                        continue
                    else:
                        # print(f"id_video: {id_video}")
                        # print(f"title: {title}")
                        # print(f"cover: {cover}")
                        
                    
                        #############
                        cover_img = cover
                        like_count = like_Count
                        video_title = title
                        print("============================================")
                        
                        ret_msg.controls.append(
                            ft.Row([

                                
                                ft.Container(
                                    ft.Image(
                                        src=cover_img,
                                        
                                        border_radius=100,
                                        fit=ft.ImageFit.COVER,
                                        width=100,
                                        height=100,
                                    ),
                                padding=0,
                                ),
                                
                                
                                ft.Container(
                                    ft.Column([

                                    
                                    
                                    ft.Text(
                                        f"العنوان : {video_title}"[:50],
                                        width=150,
                                        size=12,
                                        height=20,
                                        # bgcolor="black",
                                        visible=(True if video_title != "" else False),
                                    ),
                                    
                                    
                                    ft.Text(
                                        f"عدد الإعجابات: {like_count}"[:40],
                                        width=150,
                                        size=12,
                                        height=20,
                                    ),
                                ],spacing=5),
                                
                                padding=0,
                                # alignment=ft.alignment.top_left,
                                rtl=True,
                                width=190,
                                ),
                            
                                
                            ],spacing=5,),
                            
                        
                        )
                        self.page.update()
                        self.download(
                            url = url,
                            download_folder = download_folder,
                            id_video = id_video,
                        )
                        video_links.append({video['id']})
                        
                        downloaded_count += 1
                        print(f"Downlood id {id_video} | {downloaded_count}/{int(self.num_target.value)}")
                        self.ProgressBar_Don.visible = True
                        # ProgressBar_Don.value += 20//int(num_target.value)*0.01
                        self.ProgressBar_Don.value = downloaded_count / int(self.num_target.value)
                        self.status_text_pr.value = f"Download video {downloaded_count}/{int(self.num_target.value)}..."
                        self.page.update()


                        

                        self.page.update()
                if downloaded_count >= int(self.num_target.value):
                    self.status_text_pr.value = "All Videos Downloads Successfully ✅"
                    self.page.update()
                    break

                # collected += len(data["itemList"])
                # التحديث للموجة القادمة
                cursor = data.get("cursor", "0")
                if not data.get("hasMore", False):
                    break
                #############################
                
                

                ret_msg.update()
                self.page.update()
        except Exception as e:
            # print(e)
            self.chat.controls.append(
                ft.Text("لم يتم العثور على فيديوهات.",rtl=True)
            )
            
        self.page.update()

    def fun_close(self,e):
        self.page.window.close()

    
    def download(self,url,download_folder,id_video):
        # download_folder = os.path.join(os.getcwd(), f"Downloads/{name_folder}/{path_mp4_or_mp3}")
        # os.makedirs(download_folder, exist_ok=True)
        # existing_videos = {f.split('.')[0] for f in os.listdir(download_folder)}

        # تحميل الفيديو
        if self.type_mp4_or_mp3.value == "MP4":
            response = self.session.get(url, stream=True)
            with open(f"{download_folder}/{id_video}.mp4", "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
        else:
            response = self.session.get(url, stream=True)
            with open(f"{download_folder}/{id_video}.mp3", "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)


    def dropdown_changed(self,e):
        self.type_mp4_or_mp3.value = e.control.value  # تحديث القيمة المحددة
        print(self.type_mp4_or_mp3.value)
        self.page.update()


class Tiktok_One_Video(ft.View):
    def __init__(self,page):
        super().__init__()
        self.page = page
        self.route = "/Tiktok_One_Video"
        self.auto_scroll = True
        self.session = requests.Session()
        self.bgcolor = ft.Colors.TRANSPARENT
        # self.padding = 5
        self.bgcolor = "transparent"
        self.status_text_pr = ft.Text(style="headlineSmall",size=15)
        self.ProgressBar_Don = ft.ProgressBar(
            value=0, 
            height=5,
            color="green", 
            bgcolor="#eeeeee",
            visible=False,
            border_radius=20,
            width=350,
        )
        

        self.Text_msg = ft.TextField(
            label="أدخل رابط الفيديو هنا",
            rtl=True,
            # border=ft.InputBorder.NONE,
            # multiline=True,
            expand=True,
            # value="https://www.tiktok.com/@sameh_hussien/video/7477592073449803029",
            # on_change=on_change_msg
            label_style=ft.TextStyle(color="white"),
            border="underline"
        )
        

        
       
        
        self.type_mp4_or_mp3 = ft.Dropdown(
            # editable=True,
            value="MP4",  # تعيين القيمة الافتراضية لتطابق أحد الخيارات
            options=[
                ft.DropdownOption(
                    key="MP4",
                    content=ft.Text("MP4"),
                ),
                ft.DropdownOption(
                    key="MP3",
                    content=ft.Text("MP3"),
                ),
            ],
            on_change=self.dropdown_changed,
            border=ft.InputBorder.NONE,
            # menu_height=30
        )
        
        
        self.chat = ft.ListView(auto_scroll=True,height=300,padding=20,spacing=5)
        self.root = ft.Container(
            content=ft.Column([
                

                # chat
                self.chat,

                ft.Container(
                    ft.Column([
                        self.status_text_pr,
                        self.ProgressBar_Don,
                        #type
                        ft.Container(
                            #type
                            self.type_mp4_or_mp3,
                        alignment=ft.alignment.top_left
                        ),
                        
                    ]),
                alignment=ft.alignment.center,
                ),
                
                
                # bt msg
                ft.Container(
                    content=ft.Container(
                        ft.Row([

                            self.Text_msg,


                        ],alignment=ft.MainAxisAlignment.CENTER,)
                    ),
                padding=ft.padding.only(left=5),
                
                ),
            ]),
            padding=ft.padding.only(right=15),
            alignment=ft.alignment.center,
            # border=ft.border.all(1,"#000000"),
            border_radius=20,
        )

        # self.controls = [self.root]
        self.page.on_keyboard_event = self.on_keyboard

        self.controls = [
            ft.AppBar(
                    # title=ft.Text("Tiktok 1"),
                    center_title=True,
                    # bgcolor = "transparent",
                    #color="white",
                    actions=[
                        #ft.PopupMenuButton(#icon=ft.Icons.MENU,icon_size=25,
                            ft.Container(
                                ft.IconButton(icon=ft.Icons.CLOSE,icon_color="red",bgcolor="#1b263b",icon_size=18,width=35,height=35,on_click=self.fun_close),
                            margin=ft.Margin(0,0,5,0)
                            )
                            # items=[
                            #     # ft.PopupMenuItem(icon=ft.Icons.DARK_MODE,text="theme", checked=False, on_click=change_theme),
                            #     ft.PopupMenuItem(),  # divider
                            #     ft.PopupMenuItem(icon=ft.Icons.INFO_OUTLINE,text="About",checked=False, on_click=lambda _: self.page.go("/About")),                
                            
                            ],
                            
                        # )
                    # ],
                    leading=ft.IconButton(icon=ft.Icons.ARROW_BACK_IOS_ROUNDED,on_click=lambda _: self.page.go("/")),
                    bgcolor = ft.Colors.TRANSPARENT
                    
            ),

            self.root,
        ]
    
    
    def on_keyboard(self,e: ft.KeyboardEvent):
        #print(e)
            if e.key == "Enter":
                # print("Enter")
                self.Send_user()

    def Send_user(self):
        video_url = self.Text_msg.value
        ret_msg = ft.Column([ft.ProgressRing(width=30, height=30, stroke_width = 6,color="green")])
        
        
        

        if video_url != "":
            self.chat.controls.append(
                ft.Text(video_url,rtl=True)
            )
            self.chat.controls.append(
                ret_msg
            )
            
            

            self.Text_msg.value = ""
            self.Text_msg.focus()
            self.page.update()
            
            
            ret_msg.controls.clear()
        else:
            ret_msg.controls.clear()
            self.chat.controls.append(
                ft.Text("لم يتم العثور على فيديوهات.",rtl=True)
            )
            self.page.update()
            return

        
        try:

            self.status_text_pr.value = "Waiting to upload..."
            self.status_text_pr.update()

            # download_folder = os.path.join(os.getcwd(), f"Downloads/{video_url}/{self.type_mp4_or_mp3.value}")
            # os.makedirs(download_folder, exist_ok=True)
            # existing_videos = {f.split('.')[0] for f in os.listdir(download_folder)}
            
            headers = {
                "User-Agent": f"{UserAgent.random}",
                "Referer": "https://www.tiktok.com/",
            }

            response = self.session.get(video_url, headers=headers)
            html = response.text

            # البحث عن البيانات المخفية في الصفحة
            script_data = re.search(
                r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>',
                html
            )
            if not script_data:
                return {"error": "فشل في العثور على بيانات الفيديو"}
            
            data = json.loads(script_data.group(1))
            video_info = data.get("__DEFAULT_SCOPE__", {}).get("webapp.video-detail", {}).get("itemInfo", {}).get("itemStruct", {})

            # استخراج روابط الفيديو والصوت من الهيكل
            video_data = video_info.get("video", {})
            # video_mp4 = video_info.get("playAddr", None)

            # download_link = video_data.get("downloadAddr", "")  # رابط التحميل الرسمي (مع علامة مائية)
            play_link = video_data.get("playAddr", "")          # رابط التشغيل (قد يكون بدون علامة مائية)

            # إزالة العلامة المائية من الرابط (خدعة تعمل أحيانًا)
            no_watermark_video = play_link.replace("playwm", "play") if play_link else ""
            

            video_title = video_info.get("desc", "")
            author = video_info.get("author", {}).get("uniqueId", "")
            id = video_info.get('id', '')
            like_count = video_info.get("stats", {}).get("diggCount", 0)
            download_video = no_watermark_video # قد لا يعمل دائمًا!
            download_audio = video_info.get("music", {}).get("playUrl", "")
            cover = video_data.get("cover", None)

            print(f"video_title: {video_title}")
            print(f"author: {author}")
            print(f"id: {id}")
            print(f"like_count: {like_count}")
            print(f"cover: {cover}")


            


            
            ret_msg.controls.append(
                ft.Row([

                    
                    ft.Container(
                        ft.Image(
                            src=cover,
                            
                            border_radius=100,
                            fit=ft.ImageFit.COVER,
                            width=100,
                            height=100,
                        ),
                    padding=0,
                    ),
                    
                    
                    ft.Container(
                        ft.Column([

                        
                        
                        ft.Text(
                            f"العنوان : {video_title}"[:40],
                            width=150,
                            size=12,
                            height=20,
                            # bgcolor="black",
                            visible=(True if video_title != "" else False),
                        ),
                        
                        # ft.Text(
                        #     f"عدد المشاهدات: {view_count}"[:40],
                        #     width=150,
                        #     size=12,
                        #     height=20,
                        #     # bgcolor="black",
                        # ),
                        ft.Text(
                            f"عدد الإعجابات: {like_count}"[:40],
                            width=150,
                            size=12,
                            height=20,
                        ),
                    ],spacing=0),
                    
                    padding=0,
                    # alignment=ft.alignment.top_left,
                    rtl=True,
                    width=190,
                    ),
                
                    
                ],spacing=5,),
                
            
            )

            ret_msg.update()

            if self.type_mp4_or_mp3.value == "MP4":
                url = download_video
            else:
                url = download_audio
            download_folder = os.path.join(os.getcwd(), f"Downloads/{author}/{self.type_mp4_or_mp3.value}")
            os.makedirs(download_folder, exist_ok=True)
            existing_videos = {f.split('.')[0] for f in os.listdir(download_folder)}

            if not id in existing_videos:
                # pass
                # print(f"download_audio: {download_audio}")
                # print(f"download_audio: {download_audio}")

                self.download(url,download_folder,id)
                self.status_text_pr.value = "All Videos Downloads Successfully ✅"
            else:
                print(f"found {id}")


            
            self.page.update()
            
        

    
        except Exception as e:
            # print(e)
            self.chat.controls.append(
                ft.Text("لم يتم العثور على فيديوهات.",rtl=True)
            )
            self.status_text_pr.value = ""
            self.page.update()


































    def fun_close(self,e):
        self.page.window.close()

    
    def download(self,url,download_folder,id_video):
        # download_folder = os.path.join(os.getcwd(), f"Downloads/{name_folder}/{path_mp4_or_mp3}")
        # os.makedirs(download_folder, exist_ok=True)
        # existing_videos = {f.split('.')[0] for f in os.listdir(download_folder)}

        # تحميل الفيديو
        if self.type_mp4_or_mp3.value == "MP4":
            response = self.session.get(url, stream=True)
            with open(f"{download_folder}/{id_video}.mp4", "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
        else:
            response = self.session.get(url, stream=True)
            with open(f"{download_folder}/{id_video}.mp3", "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)


    def dropdown_changed(self,e):
        self.type_mp4_or_mp3.value = e.control.value  # تحديث القيمة المحددة
        print(self.type_mp4_or_mp3.value)
        self.page.update()






##################
###################################
def main(page: ft.Page):
    page.title = "Tiktok Downloader (by:PowerFamily)"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.height = 570
    page.window.width = 390
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.DARK
    # page.padding = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.title_bar_hidden = True
    page.window.frameless = True
    page.window.focused = True
    page.window.resizable = False
    page.window.bgcolor = "#14213d"
    
    # page.window.minimized
    # page.bgcolor = "#0d160b"
    # page.window.always_on_top = True
    page.window.center()
    page.fonts = {
        # "Cairo-Black" : "assets/fonts/Cairo-Black.ttf",
        "Cairo-Black" : "assets/fonts/NotoKufiArabic-SemiBold.ttf",
        # "Cairo-Black" : "assets/fonts/Cairo-Black.ttf",
        # "Cairo-Black" : "assets/fonts/Cairo-Black.ttf",
        # "Cairo-Black" : "assets/fonts/Cairo-Black.ttf",
    }
    page.theme = ft.Theme(font_family="Cairo-Black")  # Default app font
    #
    
    ##############################
    def change_theme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
        else:
            page.theme_mode = ft.ThemeMode.DARK
        
        page.update()

    def minimize_window(_):
        page.window.minimized = True
        page.update()

    # def Dialog_info():


    def on_hv(e):
        #bgcolor="#1b263b",
        # page.window.minimized = True
        if e.data == "true":
            e.control.bgcolor = "#3a86ff"
        else:
            e.control.bgcolor = "#1b263b"


        page.update()

    def route_change(route):
        page.views.clear()
        # page.views.append(
        #     Main_Window(page)
        # )

        if page.route == "/":
            # page.window.height = 500
            page.views.append(
                home_view
            )
        elif page.route == "/Tiktok_Window_list":
            page.views.append(
                Tiktok_List_Video(page)
            )
        elif page.route == "/Tiktok_Window_One":
            page.views.append(
                Tiktok_One_Video(page)
            )
        # elif page.route == "/store":
        #     page.views.append(
        #         Store_Window(page)
        #     )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    # page.go(page.route)

    
    home_view = ft.View(
        route = "/",
        auto_scroll = True,
        padding = 5,
        bgcolor = "transparent",
        
        controls = [
            ft.AppBar(
                    # title=ft.Text("Main"),
                    center_title=True,
                    bgcolor = "transparent",
                    #color="white",
                    actions=[
                        ft.IconButton(icon=ft.Icons.MINIMIZE,on_click=minimize_window),
                        ft.IconButton(icon=ft.Icons.CLOSE,on_click=lambda _: page.window.close())
                            
                    ],
                    # leading=ft.IconButton(icon=ft.Icons.PERSON, on_click=lambda _: Dialog_info())
                    
            ),


            ft.Container(
                ft.Column(
                    [
                        # Logo_img_1,
                        ft.Container(
                            content=ft.Column([
                                ft.Text(value="تحميل من تيك توك",size=25,text_align="center",weight=ft.FontWeight.W_100,color="#e0e1dd"),
                                ft.Divider(height=1),
                                ft.Text("",height=5,rtl=True),
                                ft.Container(
                                    ft.Column([
                                        ft.Text("المميزات : ",rtl=True),
                                        
                                        ft.Text("✅ تحميل كل الفيديوهات من الحساب",rtl=True),
                                        ft.Text("✅ تحميل بصيغة MP4 (فيديو) أو MP3 (صوت)",rtl=True),
                                        ft.Text("✅ أسرع أداء ممكن تشوفه ف حياتك",rtl=True),
                                        ft.Text("✅ مجانًا مدى الحياة ❤️",rtl=True),
                                        ft.Text("",height=5,rtl=True),

                                        
                                    ],rtl=True),
                                rtl=True
                                )
                                


                            ],alignment=ft.MainAxisAlignment.START,rtl=True),
                            padding=20,
                            # bgcolor="black",
                            border_radius=10,
                            #margin=ft.margin.only(bottom=3),
                            # width=290,
                            # height=220,

                            # on_hover=on_hover,
                        ),


                        #box 1 
                        ft.Container(
                            content=ft.Text(value="تحميل متعدد الفيديوهات",size=20,text_align="center"),
                            padding=20,
                            bgcolor="#1b263b",
                            border_radius=10,
                            on_click=lambda _: page.go("/Tiktok_Window_list"),
                            #margin=ft.margin.only(bottom=3),
                            width=290,
                            on_hover=on_hv,
                        ),

                        ft.Container(
                            content=ft.Text(value="تحميل فيديو فردي",size=20,text_align="center"),
                            padding=20,
                            bgcolor="#1b263b",
                            border_radius=10,
                            on_click=lambda _: page.go("/Tiktok_Window_One"),
                            #margin=ft.margin.only(bottom=3),
                            width=290,
                            on_hover=on_hv,
                        ),
                        
                        
                        ft.Text(height=20),
                        ft.Container(ft.Text(value="تابعنا",size=15,text_align="center",weight="w100"),
                                on_click=lambda _: page.launch_url("https://www.facebook.com/groups/powerfamily"),
                            # bgcolor="black",
                            # width=270,
                            border_radius=10,
                            padding=5,
                        ),

                        
                        ################
                        
                        # txt_number,
                        # ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),
                        # ft.IconButton(ft.Icons.ADD, on_click=plus_click),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,


                ),
            alignment=ft.alignment.center,
            expand=True,
            padding=0,
            # image_src="assets/Logo_1.jpg",
            # image_src="https://picsum.photos/100/100",
            # image_fit=ft.ImageFit.CONTAIN,
            
                    
            )



        ]
        
    
    )


    # page.go("/Tiktok_Window_list")
    page.go("/",)
    # page.go("/Tiktok_Window_One")
    # page.go("/Tiktok_Window_One")

    page.update()
        

ft.app(main, assets_dir="assets")


















