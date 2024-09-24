import os
import yaml
from flow_watcher.drive import GoogleDriveHandler
import io


def list_and_downoad():
    # Load configuration from YAML files
    with open('auth/auth.yaml', 'r') as auth_file:
        auth_config = yaml.safe_load(auth_file)

    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    # Get credentials and folder ID from the configuration
    credentials_path = os.path.join('auth', auth_config['drive'])
    folder_id = config['drive_folder']

    drive_handler = GoogleDriveHandler(credentials_path)
    files = drive_handler.list_files_in_folder(folder_id)
    
    if files:
        first_file = files[0]
        output_path = os.path.join('downloads', first_file['name'])
        os.makedirs('downloads', exist_ok=True)

        # Check if the file already exists before downloading
        if os.path.exists(output_path):
            print(f"File '{first_file['name']}' already exists. Skipping download.")
        else:
            print(f"Downloading: {first_file['name']}")
            drive_handler.download_file(first_file['id'], output_path)
    else:
        print("No files found in the specified folder.")

if __name__ == '__main__':
    list_and_downoad()


