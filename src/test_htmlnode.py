import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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