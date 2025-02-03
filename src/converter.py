import re


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


def extract_markdown_images(text: str):
    images = re.findall(r'!\[(.*?)]\((.*?)\)', text)
    return images


def extract_markdown_links(text: str):
    links = re.findall(r'(?<!\!)\[(.*?)]\((.*?)\)', text)
    return links


def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        # Extract links
        links = extract_markdown_links(node.text)
        text: str = node.text

        if not links:
            new_nodes.append(TextNode(text, TextType.TEXT))
            continue

        for link_text, link_url in links:
            texts = text.split(f"[{link_text}]({link_url})", 1)

            if texts[0] == '':
                del texts[0]
                text = texts[0]
            else:
                new_nodes.append(TextNode(texts[0], TextType.TEXT))
                text = texts[1]

            new_nodes.append(TextNode(link_text, TextType.LINK, url=link_url))
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        # Extract images
        images = extract_markdown_images(node.text)
        text: str = node.text

        if not images:
            new_nodes.append(TextNode(text, TextType.TEXT))
            continue

        for alt_text, image_url in images:
            texts = text.split(f"![{alt_text}]({image_url})", 1)

            if texts[0] == '':
                del texts[0]
                text = texts[0]
            else:
                new_nodes.append(TextNode(texts[0], TextType.TEXT))
                text = texts[1]

            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url=image_url))
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):

    if not text:
        return []

    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_images([node])
    nodes = split_nodes_links(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes
