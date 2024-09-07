import re
import os
from src import iohelper
from src.nodes.htmlnode import HtmlNode
from src.nodes.leafnode import LeafNode
from src.nodes.parentnode import ParentNode
from src.nodes.textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


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


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
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


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
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


def append_delimiters(extracted_links: list[tuple[str, str]], is_image: bool = False):
    delimiter_prefix = r""
    if is_image:
        delimiter_prefix = r"!"

    delimiters = []
    for link in extracted_links:
        delimiter = delimiter_prefix + r"\[" + link[0] + r"\]\(" + link[1] + r"\)"
        delimiter = f"({delimiter})"
        delimiters.append(delimiter)
    return delimiters


def generate_nodes(
    new_nodes: list[TextNode],
    old_node: TextNode,
    text_type: str,
    delimiters: list[str],
    extracted_links: list[tuple[str, str]],
):
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


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    expression = r"!\[(.*?)\]\((.*?)\)"
    val = re.findall(expression, text)
    return val


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    expression = r"(?<!!)\[(.*?)\]\((.*?)\)"
    val = re.findall(expression, text)
    return val


def text_to_text_node(text: str) -> list[TextNode]:
    nodes = [TextNode(text=text, text_type=text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = re.split(r"\n\s*\n", markdown)
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks


def block_to_block_type(block: str) -> str:
    if re.match(r"^#{1,6} .*", block, re.MULTILINE):
        return block_type_heading

    if len(re.findall(r"```$", block, re.MULTILINE)) == 2:
        return block_type_code

    if re.match(r"^> ", block, re.MULTILINE):
        return block_type_quote

    lines = block.splitlines()

    if all(re.match(r"^[-\*] ", line, re.MULTILINE) for line in lines):
        return block_type_unordered_list

    is_ordered_counter = 0
    for i, line in enumerate(lines):
        if line.startswith(f"{i+1}. "):
            is_ordered_counter += 1
        else:
            break

    if is_ordered_counter == len(lines):
        return block_type_ordered_list

    return block_type_paragraph


def markdown_to_html_node(markdown: str) -> HtmlNode:
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        new_node = generate_html_node_from_block(block, block_type)
        nodes.append(new_node)

    return HtmlNode(tag="div", children=nodes)


def generate_html_node_from_block(block: str, block_type: str) -> HtmlNode:
    removed_block = remove_block_type_identifier(block, block_type)
    match block_type:
        case "paragraph":
            return paragraph_to_html_node(removed_block)
        case "heading":
            match = re.match(r"^#{1,6} ", block)
            if match is None:
                raise ValueError("Invalid heading")

            indicator = match.group()
            return heading_to_html_node(removed_block, indicator)
        case "quote":
            return quote_to_html_node(removed_block)
        case "code":
            return code_to_html_node(removed_block)
        case "unordered_list":
            return unordered_list_to_html_node(removed_block)
        case "ordered_list":
            return ordered_list_to_html_node(removed_block)
        case _:
            raise Exception("invalid block type")


def paragraph_to_html_node(value: str) -> HtmlNode:
    text_nodes = text_to_text_node(value)
    html_nodes = generate_html_nodes(text_nodes)

    block_html = HtmlNode(
        tag="p",
        children=[
            LeafNode(tag=node.tag, value=node.value, props=node.props)
            for node in html_nodes
        ],
    )

    return block_html


def generate_html_nodes(text_nodes: list[TextNode]) -> list[HtmlNode]:
    html_nodes = []

    for n in text_nodes:
        html_node = text_node_to_html_node(n)
        if html_node.value is None or "":
            continue
        html_nodes.append(html_node)

    return html_nodes


def heading_to_html_node(value: str, indicator: str) -> HtmlNode:
    heading_size = indicator.count("#")
    if heading_size == 0:
        raise ValueError("Invalid heading size")

    text_nodes = text_to_text_node(value)
    html_nodes = generate_html_nodes(text_nodes)

    block_html = HtmlNode(
        tag=f"h{heading_size}",
        children=[
            LeafNode(tag=node.tag, value=node.value, props=node.props)
            for node in html_nodes
        ],
    )

    return block_html


def quote_to_html_node(value: str) -> HtmlNode:
    text_nodes = text_to_text_node(value)
    html_nodes = generate_html_nodes(text_nodes)

    block_html = HtmlNode(
        tag="blockquote",
        children=[
            LeafNode(tag=node.tag, value=node.value, props=node.props)
            for node in html_nodes
        ],
    )
    return block_html


def code_to_html_node(value: str) -> HtmlNode:
    text_nodes = text_to_text_node(value)
    html_nodes = generate_html_nodes(text_nodes)

    code_html = HtmlNode(
        tag="code",
        children=[LeafNode(value=node.value, props=node.props) for node in html_nodes],
    )

    pre_parent = HtmlNode(tag="pre", children=[code_html])
    return pre_parent


def unordered_list_to_html_node(value: str) -> HtmlNode:
    children = []
    lines = value.splitlines()
    for line in lines:
        text_nodes = text_to_text_node(line)
        html_nodes = generate_html_nodes(text_nodes)

        li_html = HtmlNode(
            tag="li",
            children=[
                LeafNode(tag=node.tag, value=node.value, props=node.props)
                for node in html_nodes
            ],
        )
        children.append(li_html)

    block_html = HtmlNode(tag="ul", value=None, children=children)
    return block_html


def ordered_list_to_html_node(value: str) -> HtmlNode:
    children = []
    lines = value.splitlines()

    for line in lines:
        text_nodes = text_to_text_node(line)
        html_nodes = generate_html_nodes(text_nodes)

        li_html = HtmlNode(
            tag="li",
            children=[
                LeafNode(tag=node.tag, value=node.value, props=node.props)
                for node in html_nodes
            ],
        )

        children.append(li_html)

    block_html = HtmlNode(tag="ol", value=None, children=children)
    return block_html


def remove_block_type_identifier(block: str, block_type: str) -> str:
    match block_type:
        case "heading":
            return re.sub(r"^#{1,6} ", "", block, count=0, flags=re.MULTILINE)

        case "code":
            return re.sub(r"```$", "", block, count=2, flags=re.MULTILINE)

        case "quote":
            return re.sub(r"^> ", "", block, count=1, flags=re.MULTILINE)

        case "unordered_list":
            lines = block.splitlines()
            return "\n".join(
                list(
                    map(
                        lambda line: re.sub(
                            r"[-\*] ", "", line, count=1, flags=re.MULTILINE
                        ),
                        lines,
                    )
                )
            )
        case "ordered_list":
            lines = block.splitlines()
            return "\n".join(
                list(
                    map(
                        lambda line: re.sub(
                            r"[0-9]\. ", "", line, count=1, flags=re.MULTILINE
                        ),
                        lines,
                    )
                )
            )
        case "paragraph":
            return block
        case _:  # assumed as paragraph
            raise Exception("Invalid block type")


def extract_title(markdown: str):
    lines = markdown.splitlines()
    for line in lines:
        if re.match(r"^#{1,6} ", line) is not None:
            ret_val = re.sub(r"^#{1,6} ", "", line, count=1)
            return ret_val.strip()

    raise Exception("can't find title to extract")


def generate_page(from_path, template_path, dest_path):
    print(f"generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    template = ""
    with open(from_path, "r") as file:
        markdown = file.read()

    with open(template_path, "r") as file:
        template = file.read()

    html = markdown_to_html_node(markdown)
    html_str = html.to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title, 1)
    template = template.replace("{{ Content }}", html_str, 1)

    with open(dest_path, "w") as f:
        f.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not iohelper.is_valid_dir(dir_path_content):
        raise Exception(f"not valid directior {dir_path_content}")

    if not iohelper.is_valid_dir(dest_dir_path):
        raise Exception(f"not valid directior {dest_dir_path}")

    iohelper.delete_all_under_directory(dest_dir_path)
    iohelper.move(iohelper.get_path_static(), iohelper.get_path_public())

    contents = iohelper.get_contents(dir_path_content)
    if contents is None:
        print("no content")
        return

    markdowns = [
        content for content in contents if os.path.splitext(content)[1] == ".md"
    ]
    markdowns = [md.replace(dir_path_content, "") for md in markdowns]

    for md in markdowns:
        from_path = dir_path_content + md
        dest_path = dest_dir_path + md.replace(".md", ".html")
        iohelper.ensure_dir_exists(dest_path)
        generate_page(from_path, template_path, dest_path)
