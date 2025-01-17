import os
import sys
import magic
import torch
import whisper
import traceback
from pathlib import Path


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
        self.current_dir = Path(__file__).parent
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
            processed_filepath = self.__prepare_input(filepath).__str__()
            print(processed_filepath)
            raise Exception

            #-Creating the transcription filepath-#
            output_filepath = self.current_dir / f"{Path(filepath).stem}_transcription.txt"

            #-Transcribing the audio file-#
            result = self.model.transcribe(processed_filepath, fp16 = False, verbose = True)

            #-Writing the transcription to a file-#
            with open(output_filepath, "w", encoding = "utf-8") as file:
                file.write(result["text"])

            print(f"Transcription saved in [{output_filepath}] successfully.")

        #-Except block to handle exceptions-#
        except:
            traceback.print_exc()

        #-Some cleanup code-#
        finally:

            #-Removing temp temporary audio file if created-#
            if Path.exists(processed_filepath):
                os.remove(processed_filepath)


speech_scribe = SpeechScribe()
speech_scribe.transcribe("Test.ts")
