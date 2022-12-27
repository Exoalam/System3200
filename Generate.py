import re
import os
from PIL import Image
from matplotlib import pyplot
from skimage.transform import resize, rescale
import tensorflow as tf
from model import RRDBNet
import numpy as np
np.random.seed(0)
class Generate:
    def esrgan(images): 
        autoencoder = RRDBNet()
        autoencoder.compile(optimizer = 'adadelta', loss = 'mean_squared_error')
        autoencoder.load_weights('weight/weights')
        image = pyplot.imread(images)
        image = resize(image, (512, 512))
        data = []
        data.append(image)
        data = np.array(data)
        data = np.clip(autoencoder.predict(data), 0.0, 1.0)
        head, tail = os.path.split(images)
        pyplot.imsave('Output/' + tail,resize(data[0], (1080, 1920)))