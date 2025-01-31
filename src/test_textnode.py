import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("this is code", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://localhost:3000")
        node2 = TextNode("This is a text node", TextType.BOLD, "http://localhost:3000")
        self.assertEqual(node, node2)

    def test_url_None(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://localhost:3000")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("", TextType.BOLD, "http://localhost:3000")
        node2 = TextNode("This is a text node", TextType.BOLD, "http://localhost:3000")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
