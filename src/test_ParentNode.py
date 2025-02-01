import unittest

from ParentNode import ParentNode
from LeafNode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_children_and_tag(self):
        child1 = LeafNode(tag='span', value='Child 1')
        child2 = LeafNode(tag='span', value='Child 2')
        parent = ParentNode(tag='div', children=[child1, child2])
        expected_html = '<div><span>Child 1</span><span>Child 2</span></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_to_html_with_children_tag_and_props(self):
        child = LeafNode(tag='p', value='Paragraph')
        parent = ParentNode(tag='div', children=[child], props={'class': 'container'})
        # Assuming props_to_html() converts props to ' class="container"'
        expected_html = '<div class="container"><p>Paragraph</p></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_to_html_with_no_tag(self):
        child = LeafNode(tag='span', value='Child')
        with self.assertRaises(ValueError):
            parent = ParentNode(tag=None, children=[child])
            parent.to_html()

    def test_to_html_with_no_children(self):
        with self.assertRaises(ValueError):
            parent = ParentNode(tag='div', children=None)
            parent.to_html()

    def test_to_html_with_empty_children(self):
        with self.assertRaises(ValueError):
            parent = ParentNode(tag='div', children=[])
            parent.to_html()


if __name__ == "__main__":
    unittest.main()
