import playsound
import time
import sounddevice as sd
import sys
import speech_recognition as sr

dot='/home/parmeet/Desktop/beep_sound/dot.wav'
dash='/home/parmeet/Desktop/beep_sound/dash.wav'
sound='/home/parmeet/Desktop/beep_sound/inp_sound.wav'

def sound_player(path):
    playsound.playsound(path)
def sound_recorder():
    r=sr.Recognizer()

    with sr.Microphone() as source:
        print('Speak bruhh!')
        audio=r.listen(source)
        try:
            text=r.recognize_google(audio)
        except:
            print('not clear!')
        print('Recorded...')
        return text
def sound_generator(s):
    alarm_path=''
    for i in s:
        if i=='-':
            alarm_path=dash
        elif i=='.':
            alarm_path=dot
        if alarm_path!='':
            sound_player(alarm_path)
    time.sleep(0.3)
def morser(text):
    ##convert text to morse
    codes={' ': ' ',
           'A': '.-',
           'B': '-...',
           'C': '-.-.',
           'D': '-..',
           'E': '.',
           'F': '..-.',
           'G': '--.',
           'H': '....',
           'I': '..',
           'J': '.---',
           'K': '-.-',
           'L': '.-..',
           'M': '--',
           'N': '-.',
           'O': '---',
           'P': '.--.',
           'Q': '--.-',
           'R': '.-.',
           'S': '...',
           'T': '-',
           'U': '..-',
           'V': '...-',
           'W': '.--',
           'X': '-..-',
           'Y': '-.--',
           'Z': '--..',
           '0': '-----',
           '1': '.----',
           '2': '..---',
           '3': '...--',
           '4': '....-',
           '5': '.....',
           '6': '-....',
           '7': '--...',
           '8': '---..',
           '9': '----.'
           }
    gen=''
    text=text.upper()
    text=text.split(' ')
    for i in text:
        for j in i:
            converted_str=codes[j]
            sound_generator(converted_str)
            gen+=converted_str+' '
            time.sleep(0.1)
        gen+=' /  '
    return gen

if __name__=='__main__':
    print('Please record the sound first :')
    text=sound_recorder()
    print('The text given is : '+text)
    print('Your encoded morse code is: '+morser(text))
