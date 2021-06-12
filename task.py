import ffmpeg
import subprocess
import sys

def flip():
    stream = ffmpeg.input('countdown.mov')
    stream = ffmpeg.vflip(stream)
    stream = ffmpeg.output(stream, 'output.mp4')
    subprocess.call(f'echo {sys.argv[1]}')
    ffmpeg.run(stream)