from src.nodes.htmlnode import HtmlNode
from src.nodes.leafnode import LeafNode
from src.nodes.textnode import TextNode


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


# It should handle each type of TextNode:
#
# text_type_text = "text"
# text_type_bold = "bold"
# text_type_italic = "italic"
# text_type_code = "code"
# text_type_link = "link"
# text_type_image = "image"
# If it gets a TextNode that is none of those types, it should raise an exception.
#
# text_type_text: This should become a LeafNode with no tag, just a raw text value.
# text_type_bold: This should become a LeafNode with a "b" tag and the text
# text_type_italic: "i" tag, text
# text_type_code: "code" tag, text
# text_type_link: "a" tag, anchor text, and "href" prop
# text_type_image: "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
