import moviepy.editor as mpy

def main():
    bruce_lee = mpy.VideoFileClip("lee.webm")
    bruce_lee.save_frame("first_frame.png")
    print("Done")


if __name__ == '__main__':
    main()
