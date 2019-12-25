import tkinter as tk
from tkinter import *
import random
from functools import partial
from tkinter import messagebox

root=tk.Tk()
root.geometry("2000x1000")
root.title('CAPTCHA')
root.configure(background='white')

word=''
def captcha():

    def login_page():
        root.destroy()
        new=tk.Tk()
        new.geometry('2000x1000')
        new.configure(background='red')
        new.title('NEW WINDOW')
        l=Label(new,text='WELCOME TO LOGIN PAGE!!',font=("verdana", 45, "bold italic"))
        l.place(relx=0.2,rely=0.5)
        new.mainloop()

    def generator():
        global word
        word=''
        for i in range(6):
            if random.random()>0.4:
                if random.random()>0.4:
                    val=random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYz')
                else:
                    val=random.choice('abcdefghifghijklmnopqrstuvwxyz')
            else:
                val=random.choice('1234567890')
            word+=val+'  '

        return word

    def validator(entry):
        if reg_entry.get()!='':
            status=True
            inp=[]
            s=entry.get()
            if s=='':
                status=False
            r=reg_entry.get()
            for i in s:
                inp.append(i)
            w=word.split('  ')

            for i,j in zip(w,inp):
                if i==j:
                    continue
                else:
                    status=False
                    break
            if status==False:
                messagebox.showinfo('ALERT!','INVALID CAPTCHA')
                mainer()
            else:
                messagebox.showinfo('ALERT!','CAPTCHA ACCEPTED')
                root.destroy()
                new=tk.Tk()
                new.geometry('2000x1000')
                new.configure(background='red')
                new.title('NEW WINDOW')
                l=Label(new,text='WELCOME TO NEW WINDOW!!',font=("verdana", 45, "bold italic"))
                l.place(relx=0.2,rely=0.5)
                new.mainloop()
        else:
            messagebox.showinfo('ALERT!','ENTER REGISTRATION NUMBER')

    def mainer():
        global word

        ##Label captcha
        cap_code=StringVar()
        text=generator()
        cap_code.set(text)
        img=PhotoImage(file='cap2.png')

        one=Label(textvariable=cap_code,anchor='e',
                  image=img,bd=2,compound=CENTER,
                  relief=RIDGE,bg="white",width=700,height=100,fg="black",border=4,
                  font=("Times", 60, "italic"))
        one.image=img
        one.textvariable=cap_code
        one.place(relx=0.25,rely=0.3)
        Label(text='Type the code you see above *',width=100,bg='white',fg='red',anchor='w').place(relx=0.25,rely=0.47)

        ##entry box
        entry=Entry(font=("Times", 20))
        entry.place(relx=0.25,rely=0.51)

        ##button refresh
        ref=PhotoImage(file='ref.png')
        refresh=Button(root,image=ref,command=mainer)
        refresh.image=ref
        refresh.place(relx=0.25,rely=0.58)

        ##button submit
        submit=Button(root,text="submit",bg='blue',fg='white',width=20,height=2,command=partial(validator,entry))
        submit.place(relx=0.30,rely=0.58)

        ##back to login page
        log=Button(text='Back to login page',
                   relief=FLAT,fg='blue',bg='white',
                   activebackground='white',activeforeground='blue',command=login_page)
        log.place(relx=0.46,rely=0.60)

    reg_num=Label(text="Registration number",bg='white',fg='black',font=("Times", 12, "bold"),anchor='w')
    reg_num.place(relx=0.125,rely=0.17,bordermode=OUTSIDE)
    reg_entry=Entry(font=("Times", 15))
    reg_entry.place(relx=0.25,rely=0.17)
    Label(text='*',bg='white',fg='red').place(relx=0.41,rely=0.163)

    head=Label(text="CAPTCHA WINDOW",bg='blue',fg='white',font=("Times", 12, "bold"),anchor='w')
    head.pack(fill=X,side=TOP)
    mainer()

captcha()
root.mainloop()
