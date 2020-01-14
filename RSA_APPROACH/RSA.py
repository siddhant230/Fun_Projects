import pickle
import random

f=open('C:\\Users\\tusha\Desktop\RSA_APPROACH\prime_list.pkl','rb')
primes=pickle.load(f)

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
    return fin_text

if __name__=='__main__':
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

    s=input('Enter the Text : ')
    s=s.lower()
    ###encryption
    encrypted_text=encrypter(lock,s)
    ###decryption
    decrypted_text=decrypter(key,encrypted_text)
    ###cleaning of decrypted Text
    final_result=cleaner(decrypted_text,lock,key)
    print(encrypted_text,final_result)
