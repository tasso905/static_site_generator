from textnode import *
from extract_markdown import *
from inline_markdown import *

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            result.append(node)
        else:
            for link_text, link_url in links:
                markdown_link = f"[{link_text}]({link_url})"
                parts = node.text.split(markdown_link, 1)                
                if parts[0]:
                    result.append(TextNode(parts[0], TextType.TEXT))
                
                result.append(TextNode(link_text, TextType.LINK, link_url))
                
                if parts[1]:
                    result.append(TextNode(parts[1], TextType.TEXT))

    return result

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if not images:
            result.append(node)
        else:
            for alt_text, image_url in images:
                markdown_image = f"![{alt_text}]({image_url})"
                parts = node.text.split(markdown_image, 1)
                
                # Don't forget: we only want to append nodes if they have text!
                if parts[0]:
                    result.append(TextNode(parts[0], TextType.TEXT))
                
                result.append(TextNode(alt_text, TextType.IMAGE, image_url))
                
                if parts[1]:
                    result.append(TextNode(parts[1], TextType.TEXT))

    return result
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

