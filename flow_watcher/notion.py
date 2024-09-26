import requests
from typing import Any, Dict, Optional, List, Set
import json

class NotionAPI:
    """
    A class to interact with the Notion API.
    
    Attributes
    ----------
    api_key : str
        The API key for authenticating with the Notion API.
    database_id : str
        The ID of the Notion database to interact with.
    base_url : str
        The base URL for the Notion API.
    headers : Dict[str, str]
        The headers to include in API requests.
    """
    def __init__(self, api_key: str, database_id: str) -> None:
        """
        Initialize the NotionAPI class with the provided API key and database ID.
        
        Parameters
        ----------
        api_key : str
            The API key for authenticating with the Notion API.
        database_id : str
            The ID of the Notion database to interact with.
        """
        self.api_key = api_key
        self.database_id = database_id
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def retrieve_database_entry(self, entry_id: str) -> Dict[str, Any]:
        """
        Retrieve a specific entry from the Notion database.
        
        Parameters
        ----------
        entry_id : str
            The ID of the entry to retrieve.
        
        Returns
        -------
        Dict[str, Any]
            The JSON response from the Notion API containing the entry details.
        """
        url = f"{self.base_url}/pages/{entry_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def write_new_page(self, title: str, content: str) -> Dict[str, Any]:
        """
        Create a new page in the Notion database with the given title and content.
        
        Parameters
        ----------
        title : str
            The title of the new page.
        content : str
            The content of the new page.
        
        Returns
        -------
        Dict[str, Any]
            The JSON response from the Notion API containing the new page details.
        """
        url = f"{self.base_url}/pages"
        data = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "title": {
                    "title": [{"text": {"content": title}}]
                }
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": content}}]
                    }
                }
            ]
        }
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def read_page_markdown(self, page_id: str) -> str:
        """
        Retrieve the content of a Notion page and convert it to Markdown.
        
        Parameters
        ----------
        page_id : str
            The ID of the page to retrieve.
        
        Returns
        -------
        str
            The content of the page in Markdown format.
        """
        processed_pages: Set[str] = set()
        markdown_content = self._fetch_page_content_recursive(page_id, processed_pages)
        return markdown_content

    def _fetch_page_content_recursive(self, page_id: str, processed_pages: Set[str]) -> str:
        """
        Recursively fetch the content of a Notion page and its children.
        
        Parameters
        ----------
        page_id : str
            The ID of the page to retrieve.
        processed_pages : Set[str]
            A set of page IDs that have already been processed to avoid recursion.
        
        Returns
        -------
        str
            The content of the page and its children in Markdown format.
        """
        if page_id in processed_pages:
            print(f"Page {page_id} already processed. Skipping to avoid recursion.")
            return ""
        processed_pages.add(page_id)

        url = f"{self.base_url}/blocks/{page_id}/children"
        response = requests.get(url, headers=self.headers)
        
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            print(f"Response content: {response.content}")
            return ""
        
        blocks = response.json().get('results', [])
        markdown_content = self._convert_blocks_to_markdown(blocks, processed_pages)
        return markdown_content

    def _convert_blocks_to_markdown(self, blocks: List[Dict[str, Any]], processed_pages: Set[str]) -> str:
        """
        Convert Notion blocks to Markdown formatted text.
        
        Parameters
        ----------
        blocks : List[Dict[str, Any]]
            A list of Notion blocks to convert.
        processed_pages : Set[str]
            A set of page IDs that have already been processed to avoid recursion.
        
        Returns
        -------
        str
            The content of the blocks in Markdown format.
        """
        markdown_lines = []
        for block in blocks:
            block_type = block.get('type')
            if not block_type:
                continue

            content = ""
            if block_type == 'paragraph':
                content = self._handle_paragraph(block['paragraph'])
            elif block_type == 'heading_1':
                content = self._handle_heading(block['heading_1'], level=1)
            elif block_type == 'heading_2':
                content = self._handle_heading(block['heading_2'], level=2)
            elif block_type == 'heading_3':
                content = self._handle_heading(block['heading_3'], level=3)
            elif block_type == 'bulleted_list_item':
                content = self._handle_bulleted_list_item(block['bulleted_list_item'])
            elif block_type == 'numbered_list_item':
                content = self._handle_numbered_list_item(block['numbered_list_item'])
            elif block_type == 'to_do':
                content = self._handle_to_do(block['to_do'])
            elif block_type == 'toggle':
                content = self._handle_toggle(block['toggle'], processed_pages)
            elif block_type == 'code':
                content = self._handle_code(block['code'])
            elif block_type == 'quote':
                content = self._handle_quote(block['quote'])
            elif block_type == 'divider':
                content = self._handle_divider()
            elif block_type == 'child_page':
                child_page = block.get('child_page', {})
                child_page_id = child_page.get('page_id')  # Updated from 'id' to 'page_id'
                child_page_title = child_page.get('title', 'Untitled Page')
                if child_page_id:
                    child_markdown = self._fetch_page_content_recursive(child_page_id, processed_pages)
                    content = f"\n### {child_page_title}\n\n{child_markdown}\n"
                else:
                    print(f"Child page ID not found in block: {block}")
            else:
                print(f"Unhandled block type: {block_type}")
                continue

            if content:
                markdown_lines.append(content)

        return "\n\n".join(markdown_lines)

    def _handle_paragraph(self, paragraph: Dict[str, Any]) -> str:
        """
        Handle paragraph blocks and convert them to Markdown.
        
        Parameters
        ----------
        paragraph : Dict[str, Any]
            The paragraph block to handle.
        
        Returns
        -------
        str
            The content of the paragraph in Markdown format.
        """
        texts = paragraph.get('rich_text', [])
        return self._compose_text(texts)

    def _handle_heading(self, heading: Dict[str, Any], level: int) -> str:
        """
        Handle heading blocks and convert them to Markdown.
        
        Parameters
        ----------
        heading : Dict[str, Any]
            The heading block to handle.
        level : int
            The level of the heading (1, 2, or 3).
        
        Returns
        -------
        str
            The content of the heading in Markdown format.
        """
        texts = heading.get('rich_text', [])
        prefix = '#' * level
        return f"{prefix} {self._compose_text(texts)}"

    def _handle_bulleted_list_item(self, list_item: Dict[str, Any]) -> str:
        """
        Handle bulleted list item blocks and convert them to Markdown.
        
        Parameters
        ----------
        list_item : Dict[str, Any]
            The bulleted list item block to handle.
        
        Returns
        -------
        str
            The content of the bulleted list item in Markdown format.
        """
        texts = list_item.get('rich_text', [])
        return f"- {self._compose_text(texts)}"

    def _handle_numbered_list_item(self, list_item: Dict[str, Any]) -> str:
        """
        Handle numbered list item blocks and convert them to Markdown.
        
        Parameters
        ----------
        list_item : Dict[str, Any]
            The numbered list item block to handle.
        
        Returns
        -------
        str
            The content of the numbered list item in Markdown format.
        """
        texts = list_item.get('rich_text', [])
        return f"1. {self._compose_text(texts)}"

    def _handle_to_do(self, to_do: Dict[str, Any]) -> str:
        """
        Handle to-do blocks and convert them to Markdown.
        
        Parameters
        ----------
        to_do : Dict[str, Any]
            The to-do block to handle.
        
        Returns
        -------
        str
            The content of the to-do block in Markdown format.
        """
        texts = to_do.get('rich_text', [])
        checked = to_do.get('checked', False)
        checkbox = "[x]" if checked else "[ ]"
        return f"- {checkbox} {self._compose_text(texts)}"

    def _handle_toggle(self, toggle: Dict[str, Any], processed_pages: Set[str]) -> str:
        """
        Handle toggle blocks and convert them to Markdown.
        
        Parameters
        ----------
        toggle : Dict[str, Any]
            The toggle block to handle.
        processed_pages : Set[str]
            A set of page IDs that have already been processed to avoid recursion.
        
        Returns
        -------
        str
            The content of the toggle block in Markdown format.
        """
        texts = toggle.get('rich_text', [])
        summary = self._compose_text(texts)
        # Fetch children of the toggle block
        toggle_id = toggle.get('id')
        if toggle_id:
            url = f"{self.base_url}/blocks/{toggle_id}/children"
            response = requests.get(url, headers=self.headers)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print(f"HTTP error occurred while fetching toggle children: {e}")
                return f"> <details><summary>{summary}</summary>\n\n</details>"
            blocks = response.json().get('results', [])
            nested_markdown = self._convert_blocks_to_markdown(blocks, processed_pages)
            return f"> <details><summary>{summary}</summary>\n\n{nested_markdown}\n</details>"
        else:
            return f"> <details><summary>{summary}</summary>\n\n</details>"

    def _handle_code(self, code: Dict[str, Any]) -> str:
        """
        Handle code blocks and convert them to Markdown.
        
        Parameters
        ----------
        code : Dict[str, Any]
            The code block to handle.
        
        Returns
        -------
        str
            The content of the code block in Markdown format.
        """
        language = code.get('language', '')
        content = code.get('rich_text', [])
        code_content = self._compose_text(content)
        return f"```{language}\n{code_content}\n```"

    def _handle_quote(self, quote: Dict[str, Any]) -> str:
        """
        Handle quote blocks and convert them to Markdown.
        
        Parameters
        ----------
        quote : Dict[str, Any]
            The quote block to handle.
        
        Returns
        -------
        str
            The content of the quote block in Markdown format.
        """
        texts = quote.get('rich_text', [])
        return f"> {self._compose_text(texts)}"

    def _handle_divider(self) -> str:
        """
        Handle divider blocks and convert them to Markdown.
        
        Returns
        -------
        str
            The Markdown representation of a divider.
        """
        return "---"

    def _compose_text(self, texts: List[Dict[str, Any]]) -> str:
        """
        Compose rich text objects into a single string with Markdown formatting.
        
        Parameters
        ----------
        texts : List[Dict[str, Any]]
            A list of rich text objects to compose.
        
        Returns
        -------
        str
            The composed text in Markdown format.
        """
        composed = ""
        for text in texts:
            if text.get('type') == 'text':
                content = text['text']['content']
                annotations = text.get('annotations', {})
                content = self._apply_markdown_annotations(content, annotations)
                composed += content
            elif text.get('type') == 'mention':
                # Handle mentions if needed
                pass
            # Handle other text types as needed
        return composed

    def _apply_markdown_annotations(self, content: str, annotations: Dict[str, Any]) -> str:
        """
        Apply Markdown formatting based on text annotations.
        
        Parameters
        ----------
        content : str
            The text content to format.
        annotations : Dict[str, Any]
            The annotations to apply.
        
        Returns
        -------
        str
            The formatted text.
        """
        if annotations.get('bold'):
            content = f"**{content}**"
        if annotations.get('italic'):
            content = f"*{content}*"
        if annotations.get('underline'):
            content = f"<u>{content}</u>"
        if annotations.get('strikethrough'):
            content = f"~~{content}~~"
        if annotations.get('code'):
            content = f"`{content}`"
        return content

    def write_markdown_to_page(self, page_id: str, markdown_content: str) -> Dict[str, Any]:
        """
        Write Markdown content to a Notion page by converting it to Notion blocks.
        
        Parameters
        ----------
        page_id : str
            The ID of the page to write to.
        markdown_content : str
            The Markdown content to write.
        
        Returns
        -------
        Dict[str, Any]
            The JSON response from the Notion API containing the updated page details.
        """
        blocks = self._convert_markdown_to_blocks(markdown_content)
        url = f"{self.base_url}/blocks/{page_id}/children"
        data = {
            "children": blocks
        }
        response = requests.patch(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def _convert_markdown_to_blocks(self, markdown: str) -> List[Dict[str, Any]]:
        """
        Convert Markdown text to Notion blocks.
        
        Parameters
        ----------
        markdown : str
            The Markdown text to convert.
        
        Returns
        -------
        List[Dict[str, Any]]
            A list of Notion blocks representing the Markdown content.
        """
        lines = markdown.split('\n')
        blocks = []
        for line in lines:
            if line.startswith('### '):
                blocks.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": line[4:]}}]
                    }
                })
            elif line.startswith('## '):
                blocks.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": line[3:]}}]
                    }
                })
            elif line.startswith('# '):
                blocks.append({
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                    }
                })
            elif line.startswith('- [x] '):
                blocks.append({
                    "object": "block",
                    "type": "to_do",
                    "to_do": {
                        "text": [{"type": "text", "text": {"content": line[6:]}}],
                        "checked": True
                    }
                })
            elif line.startswith('- [ ] '):
                blocks.append({
                    "object": "block",
                    "type": "to_do",
                    "to_do": {
                        "text": [{"type": "text", "text": {"content": line[6:]}}],
                        "checked": False
                    }
                })
            elif line.startswith('- '):
                blocks.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                    }
                })
            elif line.startswith('1. '):
                blocks.append({
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": line[3:]}}]
                    }
                })
            elif line.startswith('```'):
                language = line[3:].strip()
                blocks.append({
                    "object": "block",
                    "type": "code",
                    "code": {
                        "text": [{"type": "text", "text": {"content": ""}}],
                        "language": language
                    }
                })
            elif line.startswith('---') or line.startswith('***'):
                blocks.append({
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                })
            elif line.startswith('> '):
                blocks.append({
                    "object": "block",
                    "type": "quote",
                    "quote": {
                        "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                    }
                })
            elif line.startswith('###'):
                # Handle details summary or other extended markdown syntax if needed
                blocks.append({
                    "object": "block",
                    "type": "toggle",
                    "toggle": {
                        "rich_text": [{"type": "text", "text": {"content": line}}]
                    }
                })
            else:
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": line}}]
                    }
                })
        return blocks