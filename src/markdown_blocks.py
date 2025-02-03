def markdown_to_blocks(markdown):

    blocks = markdown.split("\n\n")
    # Remove leading and trailing whitespaces from each block and filter out empty blocks
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks