import os
import subprocess
import tempfile


def convert(input_file):

    # path of input and output files
    output_file = tempfile.gettempdir()+"/output_Music_player_Custom_.wav"

    if os.path.exists(output_file):
        os.remove(output_file)
    # run FFmpeg to convert mp3 to wav
    subprocess.run(["ffmpeg", "-i", input_file, "-vn", "-acodec",
                    "pcm_s16le", "-ar", "44100", "-ac", "2", output_file])

    return output_file
