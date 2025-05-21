from enum import Enum
from htmlnode import *
from nodesplitter import *
from parentnode import *

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'


def markdown_to_blocks(markdown):
    # Strip any leading/trailing whitespace from the entire markdown first
    markdown = markdown.strip()
    formatted_md = markdown.split("\n\n")
    blocks = []
    for block in formatted_md:
        lines = block.split("\n")
        clean_lines = [line.strip() for line in lines]
        first_line = clean_lines[0]
        if first_line.startswith("```"):
            blocks.append("\n".join(clean_lines))
        elif first_line.startswith("- "):
            blocks.append("\n".join(clean_lines))
        elif first_line[:2].isdigit() and first_line[2] == ".":
            blocks.append("\n".join(clean_lines))
        else:
             blocks.append("\n".join(clean_lines))
            
    return blocks

def block_to_block_type(block):
    if block.startswith("#"):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("- "):
        lines = block.split("\n")
        for line in lines:
            if line.startswith("- "):
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block.startswith(tuple("0123456789")):
        lines = block.split('\n')
        i = 1
        for line in lines:
            if line.startswith(str(i) + ". "):
                i += 1
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_node = ParentNode("div", children=[])
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            cleaned_block = " ".join(block.splitlines())
            parent_node.children.append(ParentNode("p", text_to_children(cleaned_block)))
            

        elif block_type == BlockType.HEADING:
            
            heading_level, remaining_text = determine_heading_level_and_remaining_text(block)
            parent_node.children.append(ParentNode(heading_level, text_to_children(remaining_text)))
            

        elif block_type == BlockType.ORDERED_LIST:
           
            children = determine_ordered_list_children(block)
            parent_node.children.append(ParentNode("ol", children))
            

        elif block_type == BlockType.UNORDERED_LIST:
            
            children = determine_unordered_list_children(block)
            parent_node.children.append(ParentNode("ul", children))
            

        elif block_type == BlockType.QUOTE:
            parent_node.children.append(ParentNode("blockquote", text_to_children(block)))
            
        elif block_type == BlockType.CODE:
            content = block.replace("```", "")
            content = content.splitlines()
            content = "\n".join(content[1:]) + "\n"
            text_node = TextNode(content, TextType.CODE)
            code_node = text_node_to_html_node(text_node)
            pre_node = ParentNode("pre", [code_node])
            parent_node.children.append(pre_node)

    return parent_node


def determine_unordered_list_children(text):
    list_of_children = []
    lines = text.split("\n")

    for line in lines:
        content = line[2:]
        if not content:
            continue
        text_nodes = text_to_textnodes(content)
        inner_list = []
        for node in text_nodes:
            child_node = text_node_to_html_node(node)
            inner_list.append(child_node)
        list_of_children.append(LeafNode("li", inner_list))

    return list_of_children

def determine_ordered_list_children(text):
    list_of_children = []
    lines = text.split("\n")
    for line in lines:
        content = line[line.find(".") + 2:]
        if not content:
            continue
        text_nodes = text_to_textnodes(content)
        inner_list = []
        for node in text_nodes:
            child_node = text_node_to_html_node(node)
            inner_list.append(child_node)

        list_of_children.append(LeafNode("li", inner_list))
        
    return list_of_children

def determine_heading_level_and_remaining_text(text):
    counter = 0
    for letter in text:
        if letter != ("#"):
            break
        counter += 1

    if counter == 1:
        return "h1", text[2:]
    elif counter == 2:
        return "h2", text[3:]
    elif counter == 3:
        return "h3", text[4:]
    elif counter == 4:
        return "h4", text[5:]
    elif counter == 5:
        return "h5", text[6:]
    elif counter == 6:
        return "h6", text[7:]


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children
     