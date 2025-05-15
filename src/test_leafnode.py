import unittest

from leafnode import *


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p_with_none_text(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_value_error(self):
        with self.assertRaises(ValueError) as context:
            # Instantiation should happen inside the context manager
            LeafNode(tag="p", value=None)

        # Assert that the correct exception message is raised
        self.assertEqual(str(context.exception), "All leaf nodes must have a value")
