from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPooling2D, Dropout
from tensorflow.keras.layers import Conv2DTranspose, UpSampling2D, add
from skimage.transform import resize, rescale
from tensorflow.keras.models import Model
from tensorflow.keras import regularizers
import matplotlib.pyplot as plt
from scipy import ndimage, misc
from matplotlib import pyplot
import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
np.random.seed(0)
import re
import os
from flask import Flask, render_template, url_for, request
from flask_dropzone import Dropzone
from model import RRDBNet
import os

app = Flask(__name__)
dropzone = Dropzone(app)

@app.route('/store', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join('Temp', f.filename))

    return render_template('Store.html')
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/retrieve')
def retrieve():
    return render_template('retrieve.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/signup')
def signup():
    return render_template('signup.html')
if __name__ == "__main__":
    autoencoder = RRDBNet()
    autoencoder.compile(optimizer = 'adadelta', loss = 'mean_squared_error')
    autoencoder.load_weights('weight/weights')
    app.run(debug=True)