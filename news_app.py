import requests
import webbrowser as web
import io
from tkinter import *
from tkinter import ttk
import key
from urllib.request import * 
from PIL import ImageTk, Image


api_key=key.API_KEY

class App :
    global api_key
    base_url='https://newsapi.org/v2/top-headlines?country=in&apiKey='+api_key

    def __init__(self):
        self.launch_app()
        self.collection=requests.get(self.base_url).json()
        # print(collection['articles'][1]['author'])
        self.load_img(0)
        
    def launch_app(self):
        self.root=Tk()
        self.root.geometry('500x600')
        self.root.resizable(0,0)
        self.root.configure(background='#C4DFDF')
        self.root.title('News App')

        ico = Image.open('Images/favicon.png')
        photo = ImageTk.PhotoImage(ico)
        self.root.wm_iconphoto(False, photo)

    #Open external link in browser for more information   
    def read_more(self, url):
        web.open(url)

    #Clearing all widgets each time new headline requested
    def clear_screen(self):
        for slaves in self.root.pack_slaves():
            slaves.destroy()
    
    #For loading image
    def load_img(self, idx):
        self.clear_screen() 

        try:
            img_link=self.collection['articles'][idx]['urlToImage']
            parsed_data=urlopen(img_link).read()
            data_in_buffer=io.BytesIO(parsed_data)
            resized_img=Image.open(data_in_buffer).resize((400,250))
            img=ImageTk.PhotoImage(resized_img)
        except:
            img_loc="Images/img_unavailable.png"
            resized_img=Image.open(img_loc).resize((400,250))
            img=ImageTk.PhotoImage(resized_img)

        self.frame=Frame(self.root, width=500, height=250,bg='#E3F4F4')
        self.frame.pack()
        img_label=Label(self.frame, image=img)
        img_label.pack(padx=50)


        self.load_content(idx)

    #News Content
    def load_content(self, idx):
        #Headline
        self.headline_frame=Frame(self.root,bg='#D2E9E9')
        self.headline_frame.pack(fill='x')
        headline_font=('Times New Roman', 17, 'bold')
        headline_text=self.collection['articles'][idx]['title']
        self.headline=Label(self.headline_frame, text=headline_text,justify='center', wraplength=500, bg='#D2E9E9', fg='black')
        self.headline.pack(pady=2)
        self.headline.configure(font=headline_font)

        #Content
        news_font=('Helvetica', 13)
        news_text= self.collection['articles'][idx]['description']
        self.news_label=Label(self.root, text=news_text, justify='center', wraplength=450, bg='#C4DFDF', fg='grey')
        self.news_label.pack(pady=2)
        self.news_label.config(font=news_font)

        #Next and Previous Headlines
        prev_button_loc="Images/prev_button.png"
        next_button_loc="Images/next_button.png"
        open_prev=Image.open(prev_button_loc)
        prev_img=ImageTk.PhotoImage(open_prev)
        self.prev_button=Button(self.root, image=prev_img, borderwidth=0, bg='#C4DFDF', command=lambda :self.load_img((idx-1)%20)) #%20 for loop
        self.prev_button.place(x=50, y=470)

        open_next=Image.open(next_button_loc)
        next_img=ImageTk.PhotoImage(open_next)
        self.next_button=Button(self.root, image=next_img, borderwidth=0, bg='#C4DFDF', command=lambda :self.load_img((idx+1)%20))
        self.next_button.place(x=380, y=470)

        #Read More Button
        #image from Image by <a href="https://www.freepik.com/free-vector/gradient-call-action-buttons-pack_13763489.htm#query=learn%20more%20button&position=6&from_view=keyword&track=ais">Freepik</a>
        read_more_url=self.collection['articles'][idx]['url']
        open_read=Image.open("Images/read_more.png").resize((200,70))
        read_img=ImageTk.PhotoImage(open_read)
        self.read_button=Button(self.root, image=read_img, borderwidth=0, bg='#C4DFDF', command=lambda :self.read_more(read_more_url))
        self.read_button.place(x=150, y=470)


        self.root.mainloop() #Prevents GUI from closing instantly by blocking execution


new_instance=App()
        