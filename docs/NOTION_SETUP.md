# Notion Setup

## Create a Notion Integration

1. Navigate to the [Notion Integrations](https://www.notion.so/my-integrations) page.
2. Click on **New Integration**.
3. Enter a name for your integration and select the workspace where you want to use it.
4. Click **Submit** to create the integration.
5. Copy the **Internal Integration Token**. You will need this token to authenticate your application with Notion.

## Share a Database with Your Integration

1. Open the Notion page or database you want to integrate with.
2. Click on the **Share** button at the top-right corner of the page.
3. In the **Invite** field, search for the name of your integration and select it.
4. Click **Invite** to share the page or database with your integration.

## Configuration

1. **Create a `notion.yaml` file**

   - In the root of your project, create a `notion.yaml` file.
   - Add the following content to the `notion.yaml` file:

   ```yaml
   notion_token: YOUR_INTEGRATION_TOKEN
   database_id: YOUR_DATABASE_ID
   ```

   Replace `YOUR_INTEGRATION_TOKEN` with the Internal Integration Token you copied earlier, and `YOUR_DATABASE_ID` with the ID of the Notion database you want to interact with.

## Usage

1. **Install Notion SDK**

   Ensure you have the Notion SDK installed. You can add it to your `requirements.txt` or install it directly using pip:

   ```bash
   pip install notion-client
   ```

2. **Access Notion API in Your Code**

   Use the Notion SDK to interact with your Notion database. Here is a basic example in Python:

   ```python
   from notion_client import Client
   import yaml

   # Load Notion configuration
   with open('notion.yaml', 'r') as file:
       config = yaml.safe_load(file)

   notion = Client(auth=config['notion_token'])

   # Example: Retrieve a database
   database_id = config['database_id']
   response = notion.databases.retrieve(database_id=database_id)
   print(response)
   ```

## Troubleshooting

- **Authentication Errors**: Ensure that the `notion_token` in your `notion.yaml` file is correct and that your integration has access to the database.
- **API Limits**: Be aware of Notion API rate limits. Refer to the [Notion API documentation](https://developers.notion.com/docs/rate-limits) for more details.

## Additional Resources

- [Notion API Documentation](https://developers.notion.com/)
- [Notion SDK for Python](https://github.com/ramnes/notion-sdk-py)
