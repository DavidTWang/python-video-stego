from pyimage import *
from pyutils import *
import argparse
import sys
# Don't write pyc files
sys.dont_write_bytecode = True
# Allowed filetypes for images. Different for output files.
ALLOWED_IMAGE_FILETYPES = [
    "jpg", "png", "bmp", "eps"
]


# ========================================================================
# Function: parse_arguments
# Input:    None
# Return:   A list[] of CLI arguments
# Desc.:    Using the argparse library, this function parses CLI arguments
#           provided for pystego. Arguments must contain either
#           [-e | --encode] or [-d | --decode]. An optional output
#           argument can be used to specify desired output filename
# ========================================================================
def parse_arguments():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--encode", action="store", nargs=2, metavar=("image", "file"), help="Encode a file into the image")
    group.add_argument("-d", "--decode", action="store", nargs=1, metavar="image", help="Decode the image into a file")
    parser.add_argument("-o", "--output", action="store", help="Optional output filename")
    return parser.parse_args()


# ========================================================================
# Function: check_image_filetype
# Input:    filename    - Path to image file
#           output      - Whether the file is an output file
# Return:   None
# Desc.:    Checks whether or not the file provided as an image is an
#           acceptable image for processing.
# ========================================================================
def check_image_filetype(filename, output=False):
    global ALLOWED_IMAGE_FILETYPES
    # Split the filepath/flename from the right
    fname = filename.rsplit(".", 1)
    if(len(fname) != 2):  # If no period is found
        exit("Invalid image file provided: %s" % filename)
    if(output is True):  # If we're processing an output filename
        ALLOWED_IMAGE_FILETYPES = ["png", "bmp"]
    if(fname[1].lower() not in ALLOWED_IMAGE_FILETYPES):
        exit("Image type not supported: %s.%s" % (fname[0], fname[1]))


# ========================================================================
# Function: check_file_exists()
# Input:    filepath - Path to a file
# Return:   None
# Desc.:    Checks if the file exists at the filepath. Uses getsize
#           instead os.path.isfile() because isfile does not always work.
# ========================================================================
def check_file_exists(filepath):
    try:
        os.path.getsize(filepath)
    except OSError as e:
        exit(e)


# ========================================================================
# Function: main()
# Input:    None
# Return:   None
# Desc.:    The main controller for pystego. Parses the arguments provided
#           in CLI and actives the tools accordingly. Mainly serves as an
#           input sanitization before calling the encode and decode
#           functions.
# ========================================================================
def main():
    args = parse_arguments()
    if(args.encode is not None):  # If we're encoding
        # Check if files exist
        check_file_exists(args.encode[0])
        check_file_exists(args.encode[1])
        # Check if image provided is valid
        check_image_filetype(args.encode[0])
        # Check if output is an image format
        if(args.output is not None):
            check_image_filetype(args.output, True)
        # Encode the image
        output = stego_image(args.encode[0], args.encode[1], args.output)
        # Announce result
        print("Image Encoded as: %s" % output)
    elif(args.decode is not None):  # If we're decoding
        # Check if file exists
        check_file_exists(args.decode[0])
        # Check if image provided is valid
        check_image_filetype(args.decode[0])
        # Decode the image
        output = decode_image(args.decode[0], args.output)
        # Announce result
        print("File extracted and saved as: %s" % output)

    else:  # Failsafe
        exit("An unexpected error has occured. Please check your arguments.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Terminate signal received. Exiting...")
