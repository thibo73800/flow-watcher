# Google Drive Setup

## Create a Google Cloud Project

1. Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click on the project dropdown and select **New Project**.
3. Enter a project name and click **Create**.

## Enable Google Drive API

1. In the [APIs & Services Dashboard](https://console.cloud.google.com/apis/dashboard), click **Enable APIs and Services**.
2. Search for "Google Drive API" and select it.
3. Click **Enable**.

## Create OAuth Credentials

1. Go to **APIs & Services** > **Credentials**.
2. Click **Create Credentials** > **OAuth client ID**.
3. Select **Desktop app** and provide a name.
4. Click **Create** and download the `credentials.json` file.
5. Create a `auth` folder in the root of the project.
6. Place the `credentials.json` file in the `auth` folder.
7. Create a `auth.yaml` file in the `auth` folder.
8. Add the following content to the `auth.yaml` file:

   ```yaml
   drive: FILE_NAME
   ```