from PIL import ImageGrab
import cv2
import numpy as np
from flask import Flask,render_template,Response

app=Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

def screen():

    while True:
        img=np.array(ImageGrab.grab(bbox=(10,10,600,1000)))
        imgencoded=cv2.imencode('.jpg',img)[1]
        strData=imgencoded.tostring()

        yield (b'--frame\r\n'b'Content-Type:text/plain\r\n\r\n'+strData+b'\r\n')


@app.route('/calc')
def calc():
    return Response(screen(),mimetype='multipart/x-mixed-replace;boundary=frame')

if __name__=='__main__':
    app.run(host='localhost',debug=True,threaded=True)
