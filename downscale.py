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
                    if len(image.shape) > 2:
                        image_resized = resize(image, (1024, 1024))
                        dwn1 = resize(image_resized, (256, 256))
                        pyplot.imsave('Storage/' + filename,dwn1)