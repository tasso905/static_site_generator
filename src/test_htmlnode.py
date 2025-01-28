import unittest
from textnode import *
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_none(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_one_prop(self):
        node = HTMLNode(props={"href": "https://google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com" target="_blank"')

class TestLeafNode(unittest.TestCase):
    def test_tag_none(self):
        node = LeafNode(None, "Hello")
        self.assertEqual(node.to_html(), 'Hello')

    def test_no_props(self):
        node = LeafNode("p", "No props")
        self.assertEqual(node.to_html(), '<p>No props</p>')
    
    def test_empty_props(self):
        node = LeafNode("p", "Empty props", {})
        self.assertEqual(node.to_html(), '<p>Empty props</p>')

    def test_unusual_props(self):
        node = LeafNode("div", "Edge cases", {"data-info": "awesome"})
        self.assertEqual(node.to_html(), '<div data-info="awesome">Edge cases</div>')

    def test_missing_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

class TestParentNode(unittest.TestCase):
    def test_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("p", None).to_html()

    def test_tag_none(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("p", "Hello")]).to_html()

    def test_no_props(self):
        node = ParentNode("div", [
            LeafNode("p", "Child 1"),
            LeafNode("span", "Child 2")
        ])
        self.assertEqual(node.to_html(), '<div><p>Child 1</p><span>Child 2</span></div>')

    def test_nested_nodes(self):
        # Test a parent node inside another parent node
        inner_node = ParentNode("div", [LeafNode("p", "Inner text")])
        outer_node = ParentNode("section", [inner_node])
        self.assertEqual(outer_node.to_html(), '<section><div><p>Inner text</p></div></section>')

class TestTextNodeToHtml(unittest.TestCase):
    def test_base_case(self):
        text_node = TextNode(text="Hello", text_type=TextType.BOLD)
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.tag, "b")
        self.assertEqual(leaf_node.value, "Hello")
        self.assertEqual(leaf_node.props, {})

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )