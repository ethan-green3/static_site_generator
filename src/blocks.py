from enum import Enum

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
        clean_block = "\n".join(clean_lines)
        if clean_block:  # Only add non-empty blocks
            blocks.append(clean_block)
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
        
     