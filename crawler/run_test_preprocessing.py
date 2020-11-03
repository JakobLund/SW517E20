# methods:
'''
Noise removal:
    - Median blur
    - Gaussian blur
    - Averaging blur
    - Bilateral filter
    - https://docs.opencv.org/3.4/d5/d69/tutorial_py_non_local_means.html
Thresholding
    - Mean
    - Gaussian
Morphological Transformations: (trash)
#    - Dilate, kernel
    - Erode, kernel, iteration (For gothic maybe?)
#    - Opening, kernel, iteration
#    - Closing, kernel, iteration
Fixing rotation etc:
    - Deskew
    - Dewarping
    - Borders around crop https://mzucker.github.io/2016/08/15/page-dewarping.html





'''
import multiprocessing
import pickle
import sys
from multiprocessing import Process, Queue

import cv2
import numpy as np
from joblib import Parallel, delayed
import argparse
import os

os.environ["OPENCV_IO_ENABLE_JASPER"] = "true"
from crawler.methods import ImagePreprocessingMethods
from crawler.method_combination import MethodCombination
from itertools import chain, combinations


# https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def load_images(images_path):
    return [ImagePreprocessingMethods.load_file(path) for path in images_path]


def apply_methods_to_images(methods, images):
    return [apply_method_to_images(method, images) for method in methods]


def apply_method_to_images(method, images):
    return Parallel(n_jobs=multiprocessing.cpu_count(), prefer="threads")(
        delayed(apply_method_to_image)(method, image)
        for image in images)


def apply_method_to_image(method, image):
    return method[1](image)


def run_test_preprocessing(images_path):
    print(images_path)

    # should be used exlusively
    noise_methods = [
        ["no_noise", lambda image: image],
        ["median blur", lambda image: cv2.medianBlur(image, 5)],
        ["gaussian blur", lambda image: cv2.GaussianBlur(image, (5, 5), 0)],
        ["averaging_blur", lambda image: cv2.filter2D(image, -1, np.ones((5, 5), np.float32) / 25)],
        ["bilateral filter", lambda image: cv2.bilateralFilter(image, 9, 75, 75)],
        ["non local means denoising", lambda image: cv2.fastNlMeansDenoising(image)],
    ]

    # should be used exlusively
    thresholding_methods = [
        ["no_thresholding", lambda image: image],
        ["mean_adaptive_thresholding",
         lambda image: cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 19, 8)],
        ["gaussian_adaptive_thresholding",
         lambda image: cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 19, 8)],
    ]

    # should be used exlusively
    morph_methods = [
        ["no_morph", lambda image: image],
        #["erosion", lambda image: cv2.morphologyEx(image, cv2.MORPH_OPEN, np.ones((kernel_value, kernel_value), np.uint8), iterations=iteration_value)]
    ]

    # not exclusive methods
    transform_methods_available = [
        ["deskew", lambda image: ImagePreprocessingMethods.deskew(image)],
        ["dewarp", lambda image: ImagePreprocessingMethods.dewarp(image)],
        ["borders", lambda image: ImagePreprocessingMethods.add_border(image,10)],

        #- Deskew
    #- Dewarping
    #- Borders around crop
    ]

    to_be_tested_combinations = []

    for noise_method in noise_methods:
        for thresholding_method in thresholding_methods:
            for morph_method in morph_methods:
                for transform_methods in powerset(transform_methods_available):
                    to_be_tested_combinations.append(
                        MethodCombination([noise_method, thresholding_method, morph_method, *transform_methods]))



    print(f"Loading {len(images_path)} images into memory..")
    original_images = load_images(images_path)
    print(f"Loaded images into memory. Total used memory: {len(pickle.dumps(original_images))}")

    print(f"Converting images into grey scale.")
    original_images = [ImagePreprocessingMethods.get_grayscale(image) for image in original_images]
    print(f"Converted images into grey scale. Total used memory: {len(pickle.dumps(original_images))}")

    combination = [noise_methods[4]]
    images = apply_methods_to_images(combination,original_images)
    cv2.imwrite("/home/knox17/Desktop/SW517e20/crawler/hejhej.tif", np.array(images[0]))

    for combination in to_be_tested_combinations:
        print(f"Testing combination {combination.get_name()}")
        processed_images = apply_methods_to_images(combination.methods, original_images)
        #todo call tesseract here


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # defines input and output path
    parser.add_argument('images_folder', help='The folder containing test images.')
    args = parser.parse_args()

    file_paths = [entry.path for entry in os.scandir(args.images_folder) if not entry.is_dir()]

    run_test_preprocessing(file_paths)
