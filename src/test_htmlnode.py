import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "this is a text")
        node2 = HTMLNode("p", "this is a text")
        self.assertEqual(node, node2)

    def test_if_vale_no_children(self):
        node = HTMLNode("p", "this is a text")
        node2 = HTMLNode("p", "this is a text")
        self.assertIsNone(node.children)
        self.assertIsNone(node2.children)
        # self.assertEqual(node, node2)

    def test_props_to_html(self):

        html_string = ' href="https://www.google.com" target="_blank"'
        node = HTMLNode(
            "a",
            "this is a text",
            None,
            {"href": "https://www.google.com", "target": "_blank"})

        self.assertEqual(node.props_to_html(), html_string)

    def test_if_no_value_children(self):
        node = HTMLNode("p", "this is a text")
        nodes = [node]
        node2 = HTMLNode("p", children=nodes)
        self.assertIsNotNone(node2.children)

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, None, {'class': 'primary'})",
        )