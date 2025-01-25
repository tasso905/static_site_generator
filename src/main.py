from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode

def main():
    text_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(text_node)
    html_node  = HTMLNode(tag="p", value="Hello", props={"class": "greeting"})
    print(html_node)

if __name__ == "__main__":
    main()