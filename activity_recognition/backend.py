"""import os

os.environ["KERAS_BACKEND"] = "theano"
import keras"""

import keras
print(keras.backend.backend())

from flask import request, render_template, redirect, url_for, Flask
import numpy as np
import time, random
from selenium import webdriver
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
std = StandardScaler()

model = load_model('activity_model4_tens_balanced_std.h5')

options = webdriver.ChromeOptions()
options.add_argument('headless')

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for("checker"))

map_dic = {2: 'Downstairs',
           4: 'Jogging',
           1: 'Sitting',
           5: 'Standing',
           3: 'Upstairs',
           0: 'Walking'}


def send_for_prediction(data):
    data = np.array(data)
    data = std.fit_transform(data)
    print(data.shape)
    data = data.reshape(1, 20, 3, 1)
    prediction = np.argmax(model.predict(data))
    print(model.predict(data))
    output = map_dic[prediction]
    print(output)
    return output

cumulated_data = []
time_frame = 20

action = 'checking...'
@app.route('/checker', methods=["POST", "GET"])

def checker():
    global cumulated_data, action
    if request.method == 'POST':

        x = request.form["id_x"]
        y = request.form["id_y"]
        z = request.form["id_z"]
        print(len(cumulated_data), x)
        if len(cumulated_data) < time_frame:
            try:
                cumulated_data.append([float(x), float(y), float(z)])
            except:
                pass
            return render_template('index.html', x=x, y=y, z=z, content=action)
        else:
            action = send_for_prediction(cumulated_data)
            cumulated_data = []
            return render_template('index.html', x=x, y=y, z=z, content=action)

    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(host='192.168.43.166', port=5000, debug=True)
    print('here')
