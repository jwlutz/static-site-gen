import unittest
from textnode import TextNode, TextType
from split_delim import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_single_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        expected = [
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" word", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_single_bold(self):
        node = TextNode("This is **bold** text", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        expected = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" text", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_single_italic(self):
        node = TextNode("This is *italic* text", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC_TEXT)
        expected = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" text", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_delimiters(self):
        node = TextNode("Text with `code` and `more code` here", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        expected = [
            TextNode("Text with ", TextType.PLAIN_TEXT),
            TextNode("code", TextType.CODE_TEXT),
            TextNode(" and ", TextType.PLAIN_TEXT),
            TextNode("more code", TextType.CODE_TEXT),
            TextNode(" here", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_start(self):
        node = TextNode("`code` at start", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        # Empty strings are filtered out
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "code")
        self.assertEqual(new_nodes[1].text, " at start")

    def test_delimiter_at_end(self):
        node = TextNode("at end `code`", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        # Empty strings are filtered out
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "at end ")
        self.assertEqual(new_nodes[1].text, "code")

    def test_no_delimiter(self):
        node = TextNode("Just plain text", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        expected = [TextNode("Just plain text", TextType.PLAIN_TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_unclosed_delimiter_raises_exception(self):
        node = TextNode("This has `unclosed code", TextType.PLAIN_TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertIn("Invalid", str(context.exception))

    def test_non_plain_text_nodes_unchanged(self):
        nodes = [
            TextNode("Plain text", TextType.PLAIN_TEXT),
            TextNode("Bold text", TextType.BOLD_TEXT),
            TextNode("Italic text", TextType.ITALIC_TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
        # Bold and italic should remain unchanged
        self.assertEqual(new_nodes[1], TextNode("Bold text", TextType.BOLD_TEXT))
        self.assertEqual(new_nodes[2], TextNode("Italic text", TextType.ITALIC_TEXT))

    def test_multiple_nodes_in_list(self):
        nodes = [
            TextNode("First `code` node", TextType.PLAIN_TEXT),
            TextNode("Second `code` node", TextType.PLAIN_TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
        # Should have 6 nodes total (3 from each)
        self.assertEqual(len(new_nodes), 6)


if __name__ == "__main__":
    unittest.main()
