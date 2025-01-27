from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    text_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(text_node)
    html_node  = HTMLNode(tag="p", value="Hello", props={"class": "greeting"})
    print(html_node)
    parent_node = ParentNode(tag="p", children="Hello", props={"class": "greeting"})
    print(parent_node)


if __name__ == "__main__":
    main()