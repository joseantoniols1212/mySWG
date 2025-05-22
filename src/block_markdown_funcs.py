import re
from enum import Enum

from htmlnode import ParentNode
from inline_markdown_funcs import text_to_textnodes
from textnode import InlineTextType, TextNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    return [x.strip() for x in markdown.split("\n\n") if x]


def is_ordered_list(splitted_block):
    for i, line in enumerate(splitted_block):
        match = re.match(r"(\d+)\. ", line)
        if match is None:
            return False
        num = int(match[1])
        if num != i + 1:
            return False
    return True


def block_to_blocktype(markdown_block):
    heading_hastags = re.match(r"^#{1,6}", markdown_block)
    if heading_hastags:
        return BlockType.HEADING
    heading_backsticks = re.match(r"```(.|\n)*```", markdown_block)
    if heading_backsticks:
        return BlockType.CODE
    splitted_block = markdown_block.split("\n")
    if all(x[0] == ">" for x in splitted_block if x):
        return BlockType.QUOTE
    if all(x[0:2] == "- " for x in splitted_block if x):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(splitted_block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_blocktype(block)
        match block_type:
            case BlockType.HEADING:
                matches = re.match(r"^(#{1,6})([\w ]*)", block)
                num_of_hastags = len(matches[1])
                header = matches[2].strip()
                children.append(
                    ParentNode(
                        tag=f"h{num_of_hastags}",
                        children=[
                            text_node.text_node_to_html_node()
                            for text_node in text_to_textnodes(header)
                        ],
                    )
                )
            case BlockType.CODE:
                matches = re.match(r"\`\`\`\n((?:.|\s)*)\`\`\`", block)
                children.append(
                    ParentNode(
                        tag="pre",
                        children=[
                            TextNode(
                                matches[1], InlineTextType.CODE
                            ).text_node_to_html_node()
                        ],
                    )
                )
            case BlockType.QUOTE:
                lines = [line[1:].strip() for line in block.split("\n")]
                content = "\n".join(lines)
                children.append(
                    ParentNode(
                        tag="blockquote",
                        children=[
                            text_node.text_node_to_html_node()
                            for text_node in text_to_textnodes(content)
                        ],
                    )
                )
            case BlockType.UNORDERED_LIST:
                lines_content = [line[2:].strip() for line in block.split("\n") if line]
                list_items = [
                    ParentNode(
                        tag="li",
                        children=[
                            text_node.text_node_to_html_node()
                            for text_node in text_to_textnodes(line_content)
                        ],
                    )
                    for line_content in lines_content
                ]
                children.append(ParentNode(tag="ul", children=list_items))
            case BlockType.ORDERED_LIST:
                lines_content = [
                    re.match(r"(?:\d*\. )(.*)", line)[1].strip()
                    for line in block.split("\n")
                ]
                list_items = [
                    ParentNode(
                        tag="li",
                        children=[
                            text_node.text_node_to_html_node()
                            for text_node in text_to_textnodes(line_content)
                        ],
                    )
                    for line_content in lines_content
                ]
                children.append(ParentNode(tag="ol", children=list_items))
            case BlockType.PARAGRAPH:
                nodes = text_to_textnodes(block)
                children.append(
                    ParentNode(
                        tag="p",
                        children=[node.text_node_to_html_node() for node in nodes],
                    )
                )
    return ParentNode(tag="div", children=children)
