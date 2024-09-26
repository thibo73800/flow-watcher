import os
import yaml
from flow_watcher.notion import NotionAPI

def read_notion_page():
    # Load configuration from YAML files
    with open('auth/auth.yaml', 'r') as auth_file:
        auth_config = yaml.safe_load(auth_file)

    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    # Get Notion API key and database ID from the configuration
    notion_api_key = auth_config['notion_api_key']
    notion_database_id = config['notion_database_id']

    # Initialize NotionAPI
    notion_api = NotionAPI(notion_api_key, notion_database_id)

    # Specify the page ID you want to read
    page_id = config['notion_page_id']

    # Read the page as markdown
    markdown_content = notion_api.read_page_markdown(page_id)

    print(markdown_content)

    return

    # Create a directory to store the markdown file
    os.makedirs('notion_exports', exist_ok=True)

    # Save the markdown content to a file
    output_file = os.path.join('notion_exports', f'{page_id}.md')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"Page content has been exported to {output_file}")

if __name__ == '__main__':
    read_notion_page()