import unittest
from markdown_to_html_node import extract_title

class TestMarkdownParser(unittest.TestCase):
    def test_extract_title(self):
        # Test a basic case
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")