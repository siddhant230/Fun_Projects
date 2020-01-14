import tkinter as tk
from tkinter import *
import random,pickle
from functools import partial
from tkinter import messagebox
from tkinter.filedialog import askopenfile

encryp_window,decryp_window,root=None,None,None

f=open('prime_list.pkl','rb')
primes=pickle.load(f)

def target_caller():
    global decryp_window,encryp_window,root
    files=askopenfile(title='Select Folder')
    file=files.name
    if file[-3:]=='pkl':
        f=open(file,'rb')
        m=pickle.load(f)
        text,key,lock=m[0],m[1],m[2]
        dec_text=decrypter(key,text)
        dec_text=cleaner(dec_text,lock,key)
        Label(decryp_window,text='DECODED TEXT').place(relx=0.1,rely=0.55)
        Label(decryp_window,text=dec_text).place(relx=0.1,rely=0.6)
    else:
        messagebox.showinfo('ALERT','Wrong file type')

def copyit(text_with_key):
    r=text_with_key
    f=open('encoded_text_file.pkl','wb')
    pickle.dump(r,f)
    tk.Label(encryp_window,text='The Encrypted text and key has been saved\nLOCATION : "C:\\Users\\tusha\Desktop\RSA_APPROACH\\encoded_text_file.pkl"\nnow open decryptor and decode you Text').place(relx=0.01,rely=0.8)

def prime_picker():
    p,q=random.choices(primes[:50],k=2)
    return p,q

def co_prime_check(e_dic,val):
    p=2
    val=val-1
    while p*p<=val:
        if e_dic[p]==True:
            e_dic[p]=False
            for j in range(p*p,val+1,p):
                if j in e_dic:
                    e_dic[j]=False
        p+=1
    return e_dic

def encrypter(lock,s):
    nums=[]
    for n in s:
        nums.append(ord(n)-96)
    enc_text=''
    for n in nums:
        value=(n**lock[0])%lock[1]
        enc_text+=chr(value+96)
    return enc_text

def decrypter(key,text):
    dec_text=''
    for t in text:
        num=ord(t)-96
        value=(num**key[0])%key[1]
        dec_text+=chr(value+96)
    return dec_text

def cleaner(text,lock,key):
    space_lock=encrypter(lock,' ')
    space_key=decrypter(key,space_lock)

    fin_list=text.split(sep=space_key)
    fin_text=' '.join(fin_list)
    while fin_text[-1] not in 'abcdefghijklmnopqrstuvwxyz0123456789':
        fin_text=fin_text[:-1]
    return fin_text

def encryption(enc_text):
    if enc_text.get("1.0",END)[:-1]!='':
        p,q=prime_picker()
        N=p*q
        phi_n= (p-1) * (q-1)

        ###choosing e
        e_dic={}
        for i in range(2,phi_n):
            e_dic[i]=True
        co_dic=co_prime_check(e_dic,N)
        co_dic=co_prime_check(co_dic,phi_n)
        e=0
        for c in co_dic:
            if co_dic[c]:
                e=c

        lock=(e,N)            ##lock found

        ###choosing d
        d=1
        security=7          ###how many factors do you want to leave
        while True:
            if (d*e)%phi_n==1:
                if security!=0:
                    security-=1
                else:
                    break
            d+=1

        key=(d,N)           ##key found
        s=enc_text.get("1.0",END)
        s=s[:-1]
        s=s.lower()
        ###encryption
        encrypted_text=encrypter(lock,s)
        val=[encrypted_text,key,lock]
        ###key showing
        tk.Label(encryp_window,text='KEY : {}'.format(str(key))).place(relx=0.1,rely=0.50)
        tk.Label(encryp_window,text='LOCK : {}'.format(str(lock))).place(relx=0.5,rely=0.50)
        tk.Label(encryp_window,text='ENCRYPTED TEXT').place(relx=0.1,rely=0.60)
        tk.Label(encryp_window,text=encrypted_text).place(relx=0.1,rely=0.64)
        tk.Button(encryp_window,text="SAVE TO FILE",command=partial(copyit,val)).place(relx=0.1,rely=0.72)

    else:
        messagebox.showinfo('ALERT','ENTER SOMETHING')

def GUI_ENCRYPTOR():
    global encryp_window,root

    encryp_window=tk.Tk()
    encryp_window.geometry("450x600")
    encryp_window.title('ENCRYPTOR')
    encryp_window.configure(background='white')
    root.destroy()
    title=tk.Label(encryp_window,text='ENCRYPTOR',font={'verdana','100','italic bold'},bg='red',fg='white',bd=8,width=70)
    title.pack(fill=Y,side=TOP)
    encrypt_exit=tk.Button(encryp_window,text='EXIT',width=5,bd=5, height=1,bg="white",font=("verdana",11,"bold"),command=partial(mainer_caller,encryp_window))
    encrypt_exit.place(relx=0.80,rely=0.0045)

    ##textbox for taking text to be encrypted
    tk.Label(encryp_window,text='ENTER TEXT BELOW').place(relx=0.1,rely=0.10)
    enc_text=Text(encryp_window,width=40,height=10)
    enc_text.place(relx=0.1,rely=0.15)

    ##button to start encryption
    but=Button(encryp_window,text='Encrypt',command=partial(encryption,enc_text))
    but.place(relx=0.1,rely=0.45)

    ##
    encryp_window.mainloop()

def GUI_DECRYPTOR():
    global decryp_window,root

    decryp_window=tk.Tk()
    decryp_window.geometry("400x300")
    decryp_window.title('DECRYPTOR')
    decryp_window.configure(background='white')
    root.destroy()
    title=tk.Label(decryp_window,text='DECRYPTOR',font={'verdana','100','italic bold'},bg='red',fg='white',bd=8,width=70)
    title.pack(fill=Y,side=TOP)
    decrypt_exit=tk.Button(decryp_window,text='EXIT',width=5,bd=5, height=1,bg="white",font=("verdana",11,"bold"),command=partial(mainer_caller,decryp_window))
    decrypt_exit.place(relx=0.80,rely=0.0045)

    tk.Label(decryp_window,text='FIND YOUR FILE BY CLICKING ON THE BUTTON').place(relx=0.1,rely=0.20)
    d_button=Button(decryp_window,text='choose',command=target_caller)
    d_button.place(relx=0.1,rely=0.3)

    decryp_window.mainloop()

def mainer_caller(win):
    win.destroy()
    mainer()
#############BAAKI KAL###############
def mainer():
    global root
    root=tk.Tk()
    root.geometry("400x300")
    root.title('RSA')
    root.configure(background='white')
    title=tk.Label(text='RSA',font={'verdana','100','italic bold'},bg='red',fg='white',bd=8,width=70)
    title.pack(fill=Y,side=TOP)
    encrypt=tk.Button(text='ENCRYPTION',width=12,bd=5, height=1,bg="white",font=("verdana",11,"bold"),command=GUI_ENCRYPTOR)
    encrypt.place(relx=0.35,rely=0.3)
    encrypt=tk.Button(text='DECRYPTION',width=12,bd=5, height=1,bg="white",font=("verdana",11,"bold"),command=GUI_DECRYPTOR)
    encrypt.place(relx=0.35,rely=0.5)
    exit_b=tk.Button(root,text='EXIT',width=6,bd=5, height=1,bg="white",font=("verdana",11,"bold"),command=exit)
    exit_b.place(relx=0.80,rely=0.0045)
    root.mainloop()
if __name__=='__main__':
    mainer()
