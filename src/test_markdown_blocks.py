import unittest

from src.markdown_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):

    def test_single_block(self):
        markdown = "This is a single block."
        expected_output = ["This is a single block."]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected_output)

    def test_multiple_blocks(self):
        markdown = "This is the first block.\n\nThis is the second block."
        expected_output = ["This is the first block.", "This is the second block."]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected_output)

    def test_leading_trailing_whitespace(self):
        markdown = "  This block has leading and trailing spaces.  \n\n  Another block with spaces.  "
        expected_output = ["This block has leading and trailing spaces.", "Another block with spaces."]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected_output)

    def test_empty_blocks(self):
        markdown = "Block with text.\n\n\n\nAnother block."
        expected_output = ["Block with text.", "Another block."]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected_output)

    def test_only_whitespace(self):
        markdown = "   \n\n   "
        expected_output = []
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected_output)

    def test_empty_string(self):
        markdown = ""
        expected_output = []
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
