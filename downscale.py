import re
import os
from PIL import Image
from matplotlib import pyplot
from skimage.transform import resize, rescale
class Downscale():
    def save():
        for root, dirnames, filenames in os.walk("Temp"):
            for filename in filenames:
                if re.search("\.(jpg|jpeg|JPEG|png|bmp|tiff)$", filename):
                    filepath = os.path.join(root, filename)
                    image = pyplot.imread(filepath)
                    image_resized = resize(image, (512, 512))
                    pyplot.imsave('Storage/' + filename, image_resized)