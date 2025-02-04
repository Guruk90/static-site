from src.LeafNode import LeafNode
from src.ParentNode import ParentNode
from src.converter import text_to_textnodes, text_node_to_html_node
from src.markdown_blocks import markdown_to_blocks, block_to_block_type


def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    head = ParentNode("div", [])
    for block in blocks:
        match  block_to_block_type(block):
            case "heading":
                head.children.append(markdown_to_heading_node(block))
            case "paragraph":
                head.children.append(markdown_to_paragraph_node(block))
            case "code":
                head.children.append(markdown_to_code_node(block))
            case "unordered_list":
                head.children.append(markdown_to_unordered_list_node(block))
            case "ordered_list":
                head.children.append(markdown_to_ordered_list_node(block))
            case "quote":
                head.children.append(markdown_to_quote_node(block))


def markdown_to_heading_node(text: str):

    # Count leading '#' characters to determine heading level
    heading_type_count = len(text) - len(text.lstrip('#'))
    header_type = f"h{heading_type_count}"

    # Strip leading '#' characters and whitespace to get the heading text
    heading_text = text.lstrip('#').strip()

    # Convert the heading text to text nodes
    header_textnodes = text_to_textnodes(heading_text)

    header = LeafNode(header_type, "".join(text_node_to_html_node(node).to_html() for node in header_textnodes))

    return header


def markdown_to_paragraph_node(text: str):
    paragraph_type = 'p'
    paragraph_textnodes = text_to_textnodes(text)
    paragraph = LeafNode(paragraph_type, "".join(text_node_to_html_node(node).to_html() for node in paragraph_textnodes))
    return paragraph


def markdown_to_quote_node(text: str):
    quote_type = 'blockquote'
    text = text.replace('> ','').strip()
    quote_textnodes = text_to_textnodes(text)
    quote = LeafNode(quote_type, "".join(text_node_to_html_node(node).to_html() for node in quote_textnodes))
    return quote

def markdown_to_code_node(text: str):
    code_type = 'code'
    code_textnodes = text_to_textnodes(text)
    code = LeafNode(code_type, "".join(text_node_to_html_node(node).to_html() for node in code_textnodes))
    code_parent = ParentNode('pre', [code])
    return code_parent


def markdown_to_unordered_list_node(text: str):
    unordered_list_type = 'li'
    list_items = text.split('\n')
    list_item_nodes = []
    for item in list_items:
        item_text = item.lstrip('- ').strip()
        list_item_textnodes = text_to_textnodes(item_text)
        list_item_node = LeafNode(unordered_list_type, "".join(text_node_to_html_node(node).to_html()
                                                               for node in list_item_textnodes))
        list_item_nodes.append(list_item_node)
    list_parent = ParentNode('ul', list_item_nodes)
    return list_parent


def markdown_to_ordered_list_node(text: str):
    unordered_list_type = 'li'
    list_items = text.split('\n')
    list_item_nodes = []
    for item in list_items:
        item_text = item.lstrip('- ').strip()
        list_item_textnodes = text_to_textnodes(item_text)
        list_item_node = LeafNode(unordered_list_type, "".join(text_node_to_html_node(node).to_html()
                                                               for node in list_item_textnodes))
        list_item_nodes.append(list_item_node)
    list_parent = ParentNode('ol', list_item_nodes)
    return list_parent
