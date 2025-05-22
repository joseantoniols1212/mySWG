import unittest

from textnode import TextNode, InlineTextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", InlineTextType.BOLD)
        node2 = TextNode("This is a text node", InlineTextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("This is a text node", InlineTextType.BOLD)
        node2 = TextNode("This is another text node", InlineTextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_text_type(self):
        node = TextNode("This is a text node", InlineTextType.NORMAL)
        node2 = TextNode("This is a text node", InlineTextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_url(self):
        node = TextNode(
            "This is a text node", InlineTextType.NORMAL, "https://www.google.es"
        )
        node2 = TextNode("This is a text node", InlineTextType.BOLD, "https://bing.com")
        self.assertNotEqual(node, node2)

    def test_url_default_to_none(self):
        node = TextNode("This is a text node", InlineTextType.BOLD)
        self.assertEqual(node.url, None)

    def test_repr_url_none(self):
        node = TextNode("This is a text node", InlineTextType.BOLD)
        node_repr = node.__repr__()
        self.assertEqual("TextNode(This is a text node, bold, None)", node_repr)

    def test_repr_url_non_none(self):
        node = TextNode(
            "This is a text node", InlineTextType.LINK, "https://www.google.es"
        )
        node_repr = node.__repr__()
        self.assertEqual(
            "TextNode(This is a text node, link, https://www.google.es)", node_repr
        )

    def test_text_node_to_html_node(self):
        node = TextNode("This is a text node", InlineTextType.NORMAL)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    unittest.main()
