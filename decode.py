import moviepy.editor as mpy
import binascii
import base64
from Crypto.Cipher import AES
from math import ceil
MASTER_KEY = "CorrectHorseBatteryStapleGunHead"


def decrypt_val(cipher):
    secret = AES.new(MASTER_KEY)
    decrypted = secret.decrypt(base64.b64decode(cipher))
    result = decrypted.rstrip("\0")
    return result


def get_lsb(color):
    if(color % 2 == 0):
        return '0'
    else:
        return '1'


def get_header(string):
    results = string.split('\0', 2)
    if(len(results) != 3):
        return 0
    return results


def analyze_header(clip):
    output = []
    for frame in clip.iter_frames(dtype="uint8"):
        for pixels in frame:
            for pixel in pixels:
                for colors in pixel:
                    output.append(get_lsb(colors))
        first_frame = int(''.join(output), 2)
        filename, filesize, data = get_header(binascii.unhexlify('%x' % first_frame))
        frames_needed = ceil(float(filesize) / len(data))
        return (filename, filesize, frames_needed)


def decode(clip):
    output = []
    filename, filesize, frames_needed = analyze_header(clip)
    print(filename, filesize, frames_needed)
    for num, frame in enumerate(clip.iter_frames(dtype="uint8")):
        for pixels in frame:
            for pixel in pixels:
                for color in pixel:
                    output.append(get_lsb(color))
        if(num == frames_needed - 1):
            n = int(''.join(output), 2)
            return get_header(binascii.unhexlify('%x' % n))


def main():
    clip = mpy.VideoFileClip('output.avi')
    filename, filesize, data = decode(clip)
    print(data[:int(filesize)])
    with open(filename, 'wb') as f:
        f.write(data[:int(filesize)])


if __name__ == '__main__':
    main()
