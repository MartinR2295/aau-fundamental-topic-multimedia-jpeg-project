# JPEG Project
## Martin Rader - 11844898

## Needed Packages
numpy - 1.25.0<br>
opencv-python - 4.8.0.74<br>
dahuffman - 0.4.1<br>

## Coding-Style
All of the logic is outsourced to the core module.
In the core module you can find the main logic in core.py, where you can find the compress
and decompress method.
These methods are working with the Channel class, which also contains some logic, and exports/imports
the needed dictionaries.<br>
Also a lot of logic, which was included in core.py was outsourced to the util python files, which
you can find in the core module.<br>
This makes the code more readable, cleaner and more easy to extend.<br>
With that approach it is also possible, to easily replace opencv with another library,
or also to replace dahuffman with another library for the huffman encoding.

## Workflow
I have two variables for quality purposes (see in chapter encoding script).

Steps for encoding:

1. Load Image
2. Transform RGB Image to YUV
3. Subsample U and V Channel
4. Split each channel in 8x8 blocks (for missing pixels at the end of the image, I used just 0 values)
5. Apply DCT to each 8x8 block
6. Generate Quantization Matrix for Y and for U and V Channel
7. Quantize with the Quantization Matrix for all 8x8 DCT Resulting blocks (just divide each value with the same value in the quant. matrix)
8. Apply Huffman Encoding on each channel
9. Create dictionary for each channel with information like huffman_coding, binary data, size, subsampling information, quantization_matrix, etc.
10. Create a dictionary which combines all channels, and save this dictionary with pickle to a binary object.

Steps for decoding:
1. Load binary file
2. Fetch the channels out of the dictionary (with all the meta information and the huffman binary)
3. With the meta information in the dicts, decode the huffman encoded binary
4. De-quantize all channels (multiply the quant matrix)
5. Inverse DCT
6. De-Subsample U and V channel
7. Reconstruct all channels from the 8x8 blocks to have the whole channels
8. Merge the channels
9. Transform YUV to RGB
10. Save the RGB Image

## Encode and Decode Script
This script is for testing purposes. It encodes the test.png image, saves it to the project folder (encoded.bin), loads the bin file again in python
decode it and save it as png file (result.png). It also calculates the PSNR after it and shows it.

```
./encode_and_decode.py
```

## Encoding Script
This script encodes a png image to a bin file. You also can specify the subsampling ratio and the compress ratio.

```
options:
  -h, --help            show this help message and exit
  -s SUBSAMPLING_FACTOR, --subsampling_factor SUBSAMPLING_FACTOR
                        Subsampling factor for U and V channels (like 1, 2, 4, 8, 16, 32, etc.)
  -c COMPRESSION_RATE, --compression_rate COMPRESSION_RATE
                        Compression Rate (1-100)
  -i IMAGE_FILE, --image_file IMAGE_FILE
                        Path to the input image file
  -o ENCODED_FILE, --encoded_file ENCODED_FILE
                        Path to the output encoded binary file
```

Example usage for very high compression but bad quality:

```
./encode.py -i test.png -o encoded.bin -s 32 -c 100
```

Example usage for very low compression but high quality:

```
./encode.py -i test.png -o encoded.bin -s 1 -c 1
```

## Decoding Script
This script decodes an encoded image in bin format to a png format.

```
options:
  -h, --help            show this help message and exit
  -i ENCODED_FILE, --encoded_file ENCODED_FILE
                        Path to the encoded file
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Path to the output png file
```

Example usage:

```
./decode.py -i encoded.bin -o result.png
```

## PSNR Script
This script calculates the PSNR value between the original image and the compressed image

```
options:
  -h, --help            show this help message and exit
  -o ORIGINAL_FILE, --original_file ORIGINAL_FILE
                        Path to the original file
  -c COMPRESSED_FILE, --compressed_file COMPRESSED_FILE
                        Path to the compressed file
```

Example usage:

```
./psnr.py -o test.png -c result.png
```

## Example usage to use the single scripts instead of the encode_decode test script

```
# encode the image
./encode.py -i test.png -o encoded.bin -s 16 -c 1
# decode the image
./decode.py -i encoded.bin -o result.png
# calculate the psnr
./psnr.py -o test.png -c result.png
```