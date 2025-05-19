from textnode import *
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        if delimiter not in text:
            new_nodes.append(old_node)
            continue
        
        # Process the string character by character
        i = 0
        while i < len(text):
            # Find start delimiter
            start_idx = text.find(delimiter, i)
            if start_idx == -1:
                # No more delimiters, add remaining text
                if i < len(text):
                    new_nodes.append(TextNode(text[i:], TextType.TEXT))
                break
            
            # Add text before the delimiter
            if start_idx > i:
                new_nodes.append(TextNode(text[i:start_idx], TextType.TEXT))
            
            # Find end delimiter
            end_idx = text.find(delimiter, start_idx + len(delimiter))
            if end_idx == -1:
                raise Exception(f"Matching delimmiter never found, invalid format")
            
            # Extract content between delimiters (without the delimiters)
            content = text[start_idx + len(delimiter):end_idx]
            new_nodes.append(TextNode(content, text_type))
            
            # Update position to after the end delimiter
            i = end_idx + len(delimiter)
    
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        # Skip non-text nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        images = extract_markdown_images(text)
        
        # If no images, keep original node
        if not images:
            new_nodes.append(old_node)
            continue
        
        # Use regex to find positions of matches
        matches = list(re.finditer(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text))
        
        last_end = 0
        for i, match in enumerate(matches):
            # Add text before image
            if match.start() > last_end:
                new_nodes.append(TextNode(text[last_end:match.start()], TextType.TEXT))
            
            # Add image node
            alt_text, url = images[i]
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            
            last_end = match.end()
        
        # Add remaining text after last image
        if last_end < len(text):
            new_nodes.append(TextNode(text[last_end:], TextType.TEXT))
    
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        # Skip non-text nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        links = extract_markdown_links(text)
        
        # If no links, keep original node
        if not links:
            new_nodes.append(old_node)
            continue
        
        # Use regex to find positions of matches
        matches = list(re.finditer(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text))
        
        last_end = 0
        for i, match in enumerate(matches):
            # Add text before link
            if match.start() > last_end:
                new_nodes.append(TextNode(text[last_end:match.start()], TextType.TEXT))
            
            # Add link node
            link_text, url = links[i]
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            
            last_end = match.end()
        
        # Don't forget text after the last match!
        if last_end < len(text):
            new_nodes.append(TextNode(text[last_end:], TextType.TEXT))
    
    return new_nodes

def text_to_textnodes(text):
    
    nodes = [TextNode(text, TextType.TEXT)]
   
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
  
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    nodes = split_nodes_image(nodes)
    
    nodes = split_nodes_link(nodes)
    
    return nodes



def extract_markdown_images(text):
    images_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    extracted_image = re.findall(images_regex, text)
    return extracted_image


def extract_markdown_links(text):
    links_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    extracted_link = re.findall(links_regex, text)   
    return extracted_link
        