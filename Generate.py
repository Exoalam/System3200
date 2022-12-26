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
    def esrgan(): 
        autoencoder = RRDBNet()
        autoencoder.compile(optimizer = 'adadelta', loss = 'mean_squared_error')
        autoencoder.load_weights('weight/weights')
        for root, dirnames, filenames in os.walk("Storage"):
            for filename in filenames:
                if re.search("\.(jpg|jpeg|JPEG|png|bmp|tiff|PNG)$", filename):
                    filepath = os.path.join(root, filename)
                    image = pyplot.imread(filepath)
                    image = resize(image, (512, 512))
                    data = []
                    data.append(image)
                    data = np.array(data)
                    data = np.clip(autoencoder.predict(data), 0.0, 1.0)
                    pyplot.imsave('Output/' + filename,data[0])