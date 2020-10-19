import cv2
import numpy as np
from PIL import Image


class Preprocessing:

    def __init__(self):
        pass

    def do_preprocessing(self, image_path):
        image = self.__load_file(image_path)
        image = self.__get_grayscale(image)
        print(image)
        cv2.waitKey(0)
        image = self.__remove_noise(image)
        image = self.__thresholding(image)
        image = self.__deskew(image)

    @staticmethod
    def __get_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def __remove_noise(image):
        return cv2.medianBlur(image, 5)

    # thresholding
    @staticmethod
    def __thresholding(image):
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # dilation
    @staticmethod
    def __dilate(image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.dilate(image, kernel, iterations=1)

    # erosion
    @staticmethod
    def __erode(image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.erode(image, kernel, iterations=1)

    # opening - erosion followed by dilation
    @staticmethod
    def __opening(image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    # canny edge detection
    @staticmethod
    def __canny(image):
        return cv2.Canny(image, 100, 200)

    # skew correction
    @staticmethod
    def __deskew(image):
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        return rotated

    @staticmethod
    def __load_file(path):
        """ Loads a .jp2 file from a given path
        :param path: The path of the file
        :return: The file in RGB format
        """
        #image = Image.open("1988.jp2").convert("L")
        image_cv2 = cv2.imread("1988.jp2")
        return image_cv2
