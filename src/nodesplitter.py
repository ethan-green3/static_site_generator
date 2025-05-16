from textnode import *
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

        