import numpy as np
import cv2


def split_to_blocks_with_padding(channel, block_size=8):
    # dimensions of the channel
    height, width = channel.shape

    # calculate the number of blocks in each dimension
    # do it with // operator to get full blocks, to get each pixel
    num_blocks_y = (height + block_size - 1) // block_size
    num_blocks_x = (width + block_size - 1) // block_size

    # init array with height of num_blocks_y, width of num_blocks_x where each element containing 8x8 array (or any other blocksize)
    blocks = np.zeros((num_blocks_y, num_blocks_x, block_size, block_size), dtype=channel.dtype)

    # Copy the channel into the blocks array with zero-padding
    for block_y in range(num_blocks_y):
        for block_x in range(num_blocks_x):
            for y in range(block_size):
                for x in range(block_size):
                    # pixel_y is offset of the block + current y. Same for pixel_x with x
                    pixel_y = (block_y * block_size) + y
                    pixel_x = (block_x * block_size) + x

                    # check if the pixel is there. otherwise, do nothing, and let the padding be 0
                    if pixel_y < channel.shape[0] and pixel_x < channel.shape[1]:
                        blocks[block_y, block_x, y, x] = channel[pixel_y, pixel_x]

    return blocks


def reconstruct_from_blocks(blocks, original_shape, block_size=8):
    # dimensions of the original image
    height, width = original_shape

    # initialize an array to store the reconstructed channel with the original size
    channel_reconstructed = np.zeros(original_shape, dtype=blocks.dtype)

    # copy the blocks into the reconstructed channel, except the zero paddings
    for reconstructed_y in range(height):
        for reconstructed_x in range(width):
            # get the index of the block
            block_y = int(reconstructed_y / block_size)
            block_x = int(reconstructed_x / block_size)

            # get the index of the pixel within the block
            # I did it here with the mod function, to get the rest of the division, to get the index within the block
            intern_block_y = reconstructed_y % block_size
            intern_block_x = reconstructed_x % block_size

            # copy the desired pixel
            channel_reconstructed[reconstructed_y, reconstructed_x] = blocks[
                block_y, block_x, intern_block_y, intern_block_x]

    return channel_reconstructed


def dct(block):
    return cv2.dct(block)


def inverse_dct(dct_block):
    return cv2.idct(dct_block)


def dct_block_array(blocks):
    dct_blocks = np.zeros(blocks.shape, dtype=blocks.dtype)
    for y in range(blocks.shape[0]):
        for x in range(blocks.shape[1]):
            dct_blocks[y, x] = dct(blocks[y, x])
    return dct_blocks


def inverse_dct_block_array(dct_blocks):
    blocks = np.zeros(dct_blocks.shape, dtype=dct_blocks.dtype)
    for y in range(dct_blocks.shape[0]):
        for x in range(dct_blocks.shape[1]):
            blocks[y, x] = inverse_dct(dct_blocks[y, x])
    return blocks


"""
Use luminance table as default (y channel).
If you want to use it with u or v channel, make sure to set use_chrominance_table to Ture
"""
def generate_quantization_matrix(compression_rate, use_chrominance_table=False):
    # calculate the quality
    quality = 1.0 / compression_rate

    # default JPEG quantization tables for luminance (Y) and chrominance (U and V) channels
    default_luminance_quantization_table = np.array([
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
    ])

    default_chrominance_quantization_table = np.array([
        [17, 18, 24, 47, 99, 99, 99, 99],
        [18, 21, 26, 66, 99, 99, 99, 99],
        [24, 26, 56, 99, 99, 99, 99, 99],
        [47, 66, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99]
    ])

    # choose the appropriate quantization table based on the channel
    quantization_table = default_chrominance_quantization_table if use_chrominance_table else default_luminance_quantization_table

    # adjust the quantization table based on the quality factor
    quantization_table = np.round(quality * quantization_table)

    # ensure that no element is less than 1 to avoid division by zero issues during dequantization
    quantization_table[quantization_table < 1] = 1

    return quantization_table.astype(np.int8)

def quantize_dct_blocks(dct_blocks, quantization_table):
    quantized_blocks = np.array(dct_blocks)

    for y in range(dct_blocks.shape[0]):
        for x in range(dct_blocks.shape[1]):
            quantized_blocks[y, x] = np.round(dct_blocks[y, x] / quantization_table).astype(int)

    return quantized_blocks

def de_quantize_dct_blocks(dct_blocks, quantization_table):
    quantized_blocks = np.array(dct_blocks)

    for y in range(dct_blocks.shape[0]):
        for x in range(dct_blocks.shape[1]):
            quantized_blocks[y, x] = np.round(dct_blocks[y, x] * quantization_table).astype(int)

    return quantized_blocks