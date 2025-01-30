import unittest

from LeafNode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_to_html(self):

        test_list = ('<p>This is a paragraph of text.</p>', '<a href="https://www.google.com">Click me!</a>')
        node1 = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(node1.to_html(), test_list[0])
        self.assertEqual(node2.to_html(), test_list[1])
