import os
import subprocess


def convert(input_file):

    # path of input and output files
    output_file = "output.wav"

    if os.path.exists(output_file):
        os.remove(output_file)
    # run FFmpeg to convert mp3 to wav
    subprocess.run(["ffmpeg", "-i", input_file, "-vn", "-acodec",
                    "pcm_s16le", "-ar", "44100", "-ac", "2", output_file])

    return output_file
