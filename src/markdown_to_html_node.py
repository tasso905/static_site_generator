from textnode import *
from extract_markdown import *
from inline_markdown import text_to_textnodes, split_nodes_delimiter
from html_node import *
from split_nodes import *


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_node_list=[]
    for block in blocks:
        det = block_to_block_type(block)
        if det == "paragraph":
            children = text_to_children(block)
            paragraph_node = HTMLNode("p", children=children)
            html_node_list.append(paragraph_node)
        elif det == "heading":
            level = 0
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break
            heading_text = block[level:].strip()
            children = text_to_children(heading_text)
            heading_node = HTMLNode(f"h{level}", children=children)
            html_node_list.append(heading_node)
        elif det == "code":
            # Remove the triple backticks from start and end
            code_text = block[3:-3].strip()
            code_node = HTMLNode("code", children=[HTMLNode(None, value=code_text)])
            #code_node = HTMLNode("code", children=[HTMLNode(None, text=code_text)])
            pre_node = HTMLNode("pre", children=[code_node])
            html_node_list.append(pre_node)
        elif det == "quote":
            # Split into lines and remove '>' from the start of each line
            lines = block.split('\n')
            quote_lines = []
            for line in lines:
                # Remove '>' and any leading/trailing whitespace
                if line.startswith('>'):
                    line = line[1:].strip()
                quote_lines.append(line)
            # Join the lines back together
            quote_text = '\n'.join(quote_lines)
            children = text_to_children(quote_text)
            quote_node = HTMLNode("blockquote", children=children)
            html_node_list.append(quote_node)
        elif det == "unordered_list":
            items = block.split('\n')  # split into lines
            list_items = []
            for item in items:
                # Remove the "* " from start of item
                item_text = item[2:].strip()  # skip "* " and remove whitespace
                # Create li node with the item text
                children = text_to_children(item_text)
                li_node = HTMLNode("li", children=children)
                list_items.append(li_node)
            
            # Create single ul node with all list items as children
            ul_node = HTMLNode("ul", children=list_items)
            html_node_list.append(ul_node)
        elif det == "ordered_list":
            items = block.split('\n')
            list_items = []
            for item in items:
                # Skip the number, period, and space (e.g., "1. ")
                item_text = item[3:].strip()  # skip "X. " and remove whitespace
                # Create li node with the item text
                children = text_to_children(item_text)
                li_node = HTMLNode("li", children=children)
                list_items.append(li_node)
            
            # Create single ol node with all list items as children
            ol_node = HTMLNode("ol", children=list_items)
            html_node_list.append(ol_node)

    parent_div = HTMLNode("div", children=html_node_list)
    return parent_div
def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("#") and not stripped_line.startswith("##"):
            return stripped_line[2:].strip()
    raise Exception("No valid header found.")
