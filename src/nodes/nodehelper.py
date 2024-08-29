import re
from src.nodes.htmlnode import HtmlNode
from src.nodes.leafnode import LeafNode
from src.nodes.textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)


def text_node_to_html_node(text_node: TextNode) -> HtmlNode:
    match text_node.text_type:
        case "text":
            return LeafNode(value=text_node.text)
        case "bold":
            return LeafNode(value=text_node.text, tag="b")
        case "italic":
            return LeafNode(value=text_node.text, tag="i")
        case "code":
            return LeafNode(value=text_node.text, tag="code")
        case "link":
            return LeafNode(
                value=text_node.text, tag="a", props={"href": text_node.url}
            )
        case "image":
            return LeafNode(
                # we use text_node.text as alt text in that case
                value="",
                tag="img",
                props={"src": text_node.url, "alt": text_node.text},
            )
        case _:
            raise Exception("Invalid text type")


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: str):
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")

        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))

        new_nodes.extend(split_nodes)

    return new_nodes


def extract_markdown_images(text):
    expression = r"!\[(.*?)\]\((.*?)\)"
    val = re.findall(expression, text)
    return val


def extract_markdown_links(text):
    expression = r"(?<!!)\[(.*?)\]\((.*?)\)"
    val = re.findall(expression, text)
    return val


def split_nodes_link(old_nodes):
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)

        extracted_links = extract_markdown_links(old_node.text)
        delimiters = []
        for link in extracted_links:
            delimiter = r"\[" + link[0] + r"\]\(" + link[1] + r"\)"
            delimiter = f"({delimiter})"
            delimiters.append(delimiter)

        regex_pattern = "|".join(delimiters)
        split_text = re.split(regex_pattern, old_node.text)
        split_text = [part for part in split_text if part]
        for text in split_text:
            finded = False
            for tup in extracted_links:
                if finded:
                    break

                for i in tup:
                    if i in text:
                        finded = True
                        new_nodes.append(TextNode(tup[0], text_type_link, tup[1]))
                        break

            if not finded:
                new_nodes.append(TextNode(text, text_type_text))

    return new_nodes


# def split_nodes_image(old_nodes):
#     new_nodes: list[TextNode] = []
#
#     return new_nodes
