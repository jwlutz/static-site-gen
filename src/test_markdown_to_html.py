import unittest
from markdown_to_html import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):

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

    def test_heading(self):
        md = "# This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>This is a heading</h1></div>")

    def test_heading_with_inline(self):
        md = "## This is a **bold** heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h2>This is a <b>bold</b> heading</h2></div>")

    def test_multiple_headings(self):
        md = """# H1

## H2

### H3

#### H4

##### H5

###### H6"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>H1</h1><h2>H2</h2><h3>H3</h3><h4>H4</h4><h5>H5</h5><h6>H6</h6></div>",
        )

    def test_quote(self):
        md = "> This is a quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a quote</blockquote></div>")

    def test_quote_multiline(self):
        md = """> This is a quote
> with multiple lines
> all quoted"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\nwith multiple lines\nall quoted</blockquote></div>",
        )

    def test_quote_with_inline(self):
        md = "> This is a **bold** quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><blockquote>This is a <b>bold</b> quote</blockquote></div>"
        )

    def test_unordered_list(self):
        md = """- Item 1
- Item 2
- Item 3"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>"
        )

    def test_unordered_list_with_inline(self):
        md = """- **Bold** item
- _Italic_ item
- `Code` item"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li><b>Bold</b> item</li><li><i>Italic</i> item</li><li><code>Code</code> item</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """1. First item
2. Second item
3. Third item"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>",
        )

    def test_ordered_list_with_inline(self):
        md = """1. **Bold** first
2. _Italic_ second
3. `Code` third"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li><b>Bold</b> first</li><li><i>Italic</i> second</li><li><code>Code</code> third</li></ol></div>",
        )

    def test_mixed_blocks(self):
        md = """# Heading

This is a paragraph with **bold** text.

- List item 1
- List item 2

> A quote"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading</h1><p>This is a paragraph with <b>bold</b> text.</p><ul><li>List item 1</li><li>List item 2</li></ul><blockquote>A quote</blockquote></div>",
        )

    def test_complex_document(self):
        md = """# Welcome

This is a **bold** statement with _italic_ text and `code`.

## Features

- Feature 1
- Feature 2
- Feature 3

> Remember: with great power comes great responsibility

```
def hello():
    print("world")
```

Visit [our site](https://example.com) for more info!"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        # Just verify it doesn't crash and contains key elements
        self.assertIn("<h1>Welcome</h1>", html)
        self.assertIn("<b>bold</b>", html)
        self.assertIn("<i>italic</i>", html)
        self.assertIn("<code>code</code>", html)
        self.assertIn("<h2>Features</h2>", html)
        self.assertIn("<ul>", html)
        self.assertIn("<blockquote>", html)
        self.assertIn("<pre><code>", html)
        self.assertIn('<a href="https://example.com">our site</a>', html)

    def test_paragraph_with_link(self):
        md = "This has a [link](https://example.com) in it"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This has a <a href="https://example.com">link</a> in it</p></div>',
        )

    def test_paragraph_with_image(self):
        md = "This has an ![image](https://example.com/img.png) in it"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This has an <img src="https://example.com/img.png" alt="image"></img> in it</p></div>',
        )


if __name__ == "__main__":
    unittest.main()
