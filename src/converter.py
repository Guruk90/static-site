from textnode import TextType, TextNode
from LeafNode import LeafNode


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("invalid type")


def split_nodes_delimiter(old_nodes, delimiter: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        string_list = node.text.split(delimiter)

        if len(string_list) % 2 == 0:
            raise Exception("invalid markdown syntax")
        split_nodes = []
        for i in range(len(string_list)):
            if string_list[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(string_list[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(string_list[i], text_type))
        new_nodes.extend(split_nodes)

    return new_nodes
