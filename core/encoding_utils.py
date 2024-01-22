from dahuffman import HuffmanCodec
import numpy as np

def encode_huffman_block(block, huffman_codec):
    flattened_block = block.flatten()
    encoded_block = huffman_codec.encode(flattened_block)
    return encoded_block

def decode_huffman_block(encoded_block, huffman_codec, block_shape=(8, 8)):
    flattened_block = huffman_codec.decode(encoded_block)
    return np.array(flattened_block).reshape(block_shape)

def get_huffman_codec(block):
    flattened_block = block.flatten()
    return HuffmanCodec.from_data(flattened_block)