import os
import yaml
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
from typing import List, Optional, Dict

from flow_watcher.utils import print_progress_bar


class GoogleDriveHandler:
    """
    A handler class for interacting with Google Drive API.
    """
    # Define the scope for Google Drive API access
    SCOPES: List[str] = ['https://www.googleapis.com/auth/drive.readonly']

    def __init__(self, credentials_path: str):
        """
        Initialize the GoogleDriveHandler with the path to the credentials file.

        Parameters
        ----------
        credentials_path : str
            Path to the credentials JSON file.
        """
        self.credentials_path: str = credentials_path
        self.credentials: Credentials = self._get_credentials()
        # Build the Google Drive service object
        self.service = build('drive', 'v3', credentials=self.credentials)

    def _get_credentials(self) -> Credentials:
        """
        Obtain user credentials for accessing Google Drive.

        Returns
        -------
        Credentials
            The authenticated credentials for Google Drive API access.
        """
        creds: Optional[Credentials] = None
        # Check if token.json file exists to load existing credentials
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If no valid credentials are available, prompt the user to log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                # Refresh the credentials if they are expired
                creds.refresh(Request())
            else:
                # Run the OAuth flow to get new credentials
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def list_files_in_folder(self, folder_id: str) -> List[Dict[str, str]]:
        """
        List all files in a specified Google Drive folder.

        Parameters
        ----------
        folder_id : str
            The ID of the Google Drive folder.

        Returns
        -------
        List[Dict[str, str]]
            A list of dictionaries containing file IDs and names.
        """
        query = f"'{folder_id}' in parents"
        # Execute the query to list files in the folder
        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        return results.get('files', [])

    def download_file(self, file_id: str, output_path: str) -> None:
        """
        Download a file from Google Drive given its file ID.

        Parameters
        ----------
        file_id : str
            The ID of the file to be downloaded.
        output_path : str
            The local path where the downloaded file will be saved.
        """
        request = self.service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done: bool = False
        print("Downloading file:")
        # Download the file in chunks and show progress
        while not done:
            status, done = downloader.next_chunk()
            print_progress_bar(int(status.progress() * 100))
        print("\nDownload complete!")
        # Write the downloaded file to the specified output path
        with open(output_path, "wb") as f:
            f.write(file.getvalue())
