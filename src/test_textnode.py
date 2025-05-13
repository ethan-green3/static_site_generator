import unittest

from textnode import TextNode, TextType


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



if __name__ == "__main__":
    unittest.main()