from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os,cv2
import urllib.request
import speech_recognition as sr
import nltk,time
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from string import punctuation
import shutil

nltk.download('punkt')
stop_words = set(stopwords.words('english'))

def get_image(keywords):
    browser=webdriver.Chrome(executable_path='C:\\Users\\tusha\\Downloads\\chromedriver.exe')
    c=0
    for keyword in keywords:
        browser.get('https://www.google.com')
        search = browser.find_element_by_name("q")
        search.send_keys(keyword,Keys.ENTER)
        elem = browser.find_element_by_link_text("Images")
        elem.get_attribute("href")
        elem.click()


        div_body = browser.find_element_by_id('islrg')
        sub = div_body.find_elements_by_tag_name('img')
        sub = sub[3:]
        print(len(sub))
        try:
            os.mkdir("downloads")
        except FileExistsError:
            pass

        for i in sub:
            src = i.get_attribute('src')
            try:
                if src != None:
                    src  = str(src)
                    print(keyword + ' done')
                    urllib.request.urlretrieve(src, os.path.join('downloads',str(c)+'.jpg'))
                    break
                else:
                    raise TypeError
            except TypeError:
                print('fail')
        c+=1
    browser.quit()

def start_taking_voice_command():
    print('speak')
    text=''
    r=sr.Recognizer()
    with sr.Microphone() as source:
        audio=r.listen(source)
        try:
            text=r.recognize_google(audio)
        except:
            speak('Try again...')
    return text

def process(raw_data):
    word_tokens = word_tokenize(raw_data)
    doc = [w for w in word_tokens if not w in stop_words]
    return doc

def make_video():
    path = 'downloads\\'

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('video.avi', fourcc, 20.0, (480, 360))

    all_images = list(os.listdir(path))

    for i in range(len(all_images)):

        try:

            img_path = path + "{}.jpg".format(i)
            img = cv2.imread(img_path)
            img = cv2.resize(img,(480,360),interpolation=cv2.INTER_AREA)
            for _ in range(90):
                out.write(img)

            cv2.imshow('original',img)
            if cv2.waitKey(1)==ord('q'):
                break
        except:
            break
    shutil.rmtree(path)

if __name__ =="__main__":

    while True:
        raw_data = start_taking_voice_command()
        print(raw_data)
        keywords = process(raw_data)
        print(keywords)
        get_image(keywords)

        make_video()

