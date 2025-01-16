import magic
import torch
import whisper
from pydub import AudioSegment


def extract_audio_from_video(video_file, output_audio_file="output.wav"):
    """
    Extracts audio from a video file and saves it in the desired format (WAV, 16 kHz, mono).
    
    Args:
        video_file (str): Path to the input video file.
        output_audio_file (str): Path to save the extracted audio file (default: "output.wav").
    
    Returns:
        str: Path to the extracted audio file.
    """
    try:
        # Load the audio from the video file
        audio = AudioSegment.from_file(video_file)
        
        # Set desired properties
        audio = audio.set_frame_rate(16000).set_channels(1)
        
        # Export to the desired format
        audio.export(output_audio_file, format="wav")
        print(f"Audio extracted and saved as: {output_audio_file}")
        return output_audio_file
    except Exception as e:
        print(f"Error during audio extraction: {e}")
        return None


def convert_audio_to_desired_format(input_audio_file, output_audio_file="output.wav"):
    """
    Converts an audio file to the desired format (WAV, 16 kHz, mono) 
    if it is not already in the desired format.
    
    Args:
        input_audio_file (str): Path to the input audio file.
        output_audio_file (str): Path to save the converted audio file (default: "output.wav").
    
    Returns:
        str: Path to the converted audio file or the input file if no conversion was needed.
    """
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
    """
    Transcribes audio to text using OpenAI's Whisper API.

    Args:
        audio_file (str): Path to the audio file.

    Returns:
        str: Transcribed text.
    """
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

# extract_audio_from_video("Test.mp4")
# convert_audio_to_desired_format("Test.wav")
transcribe_with_whisper("Test.wav")
