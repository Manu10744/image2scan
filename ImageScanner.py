import cv2
import imutils
from skimage.filters import threshold_local


class ImageScanner:
    """ Scanner that applies edge detection in order to scan an ordinary image into a grayscale scan
        while positioning the point of view accordingly if needed. """
    def __init__(self, image):
        self.image = image

    def scan(self):
        cv2_image = cv2.imread(self.image)
        ratio = cv2_image[0] / 500.0
        original = cv2_image.copy()
        cv2_image = imutils.resize(cv2_image, height=500)
