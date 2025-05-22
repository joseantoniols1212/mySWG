from enum import Enum
from htmlnode import LeafNode


class InlineTextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def text_node_to_html_node(self):
        match self.text_type:
            case InlineTextType.NORMAL:
                return LeafNode(None, self.text.replace("\n", " "))
            case InlineTextType.BOLD:
                return LeafNode("b", self.text.replace("\n", " "))
            case InlineTextType.ITALIC:
                return LeafNode("i", self.text.replace("\n", " "))
            case InlineTextType.CODE:
                return LeafNode("code", self.text)
            case InlineTextType.LINK:
                props = {"href": self.url}
                return LeafNode("a", self.text, props=props)
            case InlineTextType.IMAGE:
                props = {"src": self.url, "alt": self.text}
                return LeafNode("img", "", props=props)
            case _:
                raise ValueError(
                    "TextNode to HTMLNode conversion requires valid text type"
                )
