import unittest

from LeafNode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_to_html(self):

        test_list = ('<p>This is a paragraph of text.</p>',
                     '<a href="https://www.google.com">Click me!</a>',
                     'This is just a text.')
        node1 = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node3 = LeafNode(None, 'This is just a text.')
        node4 = LeafNode(None, None)
        self.assertEqual(node1.to_html(), test_list[0])
        self.assertEqual(node2.to_html(), test_list[1])
        self.assertEqual(node3.to_html(), test_list[2])
        try:
            node4.to_html()
        except ValueError as e:
            self.assertEqual(e.__repr__(), "ValueError('no Value')")


if __name__ == "__main__":
    unittest.main()
