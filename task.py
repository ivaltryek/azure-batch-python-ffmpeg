import ffmpeg
import subprocess
import sys

def flip():
    print('Processing Started')
    stream = ffmpeg.input('https://proplayaidev.blob.core.windows.net/pitchai-input/02B5CEE6-678C-40FC-9874-A99D8A42B522_b1b4e34b-3830-4e75-9ed5-0abd04898a50.mov')
    stream = ffmpeg.vflip(stream)
    stream = ffmpeg.output(stream, 'output.mp4')
    subprocess.call(f'echo {sys.argv[1]}')
    print('Hello World')
    subprocess.call(['ls', '-la'])
    ffmpeg.run(stream)
    print('Finished')
    
flip()