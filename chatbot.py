from tkinter import *
import tkinter as tk
import random
from PIL import Image,ImageTk
from functools import partial
import speech_recognition as sr

root=tk.Tk()
root.geometry("450x360")
root.title('BOT')

def reply(text_box):
    text=random.choice(['hey there','how are you??','may i help you??','ha ha LOL','I am fine...'])
    print(text_box.get(1.0,END))
    Label(root,text=text,bg='black',fg='white',font=("verdana",18, "bold"),width=21).place(relx=0.0,rely=0.35)
    text_box.delete(1.0,END)

def listen():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        Label(root,text='LISTENING...',bg='black',fg='white',font=("verdana",18, "bold"),width=21).place(relx=0.0,rely=0.35)
        audio=r.listen(source)
        try:
            text=r.recognize_google(audio)
        except:
            Label(root,text='NOT CLEAR, Please Say again..',bg='black',fg='white',font=("verdana",18, "bold"),width=21).place(relx=0.0,rely=0.35)
        Label(root,text='working...',bg='black',fg='white',font=("verdana",18, "bold"),width=21).place(relx=0.0,rely=0.35)
        print(text)
        #return text


#############header construction#########
head_frame=Frame(root,width=700,height=70,bg='green')
img=ImageTk.PhotoImage(Image.open('C:\\Users\\tusha\Downloads\\bot.png'))
icon=Label(head_frame,image=img,bg='green')
icon.place(relx=0.003,rely=0.03)
header=Label(head_frame,text='CHATBOT',width=50,bg='green',fg='white',font=("verdana", 20, "bold"),anchor='w')
header.place(relx=0.07,rely=0)
Online=Label(head_frame,text='Online',bg='green',fg='white',font=("verdana", 8, "bold"),anchor='w')
Online.place(relx=0.07,rely=0.64)
head_frame.place(relx=0,rely=0)
###############header done##############

###############LABEL AT CENTER#########
body_frame=Frame(root,width=450,height=360,bg='black')
body_frame.place(relx=0,rely=0.184)

#############making the input frame###########
footer_frame=Frame(root,width=700,height=100,bg='green')
text_box=Text(footer_frame,fg='black',font=("verdana", 15, "bold"),width=25,height=3)
text_box.place(relx=0.013,rely=0.070)
send=PhotoImage(file='C:\\Users\\tusha\Downloads\\send.png')
send_button=Button(footer_frame,image=send,command=partial(reply,text_box))
send_button.place(relx=0.53,rely=0.126)
mic=PhotoImage(file='C:\\Users\\tusha\Downloads\\mic.png')
mic_button=Button(root,image=mic,command=listen,width=50,height=50)
mic_button.place(relx=0.85,rely=0.55)
footer_frame.place(relx=0,rely=0.72)
#############input frame done################
reply(Text())
root.mainloop()

