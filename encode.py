import moviepy.editor as mpy
import os
import binascii


def get_max_size(clip):
    width, height = (clip.w, clip.h)
    max_frames = clip.fps * clip.duration
    return (width * height * 3 / 8 / 1024) * max_frames


def file_to_binary(file):
    with file as f:
        byte = f.read()
        return list(bin(int('1'+binascii.hexlify(byte), 16))[3:].zfill(8))


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
        print("Changed {} to {}".format(color, modified))
        return modified
    else:
        return color


def encode(clip, file_to_hide):
    file = open(file_to_hide, 'rb')
    file_binary = file_to_binary(file)
    filesize = os.path.getsize(file_to_hide) * 8
    frames = []
    [frames.append(frame) for frame in clip.iter_frames(dtype="uint8")]
    # This takes forever. In the sample there's 450+ frames and we go through
    # each and every pixel in each frame. There should be a better way to do it?
    for i1, frame in enumerate(frames):
        for i2, pixels in enumerate(frame):
            for i3, pixel in enumerate(pixels):
                frames[i1][i2][i3] = process_pixel(pixel, file_binary, i3 * 3, filesize)
                filesize -= 3
                if(filesize <= 0):
                    return frames


def main():
    clip = mpy.VideoFileClip('Samples/lee.webm')
    file_to_hide = 'Samples/hidethis.txt'
    frames = encode(clip, file_to_hide)
    output = mpy.ImageSequenceClip(frames, fps=clip.fps)
    output.write_videofile("output.webm", codec="libvpx", bitrate="50000k")


if __name__ == '__main__':
    main()
