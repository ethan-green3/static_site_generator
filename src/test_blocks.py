import unittest
from blocks import *
class TestBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_blocktype_heading(self):
        block = "##Heading"
        test = block_to_block_type(block)
        self.assertEqual(test, BlockType.HEADING)

    def test_block_to_blocktype_paragraph(self):
        block = "This is just a normal paragraph"
        test = block_to_block_type(block)
        self.assertEqual(test, BlockType.PARAGRAPH)        

    def test_block_to_blocktype_code(self):
        block = "```This is just a code block```"
        test = block_to_block_type(block)
        self.assertEqual(test, BlockType.CODE)

    def test_block_to_blocktype_unordered_list(self):
        testing_string = "- This is item 1\n- This is item 2 in the unordered list\n- this is item 3 in the list"
        test = block_to_block_type(testing_string)
        self.assertEqual(test, BlockType.UNORDERED_LIST)

    def test_block_to_blocktype_unordered_list_with_bad_list(self):
        testing_string = "- This is item 1\n This is item 2 in the unordered list\n- this is item 3 in the list"
        test = block_to_block_type(testing_string)
        self.assertEqual(test, BlockType.PARAGRAPH)

    def test_block_to_blocktype_ordered_list(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        test = block_to_block_type(block)
        self.assertEqual(test, BlockType.ORDERED_LIST)

    def test_block_to_blocktype_ordered_list_with_bad_order(self):
        block = "5. Item 1\n2. Item 2\n9. Item 3"
        test = block_to_block_type(block)
        self.assertEqual(test, BlockType.PARAGRAPH)