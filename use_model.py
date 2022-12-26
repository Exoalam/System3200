import tensorflow as tf
import os
import re

class Generator:
    def output():
                filename = os.path.abspath("./Storage/*.jpg")
                #model = tf.keras.models.load_model('models/ema_gan_model')
                model = tf.keras.models.load_model('models/gan_model')
                print(filename)
                output = model("./Storage/frame0.jpg")
                tf.keras.utils.save_img(filename, output)
