import ffmpeg
import subprocess
import sys
import logging
logging.basicConfig(level = logging.INFO)


def flip():
    logging.info('Processing Started')
    stream = ffmpeg.input('https://proplayaidev.blob.core.windows.net/pitchai-input/countdown.mov')
    stream = ffmpeg.vflip(stream)
    stream = ffmpeg.output(stream, 'output.mp4')
    logging.info(sys.argv[1])
    logging.info('Hello World')
    ffmpeg.run(stream)
    logging.info('Finished')
    
flip()