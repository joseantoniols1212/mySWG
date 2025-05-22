import re
from textnode import InlineTextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != InlineTextType.NORMAL:
            new_nodes.append(node)
        else:
            splitted = node.text.split(delimiter)
            if len(splitted) % 2 == 0:
                raise ValueError("invalid markdown, delimiter not closed")
            for i, text in enumerate(splitted):
                if text != "":
                    new_nodes.append(
                        TextNode(
                            text, InlineTextType.NORMAL if i % 2 == 0 else text_type
                        )
                    )
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != InlineTextType.NORMAL:
            new_nodes.append(node)
        else:
            text: str = node.text
            images_info = extract_markdown_images(text)
            for alt_text, url in images_info:
                splitted_text = text.split(f"![{alt_text}]({url})", maxsplit=1)
                first_text = splitted_text[0]
                if first_text != "":
                    new_nodes.append(TextNode(first_text, InlineTextType.NORMAL))
                new_nodes.append(TextNode(alt_text, InlineTextType.IMAGE, url))
                text = splitted_text[1]
            if text != "":
                new_nodes.append(TextNode(text, InlineTextType.NORMAL))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != InlineTextType.NORMAL:
            new_nodes.append(node)
        else:
            text: str = node.text
            links_info = extract_markdown_links(text)
            for anchor, url in links_info:
                splitted_text = text.split(f"[{anchor}]({url})", maxsplit=1)
                first_text = splitted_text[0]
                if first_text != "":
                    new_nodes.append(TextNode(first_text, InlineTextType.NORMAL))
                new_nodes.append(TextNode(anchor, InlineTextType.LINK, url))
                text = splitted_text[1]
            if text != "":
                new_nodes.append(TextNode(text, InlineTextType.NORMAL))
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, InlineTextType.NORMAL)
    res = split_nodes_link([node])
    res = split_nodes_image(res)
    res = split_nodes_delimiter(res, "`", InlineTextType.CODE)
    res = split_nodes_delimiter(res, "**", InlineTextType.BOLD)
    res = split_nodes_delimiter(res, "_", InlineTextType.ITALIC)
    return res
