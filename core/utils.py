import cv2

"""
Utils functions, which are needed/helpful for the project.
I outsourced it here, to make the main code clearer.
"""


def calc_size_of_yuv(y, u, v):
    return y.nbytes + u.nbytes + v.nbytes


def merge_channels(y, u, v):
    return cv2.merge((y, u, v))


def split_channels(yuv_img):
    return cv2.split(yuv_img)


def yuv_to_rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_YUV2BGR)


def rgb_to_yuv(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2YUV)


def save_img(rgb_img, path):
    return cv2.imwrite(path, rgb_img)


def read_img(path):
    return cv2.imread(path)
