import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_none(self):
        node = HTMLNode(props=None)
        assert node.props_to_html() == ""

    def test_props_to_html_one_prop(self):
        node = HTMLNode(props={"href": "https://google.com"})
        assert node.props_to_html() == ' href="https://google.com"'

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
        assert node.props_to_html() == ' href="https://google.com" target="_blank"'