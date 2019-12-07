import random,os
import speech_recognition as sr
from selenium import webdriver
import wolframalpha,gtts,pyttsx3
import datetime,wikipedia,time

engine=pyttsx3.init('sapi5')
client=wolframalpha.Client('JGQG46-Y5WTEL7J5G')
voice=engine.getProperty('voices')
engine.setProperty('voices',voice[len(voice)-1].id)
engine.setProperty('rate', 200)
options = webdriver.ChromeOptions()

###########model here#######################
def reply(text_inp):
    text=random.choice(['hey there','how are you??','may i help you??','ha ha LOL','I am fine...'])
    speak(text)
############model here#####################

def speak(text):
    print('BOT : '+text)
    engine.say(text)
    engine.runAndWait()
c=0
def listen():
    global c
    speak('How can I help?')
    r=sr.Recognizer()
    text=''
    with sr.Microphone() as source:
        audio=r.listen(source)
        try:
            text=r.recognize_google(audio)
        except:
            c+=1
            err="I can't understand what you said sir,Please try again..."
            speak(err)
            if c==2:
                err="Try writing your query..."
                speak(err)
                text=input('YOU : ')
    if text!='':
        c=0
        print('YOU : {}'.format(text))
        commands=text.split(' ')
        for i in range(len(commands)):
            commands[i]=commands[i].lower()
        if 'wait' in commands:
            speak('I am waiting...')
            time.sleep(5)
            speak('I waited for 5 seconds...')
        elif 'f***' in commands:
            speak('denge pel khatam ho jayga khel...')
            speak('Please atleast talk good, kharaab to apki shakal bhi hai...(#offence Intended)')
        elif 'weather' in commands:
            weather(commands)
        elif 'play' in commands:
            play_song(commands)
        elif 'open' in commands or 'run' in commands:
            run_command(commands)
        elif 'search' in commands or 'what' in commands or 'joke' in commands:
            search_command(commands)
        else:
            reply(text)

def play_song(commands):
    id='https://www.soundcloud.com/search/sounds?q='
    driver=webdriver.Chrome(executable_path='C:\\Users\\tusha\\Downloads\\chromedriver.exe',options=options)
    name='%20'.join(commands[1:])
    driver.get(id+name)
    try:
        driver.find_element_by_class_name('search__empty')
        speak('No such song found sir,Try again...')
        driver.quit()
    except:
        button=driver.find_element_by_class_name('soundTitle__playButton')
        button.click()

def weather(commands):
    query=' '.join(commands)
    speak("Searching for {}".format(query))
    result=client.query(query)
    opt=next(result.results).text
    speak(opt)

def search_command(commands):
    if 'joke' in commands:
        query='tell me a joke'
        result=client.query(query)
        opt=next(result.results).text
        opt=opt.split('(')[0]
    else:
        speak('searching...')
        query=' '.join(commands[1:])
        try:
            try:
                "BOT : Sure Sir!\nSearching for {}".format(query)
                speak("Searching for {}".format(query))
                result=client.query(query)
                opt=next(result.results).text
                speak("Here is what I found\nInternet says...")
                speak(opt)
            except:
                result=wikipedia.summary(query,sentences=3)
                speak("Here is what I found\nAccording to Wikipedia...")
                speak(result)
        except:
            browser=webdriver.Chrome(executable_path='C:\\Users\\tusha\\Downloads\\chromedriver.exe',options=options)
            speak("Here is what I found on Google...")
            browser.get("https://www.google.com/search?q=" + query + "&start=" + str(10 * 0))

def run_command(commands):
    speak('Opening {}'.format(''.join(commands[1:])))
    driver=webdriver.Chrome(executable_path='C:\\Users\\tusha\\Downloads\\chromedriver.exe',options=options)
    driver.get('https://www.{}.com'.format(''.join(commands[1:])))

if __name__=='__main__':
    mode='#'
    times=datetime.datetime.now().hour
    if times>=0 and times<12:
        speak('Good Morning Sir!')
    elif times>=12 and times<=16:
        speak('Good Afternoon Sir!')
    elif times>16 and times<24 and times!=0:
        speak('Good Evening Sir!')
    else:
        speak("It's already Night")

    while mode=='#':
        listen()
