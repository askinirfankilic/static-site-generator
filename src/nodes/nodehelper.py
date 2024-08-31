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


def split_nodes_link(old_nodes):
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        extracted_links = extract_markdown_links(old_node.text)
        if extracted_links is None or len(extracted_links) == 0:
            new_nodes.append(old_node)
            continue

        delimiters = append_delimiters(extracted_links, is_image=False)

        generate_nodes(
            new_nodes,
            old_node,
            text_type_link,
            delimiters,
            extracted_links,
        )

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        extracted_links = extract_markdown_images(old_node.text)
        if extracted_links is None or len(extracted_links) == 0:
            new_nodes.append(old_node)
            continue

        delimiters = append_delimiters(extracted_links, is_image=True)

        generate_nodes(
            new_nodes,
            old_node,
            text_type_image,
            delimiters,
            extracted_links,
        )

    return new_nodes


def append_delimiters(extracted_links, is_image=False):
    delimiter_prefix = r""
    if is_image:
        delimiter_prefix = r"!"

    delimiters = []
    for link in extracted_links:
        delimiter = delimiter_prefix + r"\[" + link[0] + r"\]\(" + link[1] + r"\)"
        delimiter = f"({delimiter})"
        delimiters.append(delimiter)
    return delimiters


def generate_nodes(new_nodes, old_node, text_type, delimiters, extracted_links):
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
                    new_nodes.append(TextNode(tup[0], text_type, tup[1]))
                    break

        if not finded:
            new_nodes.append(TextNode(text, text_type_text))


def extract_markdown_images(text):
    expression = r"!\[(.*?)\]\((.*?)\)"
    val = re.findall(expression, text)
    return val


def extract_markdown_links(text):
    expression = r"(?<!!)\[(.*?)\]\((.*?)\)"
    val = re.findall(expression, text)
    return val


# i want you to impement text_to_text_node function. this function will take a string and return a list of TextNode objects.
# the sstring will contain markdown text. the markdown text will contain the following elements:
# - text: this is the default type. it will be plain text.
# - **bold text**: this will be bold text.
# - *italic text*: this will be italic text.
# - `code text`: this will be code text.
# - [link text](www.example.com): this will be a likn.
# - ![alt text](www.google.com/image.png): this will be an image.
# you can assume that the markdown text will be valid.
# you should use split functions to split the text into different parts and then create TextNode objects.  you can use the split_nodes_delimiter function to split the text into different parts. you can use the split_nodes_link and split_nodes_image functions to split the text into different parts.
# you can use the text_node_to_html_node function to convert a TextNode object to a HtmlNode object.


def text_to_text_node(text):
    nodes = [TextNode(text=text, text_type=text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes
