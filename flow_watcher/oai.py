import openai
from typing import List

class OAI:
    """
    A class to interact with the OpenAI API for various functionalities such as listing models and transcribing audio.
    """

    def __init__(self, api_key: str) -> None:
        """
        Initialize the OAI class with an API key.

        Parameters
        ----------
        api_key : str
            The API key to authenticate with the OpenAI API.
        """
        self.client = openai.OpenAI(api_key=api_key)

    def list_models(self) -> None:
        """
        List all available models from the OpenAI API and print their IDs.

        This method fetches the list of models from the OpenAI API and prints the ID of each model.
        """
        models: List[openai.Model] = self.client.models.list()
        for model in models:
            print(model.id)

    def transcribe_audio(self, file_path: str) -> str:
        """
        Transcribe an audio file using the OpenAI API.

        This method reads an audio file and sends it to the OpenAI API for transcription using the 'whisper-1' model.

        Parameters
        ----------
        file_path : str
            The path to the audio file to be transcribed.

        Returns
        -------
        str
            The transcribed text from the audio file.
        """
        with open(file_path, 'rb') as audio_file:
            response: openai.AudioTranscription = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return response.text