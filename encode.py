#!/usr/bin/env python3
import argparse
# all of the logic is outsourced to the core, there you can find every step of the jpeg algorithm
from core.encode_decode_helper import image_to_compressed_bin

def main():
    parser = argparse.ArgumentParser(description="JPEG Compression Script")

    # Command line options
    parser.add_argument("-s", "--subsampling_factor", type=int, default=16, help="Subsampling factor for U and V channels (like 1, 2, 4, 8, 16, 32, etc.)")
    parser.add_argument("-c", "--compression_rate", type=int, default=50, help="Compression Rate (1-100)")
    parser.add_argument("-i", "--image_file", type=str, required=True, help="Path to the input image file")
    parser.add_argument("-o", "--encoded_file", type=str, required=True, help="Path to the output encoded binary file")

    args = parser.parse_args()

    # Encode the image and save it to a file
    image_to_compressed_bin(
        args.image_file,
        args.encoded_file,
        subsampling_factor=args.subsampling_factor,
        compression_rate=args.compression_rate
    )

    print("Image encoded")


if __name__ == "__main__":
    main()
