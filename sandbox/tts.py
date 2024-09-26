import openai
import os
import yaml

from flow_watcher import oai

# Load configuration from config.yaml
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Main function
def main():
    model = oai.OAI(api_key=config['oai_key'])
    audio_file_path = 'downloads/Recording 162643-053024.mp3'
    transcribed_text = model.transcribe_audio(audio_file_path)
    print("\nTranscribed Text:", transcribed_text)

if __name__ == "__main__":
    main()