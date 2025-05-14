import unittest

from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("Hello World", TextType.LINK, "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")
        node2 = TextNode("test123", TextType.BOLD, "https://www.wikipedia.org/")
        self.assertNotEqual(node, node2)
    
    def test_eq_function(self):
        node = TextNode("Hello World", TextType.LINK, "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")
        node2 = TextNode("test123", TextType.BOLD, "https://www.wikipedia.org/")
        test = node.__eq__(node2)
        # Test should be False, so assertEqual should be True evaluating False = False
        self.assertEqual(test, False)


    # No URL is passed so url should be None
    def test_url_property(self):
        node = TextNode("Hello World", TextType.BOLD)
        self.assertEqual(node.url, None)
    
    # node and node 2 have different text types so NotEqual should be True
    def test_different_text_types(self):
        node = TextNode("Hello world", TextType.BOLD)
        node2 = TextNode("Hello world", TextType.CODE)
        self.assertNotEqual(node, node2)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
    
    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
    
    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "www.bootdev.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "www.bootdev.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {'src': 'www.bootdev.com', 'alt': 'This is an image node'})



if __name__ == "__main__":
    unittest.main()