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

    def test_to_html_with_value_and_tag(self):
        node = LeafNode(tag='p', value='Hello, World!')
        self.assertEqual(node.to_html(), '<p>Hello, World!</p>')

    def test_to_html_with_value_tag_and_props(self):
        node = LeafNode(tag='a', value='Click here', props={'href': 'http://example.com'})
        # Assuming props_to_html() converts props to ' href="http://example.com"'
        self.assertEqual(node.to_html(), '<a href="http://example.com">Click here</a>')

    def test_to_html_with_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode(tag='p', value=None)
            node.to_html()

    def test_to_html_with_no_tag(self):
        node = LeafNode(tag=None, value='Just text')
        self.assertEqual(node.to_html(), 'Just text')

    def test_to_html_with_empty_tag(self):
        node = LeafNode(tag='', value='Just text')
        self.assertEqual(node.to_html(), 'Just text')

    def test_to_html_with_no_props(self):
        node = LeafNode(tag='div', value='Content')
        self.assertEqual(node.to_html(), '<div>Content</div>')


if __name__ == "__main__":
    unittest.main()
