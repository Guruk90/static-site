import unittest

from src.converter import text_node_to_html_node, text_to_textnodes, split_nodes_images, split_nodes_delimiter, \
    extract_markdown_images, extract_markdown_links, split_nodes_links
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


class TestSplitNodesLinks(unittest.TestCase):

    def test_single_link(self):
        node = TextNode("This is a [link](http://example.com).", TextType.TEXT)
        expected_output = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, url="http://example.com"),
            TextNode(".", TextType.TEXT),
        ]
        result = split_nodes_links([node])
        self.assertEqual(result, expected_output)

    def test_multiple_links(self):
        node = TextNode("Here is a [link1](http://example1.com) and another [link2](http://example2.com).",
                        TextType.TEXT)
        expected_output = [
            TextNode("Here is a ", TextType.TEXT),
            TextNode("link1", TextType.LINK, url="http://example1.com"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("link2", TextType.LINK, url="http://example2.com"),
            TextNode(".", TextType.TEXT),
        ]
        result = split_nodes_links([node])
        self.assertEqual(result, expected_output)

    def test_link_at_start(self):
        node = TextNode("[link](http://example.com) is at the start.", TextType.TEXT)
        expected_output = [
            TextNode("link", TextType.LINK, url="http://example.com"),
            TextNode(" is at the start.", TextType.TEXT),
        ]
        result = split_nodes_links([node])
        self.assertEqual(result, expected_output)

    def test_link_at_end(self):
        node = TextNode("This is a [link](http://example.com)", TextType.TEXT)
        expected_output = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, url="http://example.com"),
        ]
        result = split_nodes_links([node])
        self.assertEqual(result, expected_output)

    def test_no_links(self):
        node = TextNode("This text has no links.", TextType.TEXT)
        expected_output = [
            TextNode("This text has no links.", TextType.TEXT),
        ]
        result = split_nodes_links([node])
        self.assertEqual(result, expected_output)

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        expected_output = [
            TextNode("", TextType.TEXT),
        ]
        result = split_nodes_links([node])
        self.assertEqual(result, expected_output)


class TestSplitNodesImages(unittest.TestCase):

    def test_single_image(self):
        node = TextNode("This is an ![image](http://example.com/image.png).", TextType.TEXT)
        expected_output = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, url="http://example.com/image.png"),
            TextNode(".", TextType.TEXT),
        ]
        result = split_nodes_images([node])
        self.assertEqual(result, expected_output)

    def test_multiple_images(self):
        node = TextNode("Here is an ![image1](http://example1.com/image1.png)" +
                        " and another ![image2](http://example2.com/image2.png).", TextType.TEXT)
        expected_output = [
            TextNode("Here is an ", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, url="http://example1.com/image1.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, url="http://example2.com/image2.png"),
            TextNode(".", TextType.TEXT),
        ]
        result = split_nodes_images([node])
        self.assertEqual(result, expected_output)

    def test_image_at_start(self):
        node = TextNode("![image](http://example.com/image.png) is at the start.", TextType.TEXT)
        expected_output = [
            TextNode("image", TextType.IMAGE, url="http://example.com/image.png"),
            TextNode(" is at the start.", TextType.TEXT),
        ]
        result = split_nodes_images([node])
        self.assertEqual(result, expected_output)

    def test_image_at_end(self):
        node = TextNode("This is an ![image](http://example.com/image.png)", TextType.TEXT)
        expected_output = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, url="http://example.com/image.png"),
        ]
        result = split_nodes_images([node])
        self.assertEqual(result, expected_output)

    def test_no_images(self):
        node = TextNode("This text has no images.", TextType.TEXT)
        expected_output = [
            TextNode("This text has no images.", TextType.TEXT),
        ]
        result = split_nodes_images([node])
        self.assertEqual(result, expected_output)

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        expected_output = [
            TextNode("", TextType.TEXT),
        ]
        result = split_nodes_images([node])
        self.assertEqual(result, expected_output)


class TestTextToTextNodes(unittest.TestCase):

    def test_missing_delimiters(self):
        text = "This is **bold text with missing end delimiter"
        with self.assertRaises(Exception):
            text_to_textnodes(text)

#    def test_multiple_links_and_images(self):
#        text = (
#            "Here is a [link1](http://example1.com) and another [link2](http://example2.com) "
#            "and an image ![image1](http://example.com/image1.png)"
#            "and another ![image2](http://example.com/image2.png)."
#        )
#        expected_output = [
#            TextNode("Here is a ", TextType.TEXT),
#            TextNode("link1", TextType.LINK, url="http://example1.com"),
#            TextNode(" and another ", TextType.TEXT),
#            TextNode("link2", TextType.LINK, url="http://example2.com"),
#            TextNode(" and an image ", TextType.TEXT),
#            TextNode("image1", TextType.IMAGE, url="http://example.com/image1.png"),
#            TextNode(" and another ", TextType.TEXT),
#            TextNode("image2", TextType.IMAGE, url="http://example.com/image2.png"),
#            TextNode(".", TextType.TEXT),
#        ]
#        result = text_to_textnodes(text)
#        self.assertEqual(len(result), len(expected_output))
#        for res_node, exp_node in zip(result, expected_output):
#            self.assertEqual(res_node.text, exp_node.text)
#            self.assertEqual(res_node.text_type, exp_node.text_type)
#            if res_node.text_type in [TextType.LINK, TextType.IMAGE]:
#                self.assertEqual(res_node.url, exp_node.url)

    def test_edge_cases(self):
        # Empty string
        text = ""
        expected_output = []
        result = text_to_textnodes(text)
        self.assertEqual(result, expected_output)

    def test_mixed_content(self):
        text = "Text with `code` and **bold** and *italic* and a [link](http://example.com)."
        expected_output = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, url="http://example.com"),
            TextNode(".", TextType.TEXT),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(len(result), len(expected_output))
        for res_node, exp_node in zip(result, expected_output):
            self.assertEqual(res_node.text, exp_node.text)
            self.assertEqual(res_node.text_type, exp_node.text_type)
            if res_node.text_type == TextType.LINK:
                self.assertEqual(res_node.url, exp_node.url)


if __name__ == "__main__":
    unittest.main()
