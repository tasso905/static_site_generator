import unittest
from extractmarkdown import *

class TestExtractMarkdownImages(unittest.TestCase):

    def test_no_images(self):
        text = "This text has no images!"
        self.assertEqual(extract_markdown_images(text), [])

    def test_single_image(self):
        text = "Here is an image: ![dog](https://dog.jpg)"
        self.assertEqual(extract_markdown_images(text), [("dog", "https://dog.jpg")])

    def test_multiple_images(self):
        text = "![alt1](http://example1.com) and ![alt2](http://example2.com)"
        self.assertEqual(extract_markdown_images(text), [("alt1", "http://example1.com"), ("alt2", "http://example2.com")])

    def test_malformed_image_syntax(self):
        text = "Here is a broken image: [dog](https://dog.jpg)"
        self.assertEqual(extract_markdown_images(text), [])

class TestExtractMarkdownLinks(unittest.TestCase):

    def test_no_links(self):
        text = "This text has no links!"
        self.assertEqual(extract_markdown_links(text), [])

    def test_single_link(self):
        text = "Here is a [link](https://example.com)."
        self.assertEqual(extract_markdown_links(text), [("link", "https://example.com")])

    def test_multiple_links(self):
        text = "[Boot.dev](https://www.boot.dev) is cool, so is [Python](https://python.org)."
        self.assertEqual(extract_markdown_links(text), [("Boot.dev", "https://www.boot.dev"), ("Python", "https://python.org")])

if __name__ == "__main__":
    unittest.main()