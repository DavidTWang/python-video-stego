import subprocess as sp
import numpy
import moviepy.editor as mpy
from pyimage import *
from pyutils import *

def main():
    bruce_lee = mpy.VideoFileClip('Samples/lee.webm')
    for frame in bruce_lee.iter_frames(dtype="uint8"):
        pass

if __name__ == '__main__':
    main()
