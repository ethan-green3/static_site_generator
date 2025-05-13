import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="p", value="Hello, world!", props={"id": "greeting"})
        node2 = HTMLNode()
        self.assertNotEqual(node, node2)

    def test_props_to_html_with_props(self):
        node3 = HTMLNode(tag="a", value="Boot.dev", props={"href": "https://boot.dev"})
        # props_to_html should return ' href="https://boot.dev"'
        props = node3.props_to_html()
        self.assertEqual(props, ' href="https://boot.dev"')

    def test_props_to_html_with_no_props(self):
        node1 = HTMLNode(tag="p", value="No props here")
        # props_to_html should return ""
        props = node1.props_to_html()
        self.assertEqual(props, "")