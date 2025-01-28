from textnode import TextNode, TextType

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError()
    def props_to_html(self):
        format_string = []
        if self.props is None:
            return ""
        for k, v in self.props.items():
            formatted_prop = f' {k}="{v}"'
            format_string.append(formatted_prop)
        return "".join(format_string)  
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
  
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        self.props = props or {}  
        super().__init__(tag, value, props=self.props)
        self.children = None
    def to_html(self):
        if self.value is None:
            raise ValueError("a LeafNode must have a value!")
        if self.tag == None:
            return self.value
        elif self.props != None:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    def to_html(self):
        if self.children == None:
            raise ValueError("a ParentNode must have children")
        if self.tag == None:
            raise ValueError("a ParentNode must have a tag value")
        html = f"<{self.tag}>"
        for child in self.children:
            html+= child.to_html()
        html += f"</{self.tag}>"  # closing tag
        return html
    def __repr__(self):
        return f"ParentNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unsupported TextType: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes
        
    
    