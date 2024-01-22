#!/usr/bin/env python3
import argparse
# all of the logic is outsourced to the core, there you can find every step of the jpeg algorithm
from core.psnr_utils import calc_psnr
from core.utils import read_img

def main():
    parser = argparse.ArgumentParser(description="PSNR Script")

    # Command line options
    parser.add_argument("-o", "--original_file", type=str, required=True, help="Path to the original file")
    parser.add_argument("-c", "--compressed_file", type=str, required=True, help="Path to the compressed file")

    args = parser.parse_args()

    psnr = calc_psnr(read_img(args.original_file), read_img(args.compressed_file))
    print(f"PSNR: {psnr}")


if __name__ == "__main__":
    main()
