import speech_recognition as sr
from selenium import webdriver
import time,pyttsx3

engine=pyttsx3.init('sapi5')
voice=engine.getProperty('voices')
engine.setProperty('voices',voice[len(voice)-2].id)
speed=200
engine.setProperty('rate', speed)

def speak(text):
    print('BOT : '+text)
    engine.say(text)
    engine.runAndWait()

jump=300
req=None
curr=0
def start_taking_voice_command():
    global curr,req

    text=''
    r=sr.Recognizer()
    with sr.Microphone() as source:
        audio=r.listen(source)
        try:
            text=r.recognize_google(audio)
        except:
            speak('Try again...')
    if text!='':
        if 'scroll' in text:
            speak('Scrolling')
            driver.execute_script('window.scrollTo(0,{})'.format(curr+jump))
            curr+=jump

        elif 'friend requests' in text or 'friend request' in text:
            req=driver.find_element_by_id('fbRequestsJewel')
            req.click()

        elif 'messages' in text or 'message' in text:
            req=driver.find_element_by_id('u_0_e')
            req.click()

        elif 'notifications' in text or 'notification' in text:
            req=driver.find_element_by_id('fbNotificationsJewel')
            req.click()

        elif 'close' in text:
            req.click()

        elif 'like' in text:
            req=driver.find_element_by_class_name(' _6a-y _3l2t  _18vj')
            req.click()


if __name__=='__main__':
    driver=webdriver.Chrome(executable_path='C:\\Users\\tusha\\Downloads\\chromedriver.exe')
    driver.get('https://www.facebook.com')

    '''email=input('E-mail : ')
    password=input('Password : ')'''
    email='sidrai9211@gmail.com'
    password='#pokemon911'

    e_mail_box=driver.find_element_by_id('email')
    pass_box=driver.find_element_by_id('pass')
    e_mail_box.send_keys(email)
    pass_box.send_keys(password)

    speak('LOGGING IN...')
    speak('Please Wait for 5 seconds...')

    login_button=driver.find_element_by_id('u_0_2')
    login_button.click()

    time.sleep(5)
    speak('Logged In...')
    while True:
        start_taking_voice_command()
