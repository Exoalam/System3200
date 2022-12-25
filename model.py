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

class ResidualDenseBlock(tf.keras.Model):
  def __init__(self):
    super(ResidualDenseBlock, self).__init__()
    self.conv_1 = layers.Conv2D(32, (3, 3), strides=(1, 1), padding="SAME")
    self.conv_2 = layers.Conv2D(32, (3, 3), strides=(1, 1), padding="SAME")
    self.conv_3 = layers.Conv2D(32, (3, 3), strides=(1, 1), padding="SAME")
    self.conv_4 = layers.Conv2D(32, (3, 3), strides=(1, 1), padding="SAME")
    self.conv_5 = layers.Conv2D(64, (3, 3), strides=(1, 1), padding="SAME")

    self.activation_1 = tf.keras.layers.LeakyReLU(alpha=0.2)
    self.activation_2 = tf.keras.layers.LeakyReLU(alpha=0.2)
    self.activation_3 = tf.keras.layers.LeakyReLU(alpha=0.2)
    self.activation_4 = tf.keras.layers.LeakyReLU(alpha=0.2)
  
  def call(self, x):
    x1 = self.activation_1(self.conv_1(x))
    x2 = self.activation_2(self.conv_2(layers.concatenate([x, x1])))
    x3 = self.activation_3(self.conv_3(layers.concatenate([x, x1, x2])))
    x4 = self.activation_4(self.conv_4(layers.concatenate([x, x1, x2, x3])))
    x5 = self.conv_5(layers.concatenate([x, x1, x2, x3, x4]))

    # Emperically, we use 0.2 to scale the residual for better performance
    return x5 * 0.2 + x

class RRDB(tf.keras.Model):
  def __init__(self):
    super(RRDB, self).__init__()
    self.res_1 = ResidualDenseBlock()
    self.res_2 = ResidualDenseBlock()
    self.res_3 = ResidualDenseBlock()
  
  def call(self, x_input):
    x = self.res_1(x_input)
    x = self.res_2(x)
    x = self.res_3(x)

    return x * 0.2 + x_input

class RRDBNet(tf.keras.Model):
  def __init__(self):
    super(RRDBNet, self).__init__()
    self.first_conv = layers.Conv2D(64, (3, 3), strides=(1, 1), padding="SAME") # padding 1
    self.rb_1 = RRDB()
    self.rb_2 = RRDB()
    self.rb_3 = RRDB()
    self.rb_4 = RRDB()
    self.rb_5 = RRDB()
    self.rb_6 = RRDB()
    self.conv_body = layers.Conv2D(64, (3, 3), strides=(1, 1), padding="SAME") # padding 1

    self.up_1 = layers.UpSampling2D()
    self.conv_1 = layers.Conv2D(64, (3, 3), strides=(1, 1), padding="SAME") # padding 1
    self.activation_1 = tf.keras.layers.LeakyReLU(alpha=0.2)

    self.up_2 = layers.UpSampling2D()
    self.conv_2 = layers.Conv2D(64, (3, 3), strides=(1, 1), padding="SAME") # padding 1
    self.activation_2 = tf.keras.layers.LeakyReLU(alpha=0.2)

    self.conv_3 = layers.Conv2D(64, (3, 3), strides=(1, 1), padding="SAME") # padding 1
    self.activation_3 = tf.keras.layers.LeakyReLU(alpha=0.2)
    self.conv_4 = layers.Conv2D(3, (3, 3), strides=(1, 1), padding="SAME") # padding 1
    
  def call(self, x_input):
    x = self.first_conv(x_input)
    x1 = self.rb_1(x)
    x1 = self.rb_2(x1)
    x1 = self.rb_3(x1)
    x1 = self.rb_4(x1)
    x1 = self.rb_5(x1)
    x1 = self.rb_6(x1)
    x1 = self.conv_body(x1)

    x = x + x1

    x = self.up_1(x)
    x = self.conv_1(x)
    x = self.activation_1(x)

    x = self.up_2(x)
    x = self.conv_2(x)
    x = self.activation_2(x)

    x = self.conv_3(x)
    x = self.activation_3(x)
    x = self.conv_4(x)

    return x