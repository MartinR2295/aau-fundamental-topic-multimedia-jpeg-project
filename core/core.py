import cv2
import numpy as np
from .core_utils import *

def compress(y, u, v, subsampling_factor, quality_ratio=100):
    u_downscaled = cv2.resize(u, (u.shape[1] // subsampling_factor, u.shape[0] // subsampling_factor))
    v_downscaled = cv2.resize(v, (v.shape[1] // subsampling_factor, v.shape[0] // subsampling_factor))

    # split y part to 8x8 blocks
    y_blocks = split_to_blocks_with_padding(y)

    # do dct to each block (need to convert to values between 0 and 1)
    dct_blocks = dct_block_array(y_blocks/255.0)*255

    # do quantization to each block
    uv_quantization_table = generate_quantization_matrix(quality_ratio)
    y_quantization_table = generate_quantization_matrix(quality_ratio)
    quantized_blocks = quantize_dct_blocks(dct_blocks, y_quantization_table)

    return quantized_blocks, u_downscaled, v_downscaled, y_quantization_table, uv_quantization_table, y.shape


def decompress(y_blocks, u_downscaled, v_downscaled, y_quantization_table, uv_quantization_table, original_shape):
    # upscale the U component
    u = cv2.resize(u_downscaled, (original_shape[1], original_shape[0]))
    # upscale the V component
    v = cv2.resize(v_downscaled, (original_shape[1], original_shape[0]))

    # do the y part
    de_quantized_blocks = de_quantize_dct_blocks(y_blocks, y_quantization_table)
    inversed_dct_blocks = (inverse_dct_block_array(de_quantized_blocks/255.0)*255.0).astype(np.uint8)
    y = reconstruct_from_blocks(inversed_dct_blocks, original_shape)

    return y, u, v