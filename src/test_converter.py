import unittest
from converter import text_node_to_html_node
from textnode import TextNode, TextType
from LeafNode import LeafNode

class TestConverter(unittest.TestCase):
    def test_conv_text(self):
        text_node = TextNode("testar", TextType.NORMAL)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "testar")

    def test_conv_bold(self):
        text_node = TextNode("testar", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>testar</b>")

    def test_conv_italic(self):
        text_node = TextNode("testar", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<i>testar</i>")

    def test_conv_code(self):
        text_node = TextNode("testar", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<code>testar</code>")

    def test_conv_link(self):
        text_node = TextNode("testar", TextType.LINK, "http://localhost:3000")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<a href="http://localhost:3000">testar</a>')

    def test_conv_img(self):
        text_node = TextNode("testar", TextType.IMAGE, "http://localhost:3000/some.jpg")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<img src="http://localhost:3000/some.jpg" alt="testar"></img>')

