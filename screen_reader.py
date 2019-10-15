import pytesseract
import cv2
import playsound
import pyttsx3
import pyscreenshot as imageGrab
import numpy as np

def sound_player(path):
    playsound.playsound(path)
def speaker(text):
    '''obj=gtts.gTTS(text=text,lang='en',slow=False)'''  #you need to have pyttsx3 installed along with libspeak
                                          #otherwise you can simply use gtts; you just need internet connection for it.
    engine=pyttsx3.init()
    engine.say(text)
    engine.setProperty('rate',50)
    engine.setProperty('volume',1.0)
    engine.runAndWait()

def helper():
    img=cv2.imread('/home/parmeet/Downloads/saved.png')
    text=pytesseract.image_to_string(img,lang='eng')
    print(text)
    speaker(text)

count=0
while True:
    if count%30==0 and count!=0:
        cv2.imwrite('/home/parmeet/Downloads/saved.png',img)
        helper()
    count+=1
    print(count)
    img=imageGrab.grab()
    img=np.array(img)
    width,height,dim=img.shape
    print(img.shape)
    img=img[200:height,0:1366]
    print(img.shape)

    if cv2.waitKey(1)==ord('q'):
        break
