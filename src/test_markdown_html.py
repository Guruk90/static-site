import unittest
from markdown_html import markdown_to_heading_node, markdown_to_paragraph_node, markdown_to_code_node, \
    markdown_to_unordered_list_node, markdown_to_ordered_list_node, markdown_to_quote_node
from ParentNode import ParentNode
from src.LeafNode import LeafNode


class TestMarkdownToHeadingNode(unittest.TestCase):
    class TestMarkdownToHeadingNode(unittest.TestCase):

        def test_h1_heading(self):
            text = "# Heading 1"
            expected_output = LeafNode("h1", "Heading 1")
            result = markdown_to_heading_node(text)
            self.assertEqual(result, expected_output)

        def test_h2_heading(self):
            text = "## Heading 2"
            expected_output = LeafNode("h2", "Heading 2")
            result = markdown_to_heading_node(text)
            self.assertEqual(result, expected_output)

        def test_h3_heading(self):
            text = "### Heading 3"
            expected_output = LeafNode("h3", "Heading 3")
            result = markdown_to_heading_node(text)
            self.assertEqual(result, expected_output)

        def test_h4_heading(self):
            text = "#### Heading 4"
            expected_output = LeafNode("h4", "Heading 4")
            result = markdown_to_heading_node(text)
            self.assertEqual(result, expected_output)

        def test_h5_heading(self):
            text = "##### Heading 5"
            expected_output = LeafNode("h5", "Heading 5")
            result = markdown_to_heading_node(text)
            self.assertEqual(result, expected_output)

        def test_h6_heading(self):
            text = "###### Heading 6"
            expected_output = LeafNode("h6", "Heading 6")
            result = markdown_to_heading_node(text)
            self.assertEqual(result, expected_output)

        def test_no_heading(self):
            text = "No heading"
            expected_output = LeafNode("h0", "No heading")
            result = markdown_to_heading_node(text)
            self.assertEqual(result, expected_output)

        def test_to_html(self):
            text = "# Heading 1"
            expected_output = "<h1>Heading 1</h1>"
            result = markdown_to_heading_node(text).to_html()
            self.assertEqual(result, expected_output)


class TestMarkdownToParagraphNode(unittest.TestCase):

    def test_paragraph_node(self):
        text = "This is a **paragraph**."
        expected_output = LeafNode("p", "This is a <b>paragraph</b>.")
        result = markdown_to_paragraph_node(text)
        self.assertEqual(result, expected_output)

    def test_paragraph_to_html(self):
        text = "This is a **paragraph**."
        paragraph_node = markdown_to_paragraph_node(text)
        expected_html = "<p>This is a <b>paragraph</b>.</p>"
        self.assertEqual(paragraph_node.to_html(), expected_html)


class TestMarkdownToCodeNode(unittest.TestCase):

    def test_code_node(self):
        text = "def foo():\n    return 'bar'"
        expected_code = LeafNode("code", "def foo():\n    return 'bar'")
        expected_output = ParentNode("pre", [expected_code])
        result = markdown_to_code_node(text)
        self.assertEqual(result, expected_output)

    def test_code_to_html(self):
        text = "def foo():\n    return 'bar'"
        code_node = markdown_to_code_node(text)
        expected_html = "<pre><code>def foo():\n    return 'bar'</code></pre>"
        self.assertEqual(code_node.to_html(), expected_html)


class TestMarkdownToUnorderedListNode(unittest.TestCase):

    def test_single_list_item(self):
        text = "- Item 1"
        expected_item = LeafNode("li", "Item 1")
        expected_output = ParentNode("ul", [expected_item])
        result = markdown_to_unordered_list_node(text)
        self.assertEqual(result, expected_output)

    def test_multiple_list_items(self):
        text = "- Item 1\n- Item 2\n- Item 3"
        expected_items = [
            LeafNode("li", "Item 1"),
            LeafNode("li", "Item 2"),
            LeafNode("li", "Item 3")
        ]
        expected_output = ParentNode("ul", expected_items)
        result = markdown_to_unordered_list_node(text)
        self.assertEqual(result, expected_output)

    def test_list_to_html(self):
        text = "- Item 1\n- Item 2\n- Item 3"
        list_node = markdown_to_unordered_list_node(text)
        expected_html = "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>"
        self.assertEqual(list_node.to_html(), expected_html)


class TestMarkdownToOrderedListNode(unittest.TestCase):

    def test_single_list_item(self):
        text = "1. Item 1"
        expected_item = LeafNode("li", "Item 1")
        expected_output = ParentNode("ol", [expected_item])
        result = markdown_to_ordered_list_node(text)
        self.assertEqual(result, expected_output)

    def test_multiple_list_items(self):
        text = "1. Item 1\n2. Item 2\n3. Item 3"
        expected_items = [
            LeafNode("li", "Item 1"),
            LeafNode("li", "Item 2"),
            LeafNode("li", "Item 3")
        ]
        expected_output = ParentNode("ol", expected_items)
        result = markdown_to_ordered_list_node(text)
        self.assertEqual(result, expected_output)

    def test_list_to_html(self):
        text = "1. Item 1\n2. Item 2\n3. Item 3"
        list_node = markdown_to_ordered_list_node(text)
        expected_html = "<ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol>"
        self.assertEqual(list_node.to_html(), expected_html)


class TestMarkdownToQuoteNode(unittest.TestCase):

    def test_single_line_quote(self):
        text = "> This is a quote."
        expected_output = LeafNode("blockquote", "This is a quote.")
        result = markdown_to_quote_node(text)
        self.assertEqual(result, expected_output)

    def test_multi_line_quote(self):
        text = "> This is a quote.\n> It spans multiple lines."
        expected_output = LeafNode("blockquote", "This is a quote.\nIt spans multiple lines.")
        result = markdown_to_quote_node(text)
        self.assertEqual(result, expected_output)

    def test_quote_to_html(self):
        text = "> This is a quote."
        quote_node = markdown_to_quote_node(text)
        expected_html = "<blockquote>This is a quote.</blockquote>"
        self.assertEqual(quote_node.to_html(), expected_html)


if __name__ == "__main__":
    unittest.main()
