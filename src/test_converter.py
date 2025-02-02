import unittest
from converter import text_node_to_html_node, split_nodes_delimiter, extract_markdown_links, extract_markdown_images
from textnode import TextNode, TextType


class TestConverter(unittest.TestCase):
    def test_conv_text(self):
        text_node = TextNode("test", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "test")

    def test_conv_bold(self):
        text_node = TextNode("test", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>test</b>")

    def test_conv_italic(self):
        text_node = TextNode("test", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<i>test</i>")

    def test_conv_code(self):
        text_node = TextNode("test", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<code>test</code>")

    def test_conv_link(self):
        text_node = TextNode("test", TextType.LINK, "http://localhost:3000")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<a href="http://localhost:3000">test</a>')

    def test_conv_img(self):
        text_node = TextNode("test", TextType.IMAGE, "http://localhost:3000/some.jpg")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(),
                         '<img src="http://localhost:3000/some.jpg" alt="test"></img>')


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


class TestMarkdownExtraction(unittest.TestCase):

    def test_extract_markdown_images(self):
        text = "Here is an image ![alt text](http://example.com/image.png) in markdown."
        expected_output = [('alt text', 'http://example.com/image.png')]
        self.assertEqual(extract_markdown_images(text), expected_output)

        # Test with multiple images
        text = "![first image](http://example.com/first.png) and ![second image](http://example.com/second.png)"
        expected_output = [
            ('first image', 'http://example.com/first.png'),
            ('second image', 'http://example.com/second.png')
        ]
        self.assertEqual(extract_markdown_images(text), expected_output)

        # Test with no images
        text = "This text has no images."
        expected_output = []
        self.assertEqual(extract_markdown_images(text), expected_output)

    def test_extract_markdown_links(self):
        text = "Here is a [link](http://example.com) in markdown."
        expected_output = [('link', 'http://example.com')]
        self.assertEqual(extract_markdown_links(text), expected_output)

        # Test with multiple links
        text = "[first link](http://example.com/first) and [second link](http://example.com/second)"
        expected_output = [
            ('first link', 'http://example.com/first'),
            ('second link', 'http://example.com/second')
        ]
        self.assertEqual(extract_markdown_links(text), expected_output)

        # Test with no links
        text = "This text has no links."
        expected_output = []
        self.assertEqual(extract_markdown_links(text), expected_output)


if __name__ == "__main__":
    unittest.main()
