import cv2
import numpy as np
from PIL import Image


class ImagePreprocessingMethods:

    @staticmethod
    def run_method_on_multiple_images(images, method):
        return [method(image) for image in images]

    @staticmethod
    def get_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def median_blur(image, c):
        return cv2.medianBlur(image, c)  # todo bilateral

    @staticmethod
    def gaussian_blur(image, c):
        return cv2.GaussianBlur(image, )  # todo bilateral

    @staticmethod
    def averaging_blur(image, c):
        return cv2.medianBlur(image, c)  # todo bilateral

    @staticmethod
    def bilateral_filter(image, c):
        return cv2.medianBlur(image, c)  # todo bilateral

    @staticmethod
    def non_local_means_denosing(image, c):
        return cv2.medianBlur(image, c)  # todo bilateral

    # thresholding
    @staticmethod
    def __thresholding(image):
        return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 19, 8)

    # dilation
    @staticmethod
    def __dilate(image, kernel_value, iteration_value):
        kernel = np.ones((kernel_value, kernel_value), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_DILATE, kernel, iterations=iteration_value)

    # erosion
    @staticmethod
    def __erode(image, kernel_value, iteration_value):
        kernel = np.ones((kernel_value, kernel_value), np.uint8)
        return cv2.erode(image, kernel, iterations=iteration_value)

    # opening - erosion followed by dilation
    @staticmethod
    def __opening(image, kernel_value, iteration_value):
        kernel = np.ones((kernel_value, kernel_value), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=iteration_value)

    @staticmethod
    def __closing(image, kernel_value, iteration_value):
        kernel = np.ones((kernel_value, kernel_value), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=iteration_value)

    # skew correction
    @staticmethod
    def deskew(image):
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
    def load_file(path):
        """ Loads a .jp2 file from a given path
        :param path: The path of the file
        :return: The file in RGB format
        """
        image_cv2 = cv2.imread(path)
        return image_cv2

    @staticmethod
    def __convert_to_pil(image):
        return Image.fromarray(image)

    @classmethod
    def add_border(cls, image, param):
        pass
    @classmethod
    def dewarp(cls, image):
        #https://mzucker.github.io/2016/08/15/page-dewarping.html

        pass

#
