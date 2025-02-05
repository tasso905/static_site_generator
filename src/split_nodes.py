from textnode import *
from extract_markdown import *
from inline_markdown import text_to_textnodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        # Split block into lines, strip each line, and rejoin
        lines = [line.strip() for line in block.split("\n")]
        cleaned = "\n".join(lines)
        if cleaned:  # if block is not empty
            cleaned_blocks.append(cleaned)
    return cleaned_blocks

def block_to_block_type(text):
    heading_count = 0
    for char in text:
        if char == '#':
            heading_count += 1
        else:
            break
    if 1 <= heading_count <= 6 and len(text) > heading_count and text[heading_count] == ' ':
        return 'heading'
    if text.startswith("```") and text.endswith("```"):
        return 'code'
    blocks = text.split("\n")
    if all(block.startswith(">") for block in blocks):
        return 'quote'
    if all(block.startswith("* ") or block.startswith("- ") for block in blocks):
        return 'unordered_list'
    if all(block.startswith(f"{i}. ") for i, block in enumerate(blocks, start=1)):
        return 'ordered_list'
    return 'paragraph'

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return html_nodes



