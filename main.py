import openai
from gtts import gTTS
import os

# Set your OpenAI API key
client = openai.OpenAI(api_key='KEY')

# Function to list available models
def list_models():
    models = client.models.list()
    for model in models:
        print(model.id)

# Function to transcribe audio using OpenAI Whisper API
def transcribe_audio(file_path):
    with open(file_path, 'rb') as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return response.text

# Function to convert text to speech using gTTS
def text_to_speech(text, output_file):
    tts = gTTS(text)
    tts.save(output_file)

# Main function
def main():
    print("Available models:")
    list_models()
    return

    audio_file_path = 'downloads/Recording 162643-053024.mp3'
    transcribed_text = transcribe_audio(audio_file_path)
    print("\nTranscribed Text:", transcribed_text)
    
    output_speech_file = 'output_speech.mp3'
    text_to_speech(transcribed_text, output_speech_file)
    print(f"Speech saved to {output_speech_file}")

if __name__ == "__main__":
    main()