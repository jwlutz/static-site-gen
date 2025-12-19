import unittest
from generate_page import extract_title


class TestExtractTitle(unittest.TestCase):

    def test_extract_title_simple(self):
        markdown = "# Hello"
        title = extract_title(markdown)
        self.assertEqual(title, "Hello")

    def test_extract_title_with_content(self):
        markdown = """# Welcome to My Site

This is some content below the title."""
        title = extract_title(markdown)
        self.assertEqual(title, "Welcome to My Site")

    def test_extract_title_with_extra_whitespace(self):
        markdown = "#   Lots of Spaces   "
        title = extract_title(markdown)
        self.assertEqual(title, "Lots of Spaces")

    def test_extract_title_not_first_line(self):
        markdown = """Some intro text

# The Real Title

More content here"""
        title = extract_title(markdown)
        self.assertEqual(title, "The Real Title")

    def test_extract_title_no_h1_raises_exception(self):
        markdown = """## This is an h2

### This is an h3

No h1 here!"""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertIn("no h1 found", str(context.exception))

    def test_extract_title_empty_markdown(self):
        markdown = ""
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_with_inline_formatting(self):
        markdown = "# This is **bold** and _italic_"
        title = extract_title(markdown)
        self.assertEqual(title, "This is **bold** and _italic_")


if __name__ == "__main__":
    unittest.main()