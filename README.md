# Google Drive Folder Watcher

# ⚠️ **Warning:** This project is under heavy development and may be unstable.

## Description

A Python-based application that monitors a specific folder in Google Drive for real-time changes. This watcher will notify you of any additions, deletions, or modifications within the designated folder.

## Prerequisites

- **Python 3.7 or higher** installed on your machine.
- A **Google account** with access to Google Drive.
- **Google Cloud Project** with Google Drive API enabled.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/thibo73800/flow-watcher.git
   cd flow-watcher
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Python Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Setup Google Drive API

1. **Create a Google Cloud Project**

   - Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
   - Click on the project dropdown and select **New Project**.
   - Enter a project name and click **Create**.

2. **Enable Google Drive API**

   - In the [APIs & Services Dashboard](https://console.cloud.google.com/apis/dashboard), click **Enable APIs and Services**.
   - Search for "Google Drive API" and select it.
   - Click **Enable**.

3. **Create OAuth Credentials**

   - Go to **APIs & Services** > **Credentials**.
   - Click **Create Credentials** > **OAuth client ID**.
   - Select **Desktop app** and provide a name.
   - Click **Create** and download the `credentials.json` file.
   - Create a `auth` folder in the root of the project.
   - Place the `credentials.json` file in the `auth` folder.
   - Create a `auth.yaml` file in the `auth` folder.
   - Add the following content to the `auth.yaml` file:

   ```yaml
   drive: FILE_NAME
   ```

## Configuration

1. **Specify the Folder to Watch**

   - Create a `config.yaml` file in the root of the project.   
   - Obtain the **Folder ID** of the Google Drive folder you want to monitor. This can be extracted from the folder's URL.
   - Add the following content to the `config.yaml` file:

   ```yaml
   drive_folder: YOUR_FOLDER_ID
   ```

## Usage

1. **Run the Watcher**

   ```bash
   python watcher.py
   ```

2. **Authorize Access**

   - On the first run, a browser window will prompt you to authorize the application to access your Google Drive.
   - Follow the on-screen instructions to grant permissions.

3. **Monitor Folder Changes**

   - The application will start monitoring the specified folder.
   - Changes such as file additions, deletions, or updates will be logged in the console.

## Troubleshooting

- **Authentication Errors**: Ensure that the `credentials.json` file is correctly placed in the project root and that you've authorized the application.
- **API Quotas**: Be mindful of Google Drive API usage limits. Monitor your usage in the Google Cloud Console to avoid exceeding quotas.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

[MIT License](LICENSE)