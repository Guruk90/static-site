import re


def markdown_to_blocks(markdown):

    blocks = markdown.split("\n\n")
    # Remove leading and trailing whitespaces from each block and filter out empty blocks
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks


def block_to_block_type(text):
    lines = text.splitlines()
    if text.startswith("# "):
        return "heading"
    elif text.startswith("- ") or text.startswith("* "):
        return "unordered_list"
    elif text.startswith("> "):
        return "quote"
    elif re.match(r'^\d+.', text):
        return "ordered_list"
    elif len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return "code"
    else:
        return "paragraph"

