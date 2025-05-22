import unittest

from block_markdown_funcs import (
    BlockType,
    block_to_blocktype,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestBlockFunctions(unittest.TestCase):
    def test_markdown_to_blocks_1(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_2(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line




- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_blocktype_heading(self):
        block = "#Hello world"
        actual_type = block_to_blocktype(block)
        self.assertEqual(actual_type, BlockType.HEADING)

    def test_block_to_blocktype_code(self):
        block = """
```
print("Hello world")
```
""".strip()
        actual_type = block_to_blocktype(block)
        self.assertEqual(actual_type, BlockType.CODE)

    def test_block_to_blocktype_quote(self):
        block = """
>I Love coding
> - ME
""".strip()
        actual_type = block_to_blocktype(block)
        self.assertEqual(actual_type, BlockType.QUOTE)

    def test_block_to_blocktype_unordered_list_1(self):
        block = """
- Coffee
- Butter
- Milk
- Soy sauce
""".strip()
        actual_type = block_to_blocktype(block)
        self.assertEqual(actual_type, BlockType.UNORDERED_LIST)

    def test_block_to_blocktype_unordered_list_2(self):
        block = """
- You can spend years studying the legendarium and still not understand its depths
- It can be enjoyed by children and adults alike
- Disney _didn't ruin it_ (okay, but Amazon might have)
- It created an entirely new genre of fantasy
""".strip()
        actual_type = block_to_blocktype(block)
        self.assertEqual(actual_type, BlockType.UNORDERED_LIST)

    def test_block_to_blocktype_ordered_list(self):
        block = """
1. Coffee
2. Butter
3. Milk
4. Soy sauce
""".strip()
        actual_type = block_to_blocktype(block)
        self.assertEqual(actual_type, BlockType.ORDERED_LIST)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_unordered_list(self):
        md = """
- milk 
- chocolate
"""
        blocktype = block_to_blocktype(md)
        self.assertEqual(blocktype, BlockType.UNORDERED_LIST)
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0], md.strip())
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>milk</li><li>chocolate</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. Gandalf
2. Bilbo
""".strip()
        blocktype = block_to_blocktype(md)
        self.assertEqual(blocktype, BlockType.ORDERED_LIST)
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0], md.strip())
        node = markdown_to_html_node(blocks[0])
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Gandalf</li><li>Bilbo</li></ol></div>",
        )

    def test_markdown_to_html_node(self):
        md = """
## Reasons I like Tolkien

- depths
- Disney _didn't ruin it_ I think
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>Reasons I like Tolkien</h2><ul><li>depths</li><li>Disney <i>didn't ruin it</i> I think</li></ul></div>",
        )

    def test_markdown_to_html_quoute(self):
        md = """
> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><blockquote>"I am in fact a Hobbit in all but size."  -- J.R.R. Tolkien</blockquote></div>',
        )

    def test_markdown_to_html_ordered_list_with_bold(self):
        md = """
1. **An Unnecessary Interlude**: The encounter with Tom
2. **An Outlier in Purpose**: His escapades, while rich in mirth
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li><b>An Unnecessary Interlude</b>: The encounter with Tom</li><li><b>An Outlier in Purpose</b>: His escapades, while rich in mirth</li></ol></div>",
        )
