import unittest

from inline_markdown_funcs import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import InlineTextType, TextNode


class TestInlineFunctions(unittest.TestCase):
    def test_split_nodes_delimiter_1(self):
        test_node = TextNode(
            "This is text with a `code block` word", InlineTextType.NORMAL
        )
        actual_new_nodes = split_nodes_delimiter([test_node], "`", InlineTextType.CODE)
        expected_new_nodes = [
            TextNode("This is text with a ", InlineTextType.NORMAL),
            TextNode("code block", InlineTextType.CODE),
            TextNode(" word", InlineTextType.NORMAL),
        ]
        self.assertEqual(actual_new_nodes, expected_new_nodes)

    def test_split_nodes_delimiter_2(self):
        text = "Foo fiz _buuz's_ word"
        node = TextNode(text, InlineTextType.NORMAL)
        actual_new_nodes = split_nodes_delimiter([node], "_", InlineTextType.ITALIC)
        expected_new_nodes = [
            TextNode("Foo fiz ", InlineTextType.NORMAL),
            TextNode("buuz's", InlineTextType.ITALIC),
            TextNode(" word", InlineTextType.NORMAL),
        ]
        self.assertEqual(actual_new_nodes, expected_new_nodes)

    def test_split_nodes_delimiter_3(self):
        node = TextNode("This is text with a **bold** word", InlineTextType.NORMAL)
        actual_new_nodes = split_nodes_delimiter([node], "**", InlineTextType.BOLD)
        expected_new_nodes = [
            TextNode("This is text with a ", InlineTextType.NORMAL),
            TextNode("bold", InlineTextType.BOLD),
            TextNode(" word", InlineTextType.NORMAL),
        ]
        self.assertEqual(actual_new_nodes, expected_new_nodes)

    def test_split_nodes_delimiter_4(self):
        test_node = TextNode(
            "This is text with an _italic_ word", InlineTextType.NORMAL
        )
        actual_new_nodes = split_nodes_delimiter(
            [test_node], "_", InlineTextType.ITALIC
        )
        expected_new_nodes = [
            TextNode("This is text with an ", InlineTextType.NORMAL),
            TextNode("italic", InlineTextType.ITALIC),
            TextNode(" word", InlineTextType.NORMAL),
        ]
        self.assertEqual(actual_new_nodes, expected_new_nodes)

    def test_extract_markdown_images_1(self):
        text = (
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) \\"
            "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        res = extract_markdown_images(text)
        expected_res = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(expected_res, res)

    def test_extract_markdown_images_2(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_1(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        res = extract_markdown_links(text)
        expected_res = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(res, expected_res)

    def test_split_images_1(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            InlineTextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", InlineTextType.NORMAL),
                TextNode(
                    "image", InlineTextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"
                ),
                TextNode(" and another ", InlineTextType.NORMAL),
                TextNode(
                    "second image",
                    InlineTextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

    def test_split_links_1(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ) and another [second link](https://i.imgur.com/3elNhQu)",
            InlineTextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", InlineTextType.NORMAL),
                TextNode("link", InlineTextType.LINK, "https://i.imgur.com/zjjcJKZ"),
                TextNode(" and another ", InlineTextType.NORMAL),
                TextNode(
                    "second link",
                    InlineTextType.LINK,
                    "https://i.imgur.com/3elNhQu",
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_1(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        actual_new_nodes = text_to_textnodes(text)
        expected_new_nodes = [
            TextNode("This is ", InlineTextType.NORMAL),
            TextNode("text", InlineTextType.BOLD),
            TextNode(" with an ", InlineTextType.NORMAL),
            TextNode("italic", InlineTextType.ITALIC),
            TextNode(" word and a ", InlineTextType.NORMAL),
            TextNode("code block", InlineTextType.CODE),
            TextNode(" and an ", InlineTextType.NORMAL),
            TextNode(
                "obi wan image",
                InlineTextType.IMAGE,
                "https://i.imgur.com/fJRm4Vk.jpeg",
            ),
            TextNode(" and a ", InlineTextType.NORMAL),
            TextNode("link", InlineTextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(actual_new_nodes, expected_new_nodes)

    def test_text_to_textnodes_2(self):
        text = "Disney _didn't ruin it_ I think"
        actual_new_nodes = text_to_textnodes(text)
        expected_new_nodes = [
            TextNode("Disney ", InlineTextType.NORMAL),
            TextNode("didn't ruin it", InlineTextType.ITALIC),
            TextNode(" I think", InlineTextType.NORMAL),
        ]
        self.assertEqual(actual_new_nodes, expected_new_nodes)
