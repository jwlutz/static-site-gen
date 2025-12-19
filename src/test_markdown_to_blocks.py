import unittest
from split_delim import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
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

    def test_markdown_to_blocks_newlines(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "# This is a heading")
        self.assertEqual(
            blocks[1],
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
        )
        self.assertEqual(
            blocks[2],
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
        )

    def test_markdown_to_blocks_excessive_newlines(self):
        md = """
First block


Second block



Third block
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "First block")
        self.assertEqual(blocks[1], "Second block")
        self.assertEqual(blocks[2], "Third block")

    def test_markdown_to_blocks_whitespace(self):
        md = """
  First block with leading/trailing spaces

    Second block with tabs and spaces

Third block
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "First block with leading/trailing spaces")
        self.assertEqual(blocks[1], "Second block with tabs and spaces")
        self.assertEqual(blocks[2], "Third block")

    def test_markdown_to_blocks_single_block(self):
        md = "Just one block with no double newlines"
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0], "Just one block with no double newlines")

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_newlines(self):
        md = "\n\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_preserves_single_newlines(self):
        md = """
First line of block
Second line of block
Third line of block

Another block
With multiple lines
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(
            blocks[0], "First line of block\nSecond line of block\nThird line of block"
        )
        self.assertEqual(blocks[1], "Another block\nWith multiple lines")

    def test_markdown_to_blocks_code_block(self):
        md = """
Regular paragraph

```
code block
with multiple lines
```

Another paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "Regular paragraph")
        self.assertEqual(blocks[1], "```\ncode block\nwith multiple lines\n```")
        self.assertEqual(blocks[2], "Another paragraph")

    def test_markdown_to_blocks_mixed_content(self):
        md = """# Heading

Paragraph with **bold** and _italic_.

## Subheading

- List item 1
- List item 2

> Quote block

Final paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 6)
        self.assertEqual(blocks[0], "# Heading")
        self.assertEqual(blocks[1], "Paragraph with **bold** and _italic_.")
        self.assertEqual(blocks[2], "## Subheading")
        self.assertEqual(blocks[3], "- List item 1\n- List item 2")
        self.assertEqual(blocks[4], "> Quote block")
        self.assertEqual(blocks[5], "Final paragraph")


if __name__ == "__main__":
    unittest.main()
