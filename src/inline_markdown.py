from textnode import *
from extract_markdown import extract_markdown_links, extract_markdown_images


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

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    #print(f"Processing delimiter: {delimiter}")
    new_nodes = []
    for old_node in old_nodes:
        #print(f"Node text: {old_node.text}")
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        #print(f"Sections after split: {sections}")
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes