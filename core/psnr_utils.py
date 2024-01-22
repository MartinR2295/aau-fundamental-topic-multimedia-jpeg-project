import numpy as np

"""
input a cv2 imported image
"""


def calc_mse(original_image, compressed_image):
    return np.mean((original_image - compressed_image) ** 2)


"""
input a cv2 imported image
"""


def calc_psnr(original_image, compressed_image):
    mse = calc_mse(original_image, compressed_image)
    return 10 * np.log10((255 ** 2) / mse)
