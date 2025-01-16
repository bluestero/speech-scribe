import os
import sys
import magic
import torch
import whisper
import traceback
from pathlib import Path
from pydub import AudioSegment

#-Custom imports-#
sys.path.insert(0, Path(__file__).parent)
import utils


#-Class object for Invalid input file exception-#
class InvalidInputFile(Exception):
    def __init__(self, msg):
        super().__init__(msg)


#-Main class for the SpeechScribe-#
class SpeechScribe:

    #-Init function for base initializations-#
    def __init__(self, model: str = "small.en"):

        #-Base objects-#
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = whisper.load_model(model, device = device)


    #-Function to prepare the input file-#
    def __prepare_input(self, filepath: str) -> None:

        #-Getting the mime-type of the input file-#
        mime = magic.from_file(filepath, mime = True)

        #-Extracting the audio if the mime-type of the file contains audio / video-#
        if "audio" in mime or "video" in mime:
            return utils.get_audio(filepath)

        #-Else raising InvalidInputFile exception-#
        else:
            raise InvalidInputFile(f"The file [{filepath}] is not a valid audio / video file.")


    #-Function to transcribe the audio file-#
    def transcribe(self, filepath: str) -> bool:

        #-Try block to handle exceptions-#
        try:

            #-Processing the input file and getting the updated filepath-#
            filepath = self.__prepare_input(filepath)

            #-Creating the transcription filepath-#
            transcribed_path = f"{Path(filepath).stem}_transcription.txt"

            #-Transcribing the audio file-#
            result = self.model.transcribe(filepath, fp16 = False)

            #-Writing the transcription to a file-#
            with open(transcribed_path, "w", encoding = "utf-8") as file:
                file.write(result["text"])

            print(f"Transcription saved in [{transcribed_path}] successfully.")

        #-Except block to handle exceptions-#
        except:
            traceback.print_exc()

        #-Some cleanup code-#
        finally:

            #-Removing all the temporarily created audio files-#
            [os.remove(file) for file in Path.cwd().glob("temp_*")]
