# python-video-stego
Simple video stegaenograpy application written in Python

Requirements
============
Python version 2.6+
MoviePy (http://zulko.github.io/moviepy/)

> Can be installed with `pip install MoviePy`


Usage:
========
Encode

    usage: Python video stego [-h] video hide

    positional arguments:
      video       Video file to hide in
      hide        File to be hidden within

    optional arguments:
      -h, --help  Show help message


Decode:
    usage: Python video stego [-h] video

    positional arguments:
      video       Video file to hide in

    optional arguments:
      -h, --help  Show help message


Limitations
===========
Currently only outputs lossless .avi files of ridiclous size.
