from textnode import *

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
        
    
    