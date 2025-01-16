import sys
import magic
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
        self.model = model


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

            


        #-Except block to handle exceptions-#
        except:
            traceback.print_exc()


def convert_audio_to_desired_format(input_audio_file, output_audio_file="output.wav"):

    try:
        # Load the audio file
        audio: AudioSegment = AudioSegment.from_file(input_audio_file)

        # Check if the file is already in the desired format
        if audio.frame_rate == 16000 and audio.channels == 1 and "wav" in magic.from_file(input_audio_file, mime = True):
            print("Audio file is already in the desired format. No conversion needed.")
            return input_audio_file

        # Set desired properties
        audio = audio.set_frame_rate(16000).set_channels(1)

        # Export to the desired format
        audio.export(output_audio_file, format="wav")
        print(f"Audio converted and saved as: {output_audio_file}")
        return output_audio_file
    except Exception as e:
        print(f"Error during audio conversion: {e}")
        return None


def transcribe_with_whisper(audio_file):

    try:
        # Load the Whisper model
        model = whisper.load_model("small.en", device="cpu")
        
        # Transcribe the audio file
        result = model.transcribe(audio_file, fp16 = False)
        
        # Get the transcribed text
        transcription = result["text"]
        
        print("Transcription completed with Whisper:")
        print(transcription)
        return transcription
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None


mime = magic.from_file("Test.mkv", mime = True)
print(mime)
mime = magic.from_file("Test.mp4", mime = True)
print(mime)
mime = magic.from_file("Test.wav", mime = True)
print(mime)

# convert_audio_to_desired_format("Test.wav")
extract_audio_from_video("Test.mp4")
# transcribe_with_whisper("Test.wav")
