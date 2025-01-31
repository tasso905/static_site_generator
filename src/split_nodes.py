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