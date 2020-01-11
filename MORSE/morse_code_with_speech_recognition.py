import pyaudio
import struct,math
from pynput.keyboard import Key,Listener
import gtts
import playsound
import time
import speech_recognition as sr

dot='/home/parmeet/Desktop/beep_sound/dot.wav'
dash='/home/parmeet/Desktop/beep_sound/dash.wav'
sound='/home/parmeet/Desktop/beep_sound/inp_sound.wav'

code=[]
thresh,RATE,sample_period,CHANNELS,SHORT_NORMALIZE = 0.02,44100,0.01,2,(1.0/32768.0)
sample_cycles,FORMAT = int(RATE*sample_period),pyaudio.paInt16

dot='/home/parmeet/Desktop/beep_sound/dot.wav'
dash='/home/parmeet/Desktop/beep_sound/dash.wav'
sound='/home/parmeet/Desktop/beep_sound/inp_sound.wav'

##to morse
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

##to text from morse
def rms(sample):
    count = len(sample)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, sample )
    sum_squares = 0.0
    for i in shorts:
        n = i * SHORT_NORMALIZE
        sum_squares += n*n
    return math.sqrt( sum_squares / count )
def decoder_sound_beta():
    pa=pyaudio.PyAudio()
    print('start')
    stream = pa.open(format = FORMAT,
             channels = CHANNELS,
             rate = RATE,
             input = True,
             frames_per_buffer = sample_cycles)
    list1=""
    duration=500
    for i in range(duration):
        try:
            sample=stream.read(sample_cycles)
        except IOError:
            print("Error Recording")
        amp=rms(sample)
        if amp>thresh:
            list1+="1"
        else:
            list1+="0"
    print(list1)
    list1=list1.split("0")
    print(list1)
    code=''
    for i in range(len(list1)):
        length=len(list1[i])
        if length<=15 and length>8 and list1[i]!='':
            print('dot')
            code+='.'
        elif length>20 and list1[i]!='':
            print('dash')
            code+='-'

    print(code)
def press(key):
    global code
    if key==Key.left:
        print('.',end='')
        code.append('.')
    elif key==Key.right:
        print('-',end='')
        code.append('-')
    elif key==Key.space:
        code.append(' ')
    elif key==Key.enter:
        return False
    else:
        code.append('/')
def button_press():
    print('Enter the MORSE CODE BELOW ')
    print('To seperate characters use space bar and for seperating word use "/" ')
    print('MORSE : ',end='')
    with Listener(on_press=press) as listener:
        listener.join()
def morse_to_text():
    global code
    code=code[:]
    s=''
    dcodes={' ': ' ',
            '.-': 'A',
            '-...': 'B',
            '-.-.': 'C',
            '-..': 'D',
            '.': 'E',
            '..-.': 'F',
            '--.': 'G',
            '....': 'H',
            '..': 'I',
            '.---': 'J',
            '-.-': 'K',
            '.-..': 'L',
            '--': 'M',
            '-.': 'N',
            '---': 'O',
            '.--.': 'P',
            '--.-': 'Q',
            '.-.': 'R',
            '...': 'S',
            '-': 'T',
            '..-': 'U',
            '...-': 'V',
            '.--': 'W',
            '-..-': 'X',
            '-.--': 'Y',
            '--..': 'Z',
            '-----': '0',
            '.----': '1',
            '..---': '2',
            '...--': '3',
            '....-': '4',
            '.....': '5',
            '-....': '6',
            '--...': '7',
            '---..': '8',
            '----.': '9'}
    for c in code:
        s+=c
    s=list((s).rsplit('/'))
    word=''
    for w in s:
        char=list(w.split())
        for c in char:
            word+=dcodes[c]
        word+=' '
    return word
def speaker(text):
    obj=gtts.gTTS(text=text,lang='en',slow=False)
    file='/home/parmeet/Desktop/beep_sound/read.mp3'
    obj.save(file)
    sound_player(file)

if __name__=='__main__':
    if input('Enter 1 if you want to convert morse to text and 2 for otherwise : ')=='1':
        button_press()
        text=morse_to_text()
        print()
        print('TEXT : ',text)
        speaker(text)
    else:
        print('Please record the sound first :')
        text=sound_recorder()
        print('The text given is : '+text)
        print('Your encoded morse code is: '+morser(text))
