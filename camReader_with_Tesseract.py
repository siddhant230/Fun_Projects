import pytesseract
import cv2
import playsound
import pyttsx3,urllib.request
import pyscreenshot as imageGrab
import numpy as np

##########keeping tesseract in path###########
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
##############################################
def speaker(text):
    '''obj=gtts.gTTS(text=text,lang='en',slow=False)'''  #you need to have pyttsx3 installed along with libspeak
                                          #otherwise you can simply use gtts; you just need internet connection for it.
    engine=pyttsx3.init()
    engine.say(text)
    engine.setProperty('rate',50)
    engine.setProperty('volume',1.0)
    engine.runAndWait()

def helper():
    img=cv2.imread('saved.png')
    text=pytesseract.image_to_string(img,lang='eng')
    print(text)
    speaker(text)

count=0
cap=cv2.VideoCapture('http://172.21.160.127:8080/shot.jpg')
url='http://172.21.160.127:8080/shot.jpg'
while True:
    if count%30==0 and count!=0:
        cv2.imwrite('saved.png',img)
        ####tesseract helper function
        helper()
    count+=1
    print(count)
    ############picking up the image and converting it to usable form numpy array.
    imgResp = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img = cv2.imdecode(imgNp,-1)
    cv2.imshow('img',img)
    width,height,dim=img.shape
    if cv2.waitKey(1)==ord('q'):
        break
