from textnode import *
import re


def split_nodes_delimiter(old_nodes: TextNode, delimiter: str, text_type: TextType) -> TextNode:
    new_nodes = []
    text = old_nodes[0].text.split()
    building_string = ""
    for i in range(len(text)):
        if text[i].startswith(delimiter):
            # Add new text node for string that been built up to delimiter
            new_nodes.append(TextNode(f"{building_string}", TextType.TEXT))
            # Make a copy of a trimmed array of remaining words to iterate through
            remaining_words = text.copy()
            remaining_words = remaining_words[i:]
            delimited_string = ""
            for word in remaining_words:
                found_matching_delimmiter = False
                if word.endswith(delimiter):
                        # Add final word of delimmited string and append to new nodes list
                        delimited_string += word
                        new_nodes.append(TextNode(f"{delimited_string.replace(delimiter, "")}", text_type))
                        # Reset building string
                        building_string = " "
                        found_matching_delimmiter = True
                        break
                # Build delimmited string
                delimited_string += word + " "
        # Only build words that are not apart of the delimitted string
        if not text[i].startswith(delimiter) and not text[i].endswith(delimiter):
            building_string += text[i] + " "
    # Clear trailing whitespace and check if matching delimiter was found
    if found_matching_delimmiter == False:
         raise Exception("Matching delimmiter never found, invalid format")
    stripped_string = building_string.rstrip()
    new_nodes.append(TextNode(f"{stripped_string}", TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    extracted_images = extract_markdown_images(old_nodes[0].text)
    extracted_images_counter = 0
    split_text = old_nodes[0].text.split()
    building_str = ""

    for i in range(len(split_text)):
        # Build normal text until image is detected
        if not split_text[i].startswith("!"):
            building_str += split_text[i] + " "
        else:
            # Append string as TextNode that has been built up to detecting an image
            new_nodes.append(TextNode(building_str, TextType.TEXT))

            # Attach appropriate alt text and url from list of tuples of images
            alt_text = extracted_images[extracted_images_counter][0]
            url = extracted_images[extracted_images_counter][1]

            # Append the new image node, reset the building string and increment the extracted image counter to get the next tuple for next image
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            building_str = " "
            extracted_images_counter += 1

    return new_nodes



def extract_markdown_images(text):
     images_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
     extracted_image = re.findall(images_regex, text)
     if len(extracted_image) == 0:
          raise Exception("Invalid format, no image found")
     return extracted_image


def extract_markdown_links(text):
     links_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
     extracted_link = re.findall(links_regex, text)
     if len(extracted_link) == 0:
          raise Exception("Invalid format, no link found")
     return extracted_link
        