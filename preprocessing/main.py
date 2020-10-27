
from os import environ as environ
environ["OPENCV_IO_ENABLE_JASPER"] = "true"
import cv2
import numpy as np
from PIL import Image


class Preprocessing:

    def __init__(self):
        pass

    def do_preprocessing_deskew(self, image_path):
        try:
            imagecv2 = self.__load_file(image_path)
        except FileNotFoundError:
            raise Exception("The image was not found in the path: " + image_path)

        image = self.__get_grayscale(imagecv2)
        image = self.__deskew(image)
        image = self.__convert_to_pil(image)

        return image

    def do_no_preprocessing(self, image_path):
        try:
            imagecv2 = self.__load_file(image_path)
        except FileNotFoundError:
            raise Exception("The image was not found in the path: " + image_path)

        image = self.__get_grayscale(imagecv2)
        image = self.__convert_to_pil(image)

        return image

    def do_preprocessing(self, image_path, name):
        try:
            imagecv2 = self.__load_file(image_path)
        except FileNotFoundError:
            raise Exception("The image was not found in the path: " + image_path)

        image = self.__get_grayscale(imagecv2)
        image = self.__thresholding(image)
        cv2.imwrite(name, image)
        return image

    def do_preprocessing_gauss(self, image_path, value, c):
        try:
            imagecv2 = self.__load_file(image_path)
        except FileNotFoundError:
            raise Exception("The image was not found in the path: " + image_path)

        image = self.__get_grayscale(imagecv2)
        image = self.__thresholding(image)
        image = self.__convert_to_pil(image)

        return image

    def do_preprocessing_mean_dilation(self, image_path, kernel_value, iteration_value):
        try:
            imagecv2 = self.__load_file(image_path)
        except FileNotFoundError:
            raise Exception("The image was not found in the path: " + image_path)

        image = self.__get_grayscale(imagecv2)
        image = self.__thresholding(image)
        image = self.__dilate(image, kernel_value, iteration_value)
        image = self.__convert_to_pil(image)

        return image

    def do_preprocessing_mean_erosion(self, image_path, kernel_value, iteration_value):
        try:
            imagecv2 = self.__load_file(image_path)
        except FileNotFoundError:
            raise Exception("The image was not found in the path: " + image_path)

        image = self.__get_grayscale(imagecv2)
        image = self.__thresholding(image)
        image = self.__erode(image, kernel_value, iteration_value)
        image = self.__convert_to_pil(image)

        return image

    def do_preprocessing_mean_opening(self, image_path, kernel_value, iteration_value):
        try:
            imagecv2 = self.__load_file(image_path)
        except FileNotFoundError:
            raise Exception("The image was not found in the path: " + image_path)

        image = self.__get_grayscale(imagecv2)
        image = self.__thresholding(image)
        image = self.__opening(image, kernel_value, iteration_value)
        image = self.__convert_to_pil(image)

        return image

    def do_preprocessing_mean_closing(self, image_path, kernel_value, iteration_value):
        try:
            imagecv2 = self.__load_file(image_path)
        except FileNotFoundError:
            raise Exception("The image was not found in the path: " + image_path)

        image = self.__get_grayscale(imagecv2)
        image = self.__thresholding(image)
        image = self.__closing(image, kernel_value, iteration_value)
        image = self.__convert_to_pil(image)

        return image

    def do_preprocessing_mean(self, image_path, value, c):
        try:
            imagecv2 = self.__load_file(image_path)
        except FileNotFoundError:
            raise Exception("The image was not found in the path: " + image_path)
        image = self.__get_grayscale(imagecv2)
        image = self.__thresholding(image)
        image = self.__convert_to_pil(image)

        return image

    def do_preprocessing_noise(self, image_path, value):
        try:
            imagecv2 = self.__load_file(image_path)
        except FileNotFoundError:
            raise Exception("The image was not found in the path: " + image_path)
        image = self.__get_grayscale(imagecv2)
        image = self.__remove_noise(image, value)
        image = self.__convert_to_pil(image)

        return image

    def do_preprocessing_noise_gauss(self, image_path, value, c, noise_value):
        try:
            imagecv2 = self.__load_file(image_path)
        except FileNotFoundError:
            raise Exception("The image was not found in the path: " + image_path)
        image = self.__get_grayscale(imagecv2)
        image = self.__remove_noise(image, noise_value)
        image = self.__thresholding(image)
        image = self.__convert_to_pil(image)

        return image

    def do_preprocessing_gauss_noise(self, image_path, value, c, noise_value):
        try:
            imagecv2 = self.__load_file(image_path)
        except FileNotFoundError:
            raise Exception("The image was not found in the path: " + image_path)
        image = self.__get_grayscale(imagecv2)
        image = self.__thresholding(image)
        image = self.__remove_noise(image, noise_value)
        image = self.__convert_to_pil(image)

        return image

    def do_preprocessing_noise_mean(self, image_path, value, c, noise_value):
        try:
            imagecv2 = self.__load_file(image_path)
        except FileNotFoundError:
            raise Exception("The image was not found in the path: " + image_path)
        image = self.__get_grayscale(imagecv2)
        image = self.__remove_noise(image, noise_value)
        image = self.__thresholding(image)
        image = self.__convert_to_pil(image)

        return image

    def do_preprocessing_mean_noise(self, image_path, value, c, noise_value):
        try:
            imagecv2 = self.__load_file(image_path)
        except FileNotFoundError:
            raise Exception("The image was not found in the path: " + image_path)
        image = self.__get_grayscale(imagecv2)
        image = self.__thresholding(image)
        image = self.__remove_noise(image, noise_value)
        image = self.__convert_to_pil(image)

        return image

    def do_preprocessing_dilate(self, image_path, kernel_value, iteration_value):
        try:
            imagecv2 = self.__load_file(image_path)
        except FileNotFoundError:
            raise Exception("The image was not found in the path: " + image_path)

        image = self.__get_grayscale(imagecv2)
        image = self.__dilate(image, kernel_value, iteration_value)
        image = self.__convert_to_pil(image)

        return image

    def do_preprocessing_erode(self, image_path, kernel_value, iteration_value):
        try:
            imagecv2 = self.__load_file(image_path)
        except FileNotFoundError:
            raise Exception("The image was not found in the path: " + image_path)

        image = self.__get_grayscale(imagecv2)
        image = self.__erode(image, kernel_value, iteration_value)
        image = self.__convert_to_pil(image)

        return image

    def do_preprocessing_opening(self, image_path, kernel_value, iteration_value):
        try:
            imagecv2 = self.__load_file(image_path)
        except FileNotFoundError:
            raise Exception("The image was not found in the path: " + image_path)

        image = self.__get_grayscale(imagecv2)
        image = self.__opening(image, kernel_value, iteration_value)
        image = self.__convert_to_pil(image)

        return image

    def do_preprocessing_closing(self, image_path, kernel_value, iteration_value):
        try:
            imagecv2 = self.__load_file(image_path)
        except FileNotFoundError:
            raise Exception("The image was not found in the path: " + image_path)

        image = self.__get_grayscale(imagecv2)
        image = self.__closing(image, kernel_value, iteration_value)
        image = self.__convert_to_pil(image)

        return image

    def do_preprocessing_median(self, image_path, kernel):
        try:
            imagecv2 = self.__load_file(image_path)
        except FileNotFoundError:
            raise Exception("The image was not found in the path: " + image_path)

        image = self.__get_grayscale(imagecv2)
        image = cv2.medianBlur(image, kernel)
        image = self.__convert_to_pil(image)

        return image

    def do_preprocessing_gauss_blur(self, image_path, kernel, sigma):
        try:
            imagecv2 = self.__load_file(image_path)
        except FileNotFoundError:
            raise Exception("The image was not found in the path: " + image_path)

        image = self.__get_grayscale(imagecv2)
        image = cv2.GaussianBlur(image, (kernel, kernel), sigma)
        image = self.__convert_to_pil(image)

        return image

    def do_preprocessing_averaging(self, image_path, kernel):
        try:
            imagecv2 = self.__load_file(image_path)
        except FileNotFoundError:
            raise Exception("The image was not found in the path: " + image_path)

        image = self.__get_grayscale(imagecv2)
        image = cv2.blur(image, (kernel, kernel))
        image = self.__convert_to_pil(image)

        return image

    def do_preprocessing_bilateral(self, image_path, d, sigma_color, sigma_space):
        try:
            imagecv2 = self.__load_file(image_path)
        except FileNotFoundError:
            raise Exception("The image was not found in the path: " + image_path)

        image = self.__get_grayscale(imagecv2)
        image = cv2.bilateralFilter(image, d, sigma_color, sigma_space)
        image = self.__convert_to_pil(image)

        return image

    @staticmethod
    def __get_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def __remove_noise(image, c):
        return cv2.medianBlur(image, c)

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
        image_cv2 = cv2.imread(path)
        return image_cv2

    @staticmethod
    def __convert_to_pil(image):
        return Image.fromarray(image)


