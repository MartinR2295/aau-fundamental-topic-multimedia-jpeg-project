#!/usr/bin/env python3
# outsourced core and utils to extra files, to keep the main script simple and short
# with this approach it is also easier to switch from cv2 to any other framework
from core.encode_decode_helper import *
from core.psnr_utils import *

def main():

    subsampling_factor = 16  # compress the u and v channels to 1/16
    quality_ratio = 100 # higher is better
    image_file = "test.png"
    encoded_file = "encoded.bin"
    output_file = "result.png"

    # encode it and save it to a file
    image_to_compressed_bin(image_file, encoded_file, subsampling_factor=subsampling_factor, compression_rate=quality_ratio)

    # load, decode it and save the decoded png file
    compressed_bin_to_image(encoded_file, output_file)

    # calculate psnr
    psnr = calc_psnr(read_img(image_file), read_img(output_file))
    print(f"PSNR: {psnr}")

main()