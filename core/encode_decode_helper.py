# outsourced core and utils to extra files, to keep this main util script simple and short
# with this approach it is also easier to switch from cv2 to any other framework
from .core import *
from .utils import *
import pickle

"""
quality_ratio = is used for the quantization step (higher is better)
subsampling_factor = is used for subsampling (lower is better, best is 1 = no subsampling)
"""
def image_to_compressed_bin(image_path, bin_file_path, subsampling_factor=16, compression_rate=100):
    quality_ratio = 101 - compression_rate # convert it, to make the highest value to the best quality
    img = read_img(image_path)
    yuv_img = rgb_to_yuv(img)
    y, u, v = split_channels(yuv_img)
    y_obj, u_obj, v_obj = compress(y, u, v, subsampling_factor, quality_ratio)

    # img
    img_dict = {
        "y": y_obj.to_dict(),
        "u": u_obj.to_dict(),
        "v": v_obj.to_dict()
    }

    # save it in bin format
    with open(bin_file_path, 'wb') as file:
        pickle.dump(img_dict, file)

def compressed_bin_to_image(bin_file_path, result_image_path):
    # load it from file
    with open(bin_file_path, 'rb') as file:
        loaded_data_dict = pickle.load(file)

    # map object from dict
    y_obj = Channel.from_dict(loaded_data_dict.get('y'))
    y_obj.decode()

    u_obj = Channel.from_dict(loaded_data_dict.get('u'))
    u_obj.decode()

    v_obj = Channel.from_dict(loaded_data_dict.get('v'))
    v_obj.decode()

    # split the channels
    decompressed_y, decompressed_u, decompressed_v = decompress(y_obj, u_obj, v_obj)

    # merge channels
    decompressed_yuv_img = merge_channels(decompressed_y, decompressed_u, decompressed_v)
    # decompressed_yuv_img = merge_channels(y, u, v)
    decompressed_rgb_img = yuv_to_rgb(decompressed_yuv_img)
    # decompressed_rgb_img = yuv_to_rgb(yuv_img)
    save_img(decompressed_rgb_img, result_image_path)