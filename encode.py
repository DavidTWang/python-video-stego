import moviepy.editor as mpy
import os
import binascii
import base64
from Crypto.Cipher import AES
MASTER_KEY = "CorrectHorseBatteryStapleGunHead"


def get_max_size(clip):
    width, height = (clip.w, clip.h)
    max_frames = clip.fps * clip.duration
    return (width * height * 3 / 8 / 1024) * max_frames


def encrypt_val(text):
    secret = AES.new(MASTER_KEY)
    tag_string = (str(text) + (AES.block_size - len(str(text)) % AES.block_size) * "\0")
    cipher_text = base64.b64encode(secret.encrypt(tag_string))
    return cipher_text


def file_to_binary(file):
    with file as f:
        byte = f.read()
        return list(bin(int('1'+binascii.hexlify(byte), 16))[3:].zfill(8))


def str_to_binary(string):
    return ''.join(format(ord(c), 'b').zfill(8) for c in string)


def process_pixel(pixel, file_binary, index, bits_left):
    color = 0
    rgb = [pixel[0], pixel[1], pixel[2]]
    for color in range(3):
        rgb[color] = change_lsb(pixel[color], file_binary, index + color)
        bits_left -= 1
        if(bits_left == 0):
            break
    return (rgb[0], rgb[1], rgb[2])


def get_lsb(color):
    if(color % 2 == 0):
        return '0'
    else:
        return '1'


def change_lsb(color, binary, index):
    if(get_lsb(color) != binary[index]):
        modified = list(bin(color)[2:].zfill(8))
        modified[-1] = binary[index]
        modified = int(''.join(modified), 2)
        return modified
    else:
        return color


def compare(clip1, clip2):
    frames1 = []
    frames2 = []
    [frames1.append(frame) for frame in clip1.iter_frames(dtype="uint8")]
    [frames2.append(frame) for frame in clip2.iter_frames(dtype="uint8")]

    for i1, frame in enumerate(frames1):
        for i2, pixels in enumerate(frame):
            for i3, pixel in enumerate(pixels):
                if(i3 == 100):
                    return
                pixel1 = frames1[i1][i2][i3]
                pixel2 = frames2[i1][i2][i3]
                print("Original: {}, Modified: {}".format(pixel1, pixel2))


def encode(clip, file_binary):
    frames = []
    [frames.append(frame) for frame in clip.iter_frames(dtype="uint8")]
    bits_left = len(file_binary)
    # This takes forever. In the sample there's 450+ frames and we go through
    # each and every pixel in each frame. There should be a better way to do it?
    count = 0
    for i1, frame in enumerate(frames):
        for i2, pixels in enumerate(frame):
            for i3, pixel in enumerate(pixels):
                frames[i1][i2][i3] = process_pixel(pixel, file_binary, count, bits_left)
                count += 3
                bits_left -= 3
                if(bits_left <= 0):
                    return frames


def main():
    clip = mpy.VideoFileClip('Samples/lee.webm')

    file_to_hide = 'Samples/finalproj.pdf'
    file = open(file_to_hide, 'rb')
    filesize = os.path.getsize(file_to_hide)
    file_header = os.path.basename(file_to_hide) + "\0" + str(filesize) + "\0"
    file_binary = str_to_binary(file_header) + ''.join(file_to_binary(file))

    frames = encode(clip, file_binary)

    output = mpy.ImageSequenceClip(frames, fps=clip.fps)
    output.write_videofile("output.avi", codec="png")

    # new_frames = encode(verify, file_to_hide)
    # clip = mpy.VideoFileClip('Samples/lee.webm')
    # verify = mpy.VideoFileClip('output.avi')
    # compare(clip, verify)


if __name__ == '__main__':
    main()
