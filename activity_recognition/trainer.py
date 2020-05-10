# creating our backend env
"""
import os

os.environ["KERAS_BACKEND"] = "theano"
import keras

print(keras.backend.backend())
"""

import pandas as pd
import matplotlib.pyplot as plt

cols = ['uid', 'activity', 'timestamp', 'x', 'y', 'z']

data_link = 'WISDM_ar_v1.1_raw.txt'
df = pd.read_csv(data_link, header=None, names=cols)
print(df.shape)
print(df.head())
