from PIL import Image
import binascii


# ========================================================================
# Function: open_image()
# Input:    path    - Path to the image
# Return:   An image object
# Desc.:    Opens an image, if the image doesn't exist then print the
#           exception and return
# ========================================================================
def open_image(path):
    image = None
    try:
        image = Image.open(path)
    except Exception as e:
        print("Image not found")
        print(e)
        return
    return image


# ========================================================================
# Function: 
# ========================================================================
def file_to_binary(file):
    with file as f:
        byte = f.read()
        return list(bin(int('1'+binascii.hexlify(byte), 16))[3:].zfill(8))


# ========================================================================
# Function: 
# ========================================================================
def str_to_binary(string):
    return ''.join(format(ord(c), 'b').zfill(8) for c in string)


# ========================================================================
# Function: 
# ========================================================================
def get_lsb(color):
    if(color % 2 == 0):
        return '0'
    else:
        return '1'


# ========================================================================
# Function: 
# ========================================================================
def change_lsb(color, binary, index):
    if(get_lsb(color) != binary[index]):
        modified = list(bin(color)[2:].zfill(8))
        modified[-1] = binary[index]
        modified = int(''.join(modified), 2)
        return modified
    else:
        return color


# ========================================================================
# Function: 
# ========================================================================
def get_header(string):
    results = string.split('\0', 2)
    if(len(results) != 3):
        return 0
    return results


# ========================================================================
# Function: 
# ========================================================================
def process_image(image, binary):
    pixels = list(image.getdata())
    file_index = 0
    pixel_index = 0
    bits_left = len(binary)
    for pixel in pixels:
        pixels[pixel_index] = process_pixel(pixel, binary, file_index, bits_left)
        file_index += 3
        bits_left -= 3
        pixel_index += 1
        if(bits_left <= 0):
            break
    return pixels


# ========================================================================
# Function: 
# ========================================================================
def process_pixel(pixel, file_binary, index, bits_left):
    color = 0
    rgb = [pixel[0], pixel[1], pixel[2]]
    for color in range(3):
        rgb[color] = change_lsb(pixel[color], file_binary, index + color)
        bits_left -= 1
        if(bits_left == 0):
            break
    return (rgb[0], rgb[1], rgb[2])


if __name__ == '__main__':
    exit("Please run from pystego.py.")
