import unittest
from textnode import TextNode, TextType
from split_delim import split_nodes_image, split_nodes_link


class TestSplitNodesImage(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_single_image(self):
        node = TextNode(
            "Text with ![one image](https://example.com/img.png) here",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Text with ", TextType.PLAIN_TEXT),
            TextNode("one image", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" here", TextType.PLAIN_TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_image_at_start(self):
        node = TextNode(
            "![image](https://example.com/img.png) at the start",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" at the start", TextType.PLAIN_TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_image_at_end(self):
        node = TextNode(
            "At the end ![image](https://example.com/img.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("At the end ", TextType.PLAIN_TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_no_images(self):
        node = TextNode("Just plain text with no images", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("Just plain text with no images", TextType.PLAIN_TEXT)]
        self.assertListEqual(expected, new_nodes)

    def test_split_three_images(self):
        node = TextNode(
            "![first](url1) middle ![second](url2) more ![third](url3)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("first", TextType.IMAGE, "url1"),
            TextNode(" middle ", TextType.PLAIN_TEXT),
            TextNode("second", TextType.IMAGE, "url2"),
            TextNode(" more ", TextType.PLAIN_TEXT),
            TextNode("third", TextType.IMAGE, "url3"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_non_plain_text_nodes_unchanged(self):
        nodes = [
            TextNode("Plain with ![img](url)", TextType.PLAIN_TEXT),
            TextNode("Bold text", TextType.BOLD_TEXT),
            TextNode("Code text", TextType.CODE_TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        # Bold and code should remain unchanged (but at different indices)
        self.assertEqual(new_nodes[2], TextNode("Bold text", TextType.BOLD_TEXT))
        self.assertEqual(new_nodes[3], TextNode("Code text", TextType.CODE_TEXT))

    def test_split_multiple_nodes_in_list(self):
        nodes = [
            TextNode("First ![img1](url1) node", TextType.PLAIN_TEXT),
            TextNode("Second ![img2](url2) node", TextType.PLAIN_TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(len(new_nodes), 6)
        self.assertEqual(new_nodes[0].text, "First ")
        self.assertEqual(new_nodes[1].text, "img1")
        self.assertEqual(new_nodes[3].text, "Second ")
        self.assertEqual(new_nodes[4].text, "img2")

    def test_split_only_image(self):
        node = TextNode("![only](https://example.com/img.png)", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("only", TextType.IMAGE, "https://example.com/img.png")]
        self.assertListEqual(expected, new_nodes)


class TestSplitNodesLink(unittest.TestCase):

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.PLAIN_TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_single_link(self):
        node = TextNode(
            "Text with [one link](https://example.com) here",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text with ", TextType.PLAIN_TEXT),
            TextNode("one link", TextType.LINK, "https://example.com"),
            TextNode(" here", TextType.PLAIN_TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_link_at_start(self):
        node = TextNode(
            "[link](https://example.com) at the start",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" at the start", TextType.PLAIN_TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_link_at_end(self):
        node = TextNode(
            "At the end [link](https://example.com)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("At the end ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_no_links(self):
        node = TextNode("Just plain text with no links", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("Just plain text with no links", TextType.PLAIN_TEXT)]
        self.assertListEqual(expected, new_nodes)

    def test_split_three_links(self):
        node = TextNode(
            "[first](url1) middle [second](url2) more [third](url3)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("first", TextType.LINK, "url1"),
            TextNode(" middle ", TextType.PLAIN_TEXT),
            TextNode("second", TextType.LINK, "url2"),
            TextNode(" more ", TextType.PLAIN_TEXT),
            TextNode("third", TextType.LINK, "url3"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_only_link(self):
        node = TextNode("[only](https://example.com)", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("only", TextType.LINK, "https://example.com")]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_ignores_images(self):
        node = TextNode(
            "Text with ![image](https://img.com/pic.png) but no links",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        # Should not split, just return original
        expected = [
            TextNode(
                "Text with ![image](https://img.com/pic.png) but no links",
                TextType.PLAIN_TEXT,
            )
        ]
        self.assertListEqual(expected, new_nodes)


if __name__ == "__main__":
    unittest.main()
