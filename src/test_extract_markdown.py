import unittest
from split_delim import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):

    def test_extract_single_image(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_no_images(self):
        text = "This is just plain text with no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_images_ignores_links(self):
        text = "This has a [link](https://example.com) but no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_images_with_empty_alt_text(self):
        text = "Image with no alt: ![](https://i.imgur.com/image.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "https://i.imgur.com/image.png")], matches)

    def test_extract_images_mixed_with_links(self):
        text = "Here's an ![image](https://img.com/pic.png) and a [link](https://example.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://img.com/pic.png")], matches)

    def test_extract_three_images(self):
        text = "![first](url1) some text ![second](url2) more text ![third](url3)"
        matches = extract_markdown_images(text)
        expected = [
            ("first", "url1"),
            ("second", "url2"),
            ("third", "url3")
        ]
        self.assertListEqual(expected, matches)


class TestExtractMarkdownLinks(unittest.TestCase):

    def test_extract_single_link(self):
        text = "This is text with a [link](https://www.example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://www.example.com")], matches)

    def test_extract_multiple_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_no_links(self):
        text = "This is just plain text with no links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_links_ignores_images(self):
        text = "This has an ![image](https://i.imgur.com/pic.png) but no links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_links_with_empty_anchor_text(self):
        text = "Link with no text: [](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("", "https://example.com")], matches)

    def test_extract_links_mixed_with_images(self):
        text = "Here's a [link](https://example.com) and an ![image](https://img.com/pic.png)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_three_links(self):
        text = "[first](url1) some text [second](url2) more text [third](url3)"
        matches = extract_markdown_links(text)
        expected = [
            ("first", "url1"),
            ("second", "url2"),
            ("third", "url3")
        ]
        self.assertListEqual(expected, matches)

    def test_links_and_images_together(self):
        text = "Check out this ![cool image](https://img.com/cool.png) and visit [our site](https://example.com)!"
        link_matches = extract_markdown_links(text)
        image_matches = extract_markdown_images(text)

        self.assertListEqual([("our site", "https://example.com")], link_matches)
        self.assertListEqual([("cool image", "https://img.com/cool.png")], image_matches)


if __name__ == "__main__":
    unittest.main()
