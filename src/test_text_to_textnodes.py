import unittest
from textnode import TextNode, TextType
from split_delim import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):

    def test_full_example(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.PLAIN_TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, nodes)

    def test_only_bold(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" text", TextType.PLAIN_TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_only_italic(self):
        text = "This is _italic_ text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" text", TextType.PLAIN_TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_only_code(self):
        text = "This is `code` text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("code", TextType.CODE_TEXT),
            TextNode(" text", TextType.PLAIN_TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_only_image(self):
        text = "This is an ![image](https://example.com/img.png)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is an ", TextType.PLAIN_TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
        ]
        self.assertListEqual(expected, nodes)

    def test_only_link(self):
        text = "This is a [link](https://example.com)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(expected, nodes)

    def test_plain_text_only(self):
        text = "This is just plain text"
        nodes = text_to_textnodes(text)
        expected = [TextNode("This is just plain text", TextType.PLAIN_TEXT)]
        self.assertListEqual(expected, nodes)

    def test_multiple_bold(self):
        text = "**Bold1** and **bold2**"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Bold1", TextType.BOLD_TEXT),
            TextNode(" and ", TextType.PLAIN_TEXT),
            TextNode("bold2", TextType.BOLD_TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_bold_and_italic(self):
        text = "**bold** and _italic_"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" and ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_all_inline_types(self):
        text = "**bold** _italic_ `code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" ", TextType.PLAIN_TEXT),
            TextNode("code", TextType.CODE_TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_image_and_link_together(self):
        text = "![img](https://img.com/pic.png) and [link](https://example.com)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("img", TextType.IMAGE, "https://img.com/pic.png"),
            TextNode(" and ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(expected, nodes)

    def test_complex_combination(self):
        text = "Start **bold** then _italic_ with `code` and ![img](url) end"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Start ", TextType.PLAIN_TEXT),
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" then ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" with ", TextType.PLAIN_TEXT),
            TextNode("code", TextType.CODE_TEXT),
            TextNode(" and ", TextType.PLAIN_TEXT),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode(" end", TextType.PLAIN_TEXT),
        ]
        self.assertListEqual(expected, nodes)


if __name__ == "__main__":
    unittest.main()
