import unittest

from nodesplitter import *


class TestNodeSplitter(unittest.TestCase):

    def test_node_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT),])
           
        
    def test_node_split_italic(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("italic block", TextType.ITALIC), TextNode(" word", TextType.TEXT),])

    def test_node_split_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("bold block", TextType.ITALIC), TextNode(" word", TextType.TEXT),])

    def test_node_split_multiple_code_blocks(self):
        node = TextNode("This is text with a `code block` word `second block` captured", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word ", TextType.TEXT),
            TextNode("second block", TextType.CODE),
            TextNode(" captured", TextType.TEXT)])
    
    def test_node_split_multiple_bold_blocks(self):
        node = TextNode("This is text with a **bold block** word **second block** captured", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word ", TextType.TEXT),
            TextNode("second block", TextType.BOLD),
            TextNode(" captured", TextType.TEXT)])
        
    def test_node_split_multiple_italic_blocks(self):
        node = TextNode("This is text with a _italic block_ word _second block_ captured", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word ", TextType.TEXT),
            TextNode("second block", TextType.ITALIC),
            TextNode(" captured", TextType.TEXT)])
        
    def test_no_matching_delimiter(self):
        node = TextNode("This _is_ _text with a _italic block_ _word", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(str(context.exception), "Matching delimmiter never found, invalid format")

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_with_invalid_format(self):
        with self.assertRaises(Exception) as context:
            matches = extract_markdown_images(
                "This is text with an image"
            )
        self.assertEqual(str(context.exception), "Invalid format, no image found")
    
    def text_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.come/@bootdotdev")])
    
    def test_extract_markdown_link_with_invalid_format(self):
        with self.assertRaises(Exception) as context:
            matches = extract_markdown_links(
                "This is text with a link"
            )
        self.assertEqual(str(context.exception), "Invalid format, no link found")

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )        
