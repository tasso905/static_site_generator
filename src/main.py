from textnode import TextNode, TextType
from html_node import HTMLNode, LeafNode, ParentNode
from split_nodes import *
import os
import shutil

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

def main():

    # Define source and destination directory paths
    src_dir = "static"
    dest_dir = "public"

    # Call your recursive function to copy contents
    copy_recursive(src_dir, dest_dir)


    text_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(text_node)
    html_node  = HTMLNode(tag="p", value="Hello", props={"class": "greeting"})
    print(html_node)
    parent_node = ParentNode(tag="p", children="Hello", props={"class": "greeting"})
    print(parent_node)
    print(block_to_block_type("# Valid heading"))  # should return 'heading'
    print(block_to_block_type("#Invalid heading"))  # should return 'paragraph' (no space after #)
    print(block_to_block_type("####### Too many"))  # should return 'paragraph'
    print(block_to_block_type("```\nsome code\n```"))  # should return 'code'
    print(block_to_block_type("```not closed"))  # should return 'paragraph'
    print(block_to_block_type("1. First\n2. Second"))  # should return 'ordered_list'
    print(block_to_block_type("1. First\n3. Third"))  # should return 'paragraph' (missing 2)


if __name__ == "__main__":
    main()