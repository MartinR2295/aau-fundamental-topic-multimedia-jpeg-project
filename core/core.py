import cv2
import numpy as np
from .core_utils import *
from .encoding_utils import *

class Channel:

    def __init__(self, data):
        self.data = data
        self.shape = data.shape
        self.compressed_blocks = None
        self.subsampled_data = None
        self.subsampling_factor = None
        self.quantization_table = None
        self.huffman_codec = None
        self.encoded_block = None

    def subsample(self, subsampling_factor):
        self.subsampling_factor = subsampling_factor
        self.subsampled_data = cv2.resize(self.data, (self.data.shape[1] // subsampling_factor, self.data.shape[0] // subsampling_factor))

    def de_subsample(self):
        self.data = cv2.resize(self.subsampled_data, (self.shape[1], self.shape[0]))

    def compress(self, quantization_table):
        # split y part to 8x8 blocks
        y_blocks = split_to_blocks_with_padding(self.data)

        # do dct to each block (need to convert to values between 0 and 1)
        dct_blocks = dct_block_array(y_blocks/255.0)*255

        # do quantization to each block
        quantized_blocks = quantize_dct_blocks(dct_blocks, quantization_table)

        # save it in this object
        self.compressed_blocks = quantized_blocks
        self.quantization_table = quantization_table

        return quantized_blocks

    def de_compress(self):
        de_quantized_blocks = de_quantize_dct_blocks(self.compressed_blocks, self.quantization_table)
        inversed_dct_blocks = (inverse_dct_block_array(de_quantized_blocks/255.0)*255.0).astype(np.uint8)
        self.data = reconstruct_from_blocks(inversed_dct_blocks, self.shape)

    """
    Compress it first
    """
    def encode(self):
        self.huffman_codec = get_huffman_codec(self.compressed_blocks)
        self.encoded_block = encode_huffman_block(self.compressed_blocks, self.huffman_codec)
        return self.encoded_block

    def decode(self):
        height, width = self.shape
        block_size = 8
        num_blocks_y = (height + block_size - 1) // block_size
        num_blocks_x = (width + block_size - 1) // block_size
        self.compressed_blocks = decode_huffman_block(self.encoded_block, self.huffman_codec, (num_blocks_y, num_blocks_x, 8, 8))

    def to_dict(self):
        return {
            "encoded_block": self.encoded_block,
            "height": self.shape[0],
            "width": self.shape[1],
            "huffman_codec": self.huffman_codec,
            "subsampling_factor": self.subsampling_factor,
            "quantization_table": self.quantization_table
        }

    @staticmethod
    def from_dict(dict):
        channel = Channel(np.zeros((dict.get('height'), dict.get('width'))))
        channel.encoded_block = dict.get('encoded_block')
        channel.huffman_codec = dict.get('huffman_codec')
        channel.subsampling_factor = dict.get('subsampling_factor')
        channel.quantization_table = dict.get('quantization_table')
        return channel

def compress(y, u, v, subsampling_factor, quality_ratio=100):
    # create the objects
    y_obj = Channel(y)
    u_obj = Channel(u)
    v_obj = Channel(v)

    # subsample
    u_obj.subsample(subsampling_factor)
    v_obj.subsample(subsampling_factor)

    # do y compression part
    y_quantization_table = generate_quantization_matrix(quality_ratio)
    y_obj.compress(y_quantization_table)

    # encode each channel
    y_obj.encode()

    return y_obj, u_obj, v_obj

def decompress(y_obj: Channel, u_obj: Channel, v_obj: Channel):
    # de_subsampling
    u_obj.de_subsample()
    v_obj.de_subsample()

    # do the y part
    y_obj.de_compress()

    return y_obj.data, u_obj.data, v_obj.data
