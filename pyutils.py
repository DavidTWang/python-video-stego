from pyimage import *
import os


# ========================================================================
# Function: stego_image
# Input:    image_path  - String path to the image to hide in
#           file_path   - String path to the file to be hidden
#           output      - Output filename. Will be changed if null
# Return:   output      - Output filename after the file is saved
# Desc.:    Main function to perform steganography on an image by hiding
#           a file within the image's least significant bit (LSB).
#           Information regarding the file's name and size is embedded
#           as header data seperated by two null characters.
#           Note that the file to be hidden cannot exceed the max size
#           allowed which is set to width * height of the image multiplied
#           by 3 (for 3 color channels) and divided by 8 (8 bits per byte)
#
#           By default this saves the encoded image as "stego.BMP". If
#           an output variable other than null is provided then the
#           program will attempt to save it with that name and that file
#           format (Either PNG or BMP, due to lossless limitations)
# ========================================================================
def stego_image(image_path, file_path, output):
    # Open the image and get its dimensions
    img = open_image(image_path)
    width, height = img.size
    # Calculate the maximum about of bytes that can be stored
    max_size = width * height * 3 / 8

    # Open the file and get its header information
    file = open(file_path, 'rb')
    filename = os.path.basename(file_path)
    filesize = os.path.getsize(file_path)

    # Create the file header and calculate its length
    file_header = filename + "\0" + str(filesize) + "\0"
    file_header_size = len(str_to_binary(file_header))

    # If the file's size and the header exceeds the maximum allowed size
    if(filesize + file_header_size > max_size):
        exit("File too large for image: {} in {}".format(filesize, max_size))
    # Convert and combine the header and file data to binary
    binary = str_to_binary(file_header) + ''.join(file_to_binary(file))
    # Go through the image and write the file's data into each pixel's LSBs
    image_data = process_image(img, binary)
    # Save the new image
    img.putdata(image_data)
    if(output is None):
        output = "stego.BMP"
    img.save(output)
    return output


# ========================================================================
# Function: decode_image()
# Input:    image_path  - Path to an image
#           output      - Output filename
# Return:   output      - Saved file's filename
# Desc.:    Undo the steganography performed by stego_image() found above.
#           Extracts information from the least significant bit of each
#           color channel of each pixel in an image and writes it to a
#           file.
#           The file header is extracted and seperated from the actual
#           data contents of the file in order to know which portion
#           of the image contains the hidden file. By default the output
#           file's filename will be taken from the header.
# ========================================================================
def decode_image(image_path, output):
    # Opens the image
    img = open_image(image_path)
    # Get pixel information from the image
    pixels = img.getdata()
    result = []
    # For each color band of eacn pixel
    for pixel in pixels:
        for color in pixel:
            # Get the LSB and append it to a list
            result.append(get_lsb(color))
    # Convert the list into binary
    n = int(''.join(result), 2)
    # Convert the binary into an ascii representation and extract the header
    filename, filesize, data = get_header(binascii.unhexlify('%x' % n))

    # Save the output file
    if(output is None):
        output = "decoded_{}".format(filename)
    with open(output, 'wb') as f:
        f.write(data[:int(filesize)])
    return output

if __name__ == '__main__':
    exit("Please run from pystego.py.")
