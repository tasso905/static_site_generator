import unittest
from textnode import *
from html_node import *
from extract_markdown import *
from inline_markdown import split_nodes_delimiter
from split_nodes import *

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

class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_link_basic(self):
        # Test case 1: no links
        node = TextNode("This is just plain text", TextType.TEXT)
        nodes = split_nodes_link([node])
        assert len(nodes) == 1
        assert nodes[0].text == "This is just plain text"
        assert nodes[0].text_type == TextType.TEXT

    # Test case 2: one link
        node = TextNode("This is a [link](https://boot.dev) to click", TextType.TEXT)
        nodes = split_nodes_link([node])
        assert len(nodes) == 3
        assert nodes[0].text == "This is a "
        assert nodes[1].text == "link"
        assert nodes[1].url == "https://boot.dev"
        assert nodes[2].text == " to click"

    def test_split_nodes_image_basic(self):
        # Test case 1: no images
        node = TextNode("This is just plain text", TextType.TEXT)
        nodes = split_nodes_image([node])
        assert len(nodes) == 1
        assert nodes[0].text == "This is just plain text"
        assert nodes[0].text_type == TextType.TEXT

        # Test case 2: one image
        node = TextNode("This is an ![image](https://example.com/img.png) to view", TextType.TEXT)
        nodes = split_nodes_image([node])
        assert len(nodes) == 3
        assert nodes[0].text == "This is an "
        assert nodes[1].text == "image"
        assert nodes[1].url == "https://example.com/img.png"
        assert nodes[2].text == " to view"

    def test_empty_text_links(self):
        node = TextNode("[](https://boot.dev)", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 1)

    def test_nodes_ending_with_link(self):
        node = TextNode("Click this link [boot.dev](https://boot.dev)", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "Click this link ")
        self.assertEqual(nodes[1].text, "boot.dev")
        self.assertEqual(nodes[1].url, "https://boot.dev")

    def test_nodes_ending_with_image(self):
        node = TextNode("Check out this image ![logo](https://example.com/logo.png)", TextType.TEXT)
        nodes = split_nodes_image([node])
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "Check out this image ")
        self.assertEqual(nodes[1].text, "logo")
        self.assertEqual(nodes[1].url, "https://example.com/logo.png")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)

    def test_mixed_markdown(self):
        node = TextNode(
            "Here's a ![image](img.png) and a [link](url)",
            TextType.TEXT
        )
        # Test splitting images first
        img_nodes = split_nodes_image([node])
        self.assertEqual(len(img_nodes), 3)
        self.assertEqual(img_nodes[0].text, "Here's a ")
        self.assertEqual(img_nodes[1].text, "image")
        self.assertEqual(img_nodes[1].url, "img.png")
        self.assertEqual(img_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(img_nodes[2].text, " and a [link](url)")

        # Test splitting links on the result
        final_nodes = split_nodes_link(img_nodes)
        self.assertEqual(len(final_nodes), 4)
        self.assertEqual(final_nodes[0].text, "Here's a ")
        self.assertEqual(final_nodes[1].text, "image")
        self.assertEqual(final_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(final_nodes[2].text, " and a ")
        self.assertEqual(final_nodes[3].text, "link")
        self.assertEqual(final_nodes[3].url, "url")
        self.assertEqual(final_nodes[3].text_type, TextType.LINK)