import sys
import torch
import subprocess
import time
import wave
import json
import logging
import re
from transformers import pipeline
from transformers.pipelines.audio_utils import ffmpeg_microphone_live
from gemini import process_transcription as process_transcription
from piper.voice import PiperVoice

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("voice_assistant.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.info("Starting the script...")

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

device = "cuda:0" if torch.cuda.is_available() else "cpu"
logging.info(f"Device selected: {device}")

transcriber = pipeline(
    "automatic-speech-recognition", model="openai/whisper-base.en", device=device
)
logging.info("Pipeline initialized...")

male_voice = PiperVoice.load(config["male_model_path"])
female_voice = PiperVoice.load(config["female_model_path"])

def text_to_speech(text, use_male_voice=True):
    try:
        voice = male_voice if use_male_voice else female_voice
        output_file = "output.wav"
        with wave.open(output_file, "wb") as wav_file:
            wav_file.setnchannels(config["channels"])
            wav_file.setsampwidth(config["sample_width"])
            wav_file.setframerate(config["sample_rate"])
            voice.synthesize(text, wav_file)
        subprocess.run(["aplay", output_file])
        logging.info(f"Successfully synthesized and played speech: {text}")
    except Exception as e:
        logging.error(f"Failed to synthesize speech: {str(e)}")

def clean_text(text):
    return re.sub(r'[^\w\s]', '', text)

def transcribe():
    try:
        sampling_rate = transcriber.feature_extractor.sampling_rate
        mic = ffmpeg_microphone_live(
            sampling_rate=sampling_rate,
            chunk_length_s=5.0,
            stream_chunk_s=1.0,
        )

        logging.info("Start speaking...") 

        for item in transcriber(mic, generate_kwargs={"max_new_tokens": 128}):
            sys.stdout.write("\033[K")
            cleaned_text = clean_text(item["text"])
            logging.info(f"Transcribed Text (Cleaned): {cleaned_text}")
            if not item["partial"][0]:
                break

        response = process_transcription(cleaned_text)
        return cleaned_text, response
    except Exception as e:
        logging.error(f"Transcription failed: {str(e)}")
        return "", "Sorry, I couldn't understand that."

if __name__ == "__main__":
    while True:
        user_choice = input("Which voice do you want to use? (male/female): ").strip().lower()
        if user_choice in ["male", "female"]:
            use_male_voice = (user_choice == "male")
            break
        else:
            logging.warning("Invalid choice. Please choose 'male' or 'female'.")

    while True:
        text, response = transcribe()

        if "switch to male voice" in text.lower():
            use_male_voice = True
            logging.info("Switched to male voice")
        elif "switch to female voice" in text.lower():
            use_male_voice = False
            logging.info("Switched to female voice")

        text_to_speech(response, use_male_voice)

        if "exit" in text.lower():
            logging.info("Exiting...")
            break
        
        time.sleep(2)
