# The AI Agent Watcher

# ⚠️ **Warning:** This project is under heavy development and may be unstable.

## Description

A Python-based application that monitors a specific folder in Google Drive for real-time changes. This watcher will notify you of any additions, deletions, or modifications within the designated folder.

## Prerequisites

- **Python 3.7 or higher** installed on your machine.
- A **Google account** with access to Google Drive.
- **Google Cloud Project** with Google Drive API enabled.
- A **Notion account** with access to the Notion API.

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

For detailed instructions on setting up the Google Drive API, please refer to the [Google Drive Setup Documentation](docs/GOOGLE_DRIVE_SETUP.md).

## Setup Notion API

For detailed instructions on setting up the Notion API, please refer to the [Notion Setup Documentation](NOTION_SETUP.md).

## Configuration

1. **Specify the Folder to Watch**

   - Create a `config.yaml` file in the root of the project.   
   - Obtain the **Folder ID** of the Google Drive folder you want to monitor. This can be extracted from the folder's URL.
   - Add the following content to the `config.yaml` file:

   ```yaml
   drive_folder: YOUR_FOLDER_ID
   ```

2. **Specify Notion Configuration**

   - Create a `notion.yaml` file in the root of the project.
   - Add the following content to the `notion.yaml` file:

   ```yaml
   notion_token: YOUR_INTEGRATION_TOKEN
   database_id: YOUR_DATABASE_ID
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