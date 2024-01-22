# outsourced core and utils to extra files, to keep the main script simple and short
# with this approach it is also easier to switch from cv2 to any other framework
from core.core import *
from core.utils import *


def main():

    subsampling_factor = 16  # compress the u and v channels to 1/16
    quality_ratio = 100 # higher is better

    img = read_img("test.png")
    yuv_img = rgb_to_yuv(img)
    y, u, v = split_channels(yuv_img)
    compressed_y, compressed_u, compressed_v, \
        y_quantization_table, uv_quantization_table, original_shape = compress(y, u, v, subsampling_factor, quality_ratio)

    # save it in bin format

    # outsource this part to a decompress file

    # split the channels
    decompressed_y, decompressed_u, decompressed_v = decompress(compressed_y, compressed_u, compressed_v,
                                                                y_quantization_table, uv_quantization_table,
                                                                original_shape)

    # merge channels
    decompressed_yuv_img = merge_channels(decompressed_y, decompressed_u, decompressed_v)
    # decompressed_yuv_img = merge_channels(y, u, v)
    decompressed_rgb_img = yuv_to_rgb(decompressed_yuv_img)
    # decompressed_rgb_img = yuv_to_rgb(yuv_img)
    save_img(decompressed_rgb_img, "result.png")

main()