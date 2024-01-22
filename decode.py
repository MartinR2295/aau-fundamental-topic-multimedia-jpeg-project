#!/usr/bin/env python3
import argparse
# all of the logic is outsourced to the core, there you can find every step of the jpeg algorithm
from core.encode_decode_helper import compressed_bin_to_image

def main():
    parser = argparse.ArgumentParser(description="JPEG Decompression Script")

    # Command line options
    parser.add_argument("-i", "--encoded_file", type=str, required=True, help="Path to the encoded file")
    parser.add_argument("-o", "--output_file", type=str, required=True, help="Path to the output png file")

    args = parser.parse_args()

    compressed_bin_to_image(args.encoded_file, args.output_file)
    print("Image decoded")


if __name__ == "__main__":
    main()
