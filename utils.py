import os
import shutil
import magic
from pathlib import Path
from pydub import AudioSegment


#-Function to extract or get the audio in the desired format-#
def get_audio(input_file: str, output_filepath: str = None):

    #-Loading the audio file-#
    audio: AudioSegment = AudioSegment.from_file(input_file)

    #-Creating output filepath if not given-#
    if not output_filepath:
        output_filepath = Path.cwd() / f"temp_{Path(input_file).stem}.wav"

    #-Checking if the file is already in the desired format-#
    if audio.frame_rate == 16000 and audio.channels == 1 and "wav" in magic.from_file(input_file, mime = True):
        print("Audio already in the desired format. Creating a temp copy of it.")

        #-Removing the file if exists already-#
        if Path.exists(output_filepath):
            os.remove(output_filepath)

        #-Creating a copy of the file-#
        shutil.copy(input_file, output_filepath)

        #-Returning the input path-#
        return output_filepath

    #-Setting the desired sample rate-#
    audio = audio.set_frame_rate(16000).set_channels(1)

    #-Exporting the file to the output filepath-#
    audio.export(output_filepath, format = "wav")
    print(f"Audio extracted and saved as: {output_filepath}.")

    #-Returning the output filepath-#
    return output_filepath
