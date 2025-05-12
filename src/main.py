from textnode import TextNode, TextType
from html_node import HTMLNode, LeafNode, ParentNode
from split_nodes import *
import os
import shutil
from markdown_to_html_node import extract_title, markdown_to_html_node


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Scanning directory: {dir_path_content}")  # Add this debug line
     # First, we need to get the list of items in the directory
    for item in os.listdir(dir_path_content):
        # Create full paths for source and destination
        src_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        print(f"Found item: {src_path}")  # Add this debug line
        if os.path.isfile(src_path):
            if src_path.endswith(".md"):
                with open(src_path, 'r') as file:
                    markdown = file.read()
                html_node = markdown_to_html_node(markdown)
                dest_path = dest_path.replace('.md', '.html')
                generate_page(src_path, template_path, dest_path)
        else:
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(src_path, template_path, dest_path)

def copy_recursive(src_dir, dest_dir):

    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
        os.mkdir(dest_dir)

    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
            print(f"Copied file: {dest_path}")
        elif os.path.isdir(src_path):
            os.mkdir(dest_path)
            print(f"Created directory: {dest_path}")
            # Recurse into the subdirectory
            copy_recursive(src_path, dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as file:
        content_from = file.read()
    title = extract_title(content_from)
    with open(template_path, 'r') as file:
        content_template = file.read()
    html_node = markdown_to_html_node(content_from)
    html_content = html_node.to_html()
    final_html = content_template.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(final_html)

def main():
    # Define directory paths
    dest_dir = "public"

    # Delete and recreate public directory
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)

    # Copy static files
    copy_recursive("static", dest_dir)

    # Generate pages recursively
    generate_pages_recursive(
        "content",       # directory containing markdown files
        "template.html", # template file path
        "public"        # output directory
    )

if __name__ == "__main__":
    main()
