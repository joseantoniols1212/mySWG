import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=props)
        props_html = node.props_to_html()
        self.assertEqual(props_html, ' href="https://www.google.com" target="_blank"')


class TestLeafNode(unittest.TestCase):
    def test_to_html_1(self):
        node_html = LeafNode("p", "This is a paragraph of text.").to_html()
        res = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node_html, res)

    def test_to_html_2(self):
        node_html = LeafNode(
            "a", "Click me!", {"href": "https://www.google.com"}
        ).to_html()
        res = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node_html, res)

    def test_to_html_3(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


class TestParentNode(unittest.TestCase):

    def test_to_html_1(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        res = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), res)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
