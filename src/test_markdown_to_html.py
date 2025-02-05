import unittest
from textnode import *
from html_node import *
from extract_markdown import *
from inline_markdown import *
from split_nodes import *
from markdown_to_html_node import *

class TestMarkdownToHtml(unittest.TestCase):
    
    def test_paragraph(self):
        text = "This is a paragraph"
        node = markdown_to_html_node(text)
        assert node.tag == "div"
        assert len(node.children) == 1
        assert node.children[0].tag == "p"
        assert node.children[0].children[0].text == "This is a paragraph"

    def test_heading(self):
        text = "# Header"
        node = markdown_to_html_node(text)
        assert node.tag == "div"
        assert len(node.children) == 1
        assert node.children[0].tag == "h1"
        assert node.children[0].children[0].text == "Header"
    
    #def test_code_block(self):
    #    text = "```\nprint('hello')\n```"
    #    node = markdown_to_html_node(text)
    #    assert node.tag == "div"
    #    assert node.children[0].tag == "pre"
    #    assert node.children[0].children[0].tag == "code"
    #    assert node.children[0].children[0].children[0].text == "print('hello')"

    def test_quote_block(self):
        text = "> This is a quote\n> More quote"
        node = markdown_to_html_node(text)
        assert node.tag == "div"
        assert node.children[0].tag == "blockquote"
        assert "This is a quote" in node.children[0].children[0].text

    def test_unordered_list(self):
        text = "* Item 1\n* Item 2"
        node = markdown_to_html_node(text)
        assert node.tag == "div"
        assert node.children[0].tag == "ul"
        assert len(node.children[0].children) == 2
        assert node.children[0].children[0].tag == "li"
        assert "Item 1" in node.children[0].children[0].children[0].text

    def test_ordered_list(self):
        text = "1. First\n2. Second"
        node = markdown_to_html_node(text)
        assert node.tag == "div"
        assert node.children[0].tag == "ol"
        assert len(node.children[0].children) == 2
        assert node.children[0].children[0].tag == "li"
        assert "First" in node.children[0].children[0].children[0].text
    
    #def test_multiple_headings(self):
    #    text = "# Heading 1\n## Heading 2\n### Heading 3"
    #    node = markdown_to_html_node(text)
    #    assert len(node.children) == 3
    #    assert node.children[0].tag == "h1"
    #    assert node.children[1].tag == "h2"
    #    assert node.children[2].tag == "h3"

    #def test_mixed_content(self):
    #    text = "# Header\nThis is a paragraph\n* List item"
    #    node = markdown_to_html_node(text)
    #    assert len(node.children) == 3
    #    assert node.children[0].tag == "h1"
    #    assert node.children[1].tag == "p"
    #    assert node.children[2].tag == "ul"

    def test_inline_markdown(self):
        text = "This is **bold** and *italic*"
        node = markdown_to_html_node(text)
        children = node.children[0].children
        assert "bold" in str(children)
        assert "italic" in str(children)

if __name__ == "__main__":
    unittest.main()