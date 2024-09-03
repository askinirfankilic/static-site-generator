# write some unit tests for the nodehelper module
from sys import exception
import unittest

from src.nodes.htmlnode import HtmlNode
import src.nodes.nodehelper as helper
from src.nodes.leafnode import LeafNode
from src.nodes.textnode import TextNode


def helper_print_collection_vert(collection: list):
    print("\n")
    for elem in collection:
        print(elem)
    print("\n")


class TestNodeHelper(unittest.TestCase):
    def test_text_node_to_html_node(self):
        text_node = TextNode(text="Hello, World!", text_type="text")
        html_node = helper.text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode(value="Hello, World!"))

    def test_text_node_to_html_node_italic(self):
        text_node = TextNode(text="Hello, World!", text_type="italic")
        html_node = helper.text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode(value="Hello, World!", tag="i"))

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode(text="Hello, World!", text_type="bold")
        html_node = helper.text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode(value="Hello, World!", tag="b"))

    def test_text_node_to_html_node_link(self):
        text_node = TextNode(
            text="Hello, World!",
            text_type="link",
            url="https://example.com",
        )
        html_node = helper.text_node_to_html_node(text_node)
        self.assertEqual(
            html_node,
            LeafNode(
                value="Hello, World!",
                tag="a",
                props={"href": "https://example.com"},
            ),
        )

    def test_text_node_to_html_node_image(self):
        text_node = TextNode(
            text="alt text example",
            text_type="image",
            url="https://example.com/image.png",
        )
        html_node = helper.text_node_to_html_node(text_node)
        self.assertEqual(
            html_node,
            LeafNode(
                value="",
                tag="img",
                props={
                    "src": "https://example.com/image.png",
                    "alt": "alt text example",
                },
            ),
        )

    def test_split_nodes_delimiter(self):
        old_nodes = [
            TextNode(text="Hello 'this is a code 'World!", text_type="text"),
        ]
        new_nodes = helper.split_nodes_delimiter(old_nodes, "'", helper.text_type_code)
        self.assertEqual(
            new_nodes,
            [
                TextNode(text="Hello ", text_type="text"),
                TextNode(text="this is a code ", text_type="code"),
                TextNode(text="World!", text_type="text"),
            ],
        )

    def test_extract_markdown_images(self):
        text = """
        # Title
        ![alt text](https://example.com/image.png)
        ![alt text](https://example.com/image2.png)
        """
        images = helper.extract_markdown_images(text)
        self.assertEqual(
            images,
            [
                ("alt text", "https://example.com/image.png"),
                ("alt text", "https://example.com/image2.png"),
            ],
        )

    def test_extract_markdown_links(self):
        text = """
        # Title another things
        [alt example1 text](www.example.com) some things jdoejd:aa, ..
        [alt example2 text](https://example2.com)
        """

        images = helper.extract_markdown_links(text)
        self.assertEqual(
            images,
            [
                ("alt example1 text", "www.example.com"),
                ("alt example2 text", "https://example2.com"),
            ],
        )

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            helper.text_type_text,
        )

        test_case = [
            TextNode("This is text with a link ", helper.text_type_text),
            TextNode("to boot dev", helper.text_type_link, "https://www.boot.dev"),
            TextNode(" and ", helper.text_type_text),
            TextNode(
                "to youtube",
                helper.text_type_link,
                "https://www.youtube.com/@bootdotdev",
            ),
        ]
        splitted = helper.split_nodes_link([node])
        self.assertEqual(splitted, test_case)

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an image ![insert image in there](src/image.png)",
            helper.text_type_text,
        )

        test_case = [
            TextNode("This is text with an image ", helper.text_type_text),
            TextNode("insert image in there", helper.text_type_image, "src/image.png"),
        ]
        splitted = helper.split_nodes_image([node])
        self.assertEqual(splitted, test_case)

    def test_text_to_text_node(self):
        text = "Hello, World!"
        nodes = helper.text_to_text_node(text)
        self.assertEqual(nodes, [TextNode(text=text, text_type="text")])

    def test_text_to_text_node_bold(self):
        text = "**Hello, World!**"
        nodes = helper.text_to_text_node(text)
        self.assertEqual(nodes, [TextNode(text="Hello, World!", text_type="bold")])

    def test_text_to_text_node_italic(self):
        text = "*Hello, World!*"
        nodes = helper.text_to_text_node(text)
        self.assertEqual(nodes, [TextNode(text="Hello, World!", text_type="italic")])

    def test_text_to_text_node_code(self):
        text = "`Hello, World!`"
        nodes = helper.text_to_text_node(text)
        self.assertEqual(nodes, [TextNode(text="Hello, World!", text_type="code")])

    def test_text_to_text_node_link(self):
        text = "[Hello, World!](https://example.com)"
        nodes = helper.text_to_text_node(text)
        self.assertEqual(
            nodes,
            [
                TextNode(
                    text="Hello, World!", text_type="link", url="https://example.com"
                )
            ],
        )

    def test_text_to_text_node_image(self):
        text = "![Hello, World!](https://example.com/image.png)"
        nodes = helper.text_to_text_node(text)
        self.assertEqual(
            nodes,
            [
                TextNode(
                    text="Hello, World!",
                    text_type="image",
                    url="https://example.com/image.png",
                )
            ],
        )

    def test_text_to_text_node_image_no_alt(self):
        text = "![](https://example.com/image.png)"
        nodes = helper.text_to_text_node(text)
        self.assertEqual(
            nodes,
            [
                TextNode(
                    text="",
                    text_type="image",
                    url="https://example.com/image.png",
                )
            ],
        )

    def test_text_to_text_node_link_no_alt(self):
        text = "[](https://example.com)"
        nodes = helper.text_to_text_node(text)
        self.assertEqual(
            nodes,
            [
                TextNode(
                    text="",
                    text_type="link",
                    url="https://example.com",
                )
            ],
        )

    # create text_to_text_node tests for multiple text nodes as test cases
    def test_text_to_text_node_multiple(self):
        text = "Hello, **World!** *Hello, World!* `Hello, World!`"
        nodes = helper.text_to_text_node(text)
        self.assertEqual(
            nodes,
            [
                TextNode(text="Hello, ", text_type="text"),
                TextNode(text="World!", text_type="bold"),
                TextNode(text=" ", text_type="text"),
                TextNode(text="Hello, World!", text_type="italic"),
                TextNode(text=" ", text_type="text"),
                TextNode(text="Hello, World!", text_type="code"),
            ],
        )

    def test_text_to_text_node_multiple_complex(self):
        text = "Hello, **World!** *Hello, World!* `Hello, World!` [Hello, World!](https://example.com)"
        nodes = helper.text_to_text_node(text)
        self.assertEqual(
            nodes,
            [
                TextNode(text="Hello, ", text_type="text"),
                TextNode(text="World!", text_type="bold"),
                TextNode(text=" ", text_type="text"),
                TextNode(text="Hello, World!", text_type="italic"),
                TextNode(text=" ", text_type="text"),
                TextNode(text="Hello, World!", text_type="code"),
                TextNode(text=" ", text_type="text"),
                TextNode(
                    text="Hello, World!",
                    text_type="link",
                    url="https://example.com",
                ),
            ],
        )

    def test_markdown_to_blocks(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        blocks = helper.markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            ],
        )

    def test_markdown_to_blocks_multiple_blank_lines(self):
        markdown = """
# Heading 1


This is a paragraph with multiple blank lines above.

* List item 1
* List item 2

Another paragraph with extra spaces around the blank lines.
   
"""
        blocks = helper.markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            [
                "# Heading 1",
                "This is a paragraph with multiple blank lines above.",
                "* List item 1\n* List item 2",
                "Another paragraph with extra spaces around the blank lines.",
            ],
        )

    def test_markdown_to_blocks_no_blank_lines(self):
        markdown = """# Heading 1
This is a paragraph directly under the heading without blank lines.
* List item 1
* List item 2"""

        blocks = helper.markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            [
                "# Heading 1\nThis is a paragraph directly under the heading without blank lines.\n* List item 1\n* List item 2"
            ],
        )

    def test_block_to_block_type_code_simple(self):
        block = """```
print("Hello, world!")
```"""
        block_type = helper.block_to_block_type(block)
        self.assertEqual(block_type, helper.block_type_code)

    def test_block_to_block_type_heading(self):
        block = """#### Heading"""
        block_type = helper.block_to_block_type(block)
        self.assertEqual(block_type, helper.block_type_heading)

    def test_block_to_block_type_quote(self):
        block = "> This is a test string."
        block_type = helper.block_to_block_type(block)
        self.assertEqual(block_type, helper.block_type_quote)

    def test_block_to_block_type_unordered_list(self):
        block = "- This is a test string.\n- This is another test string."
        block_type = helper.block_to_block_type(block)
        self.assertEqual(block_type, helper.block_type_unordered_list)

    def test_block_to_block_type_unordered_list_mistake(self):
        block = "* This is a test string.\n*This is another test string."
        block_type = helper.block_to_block_type(block)
        self.assertNotEqual(block_type, helper.block_type_unordered_list)

    def test_block_to_block_type_ordered_list(self):
        block = "1. This is a no1.\n2. This is a no2."
        block_type = helper.block_to_block_type(block)
        self.assertEqual(block_type, helper.block_type_ordered_list)

    def test_block_to_block_type_ordered_list_mistake(self):
        block = "1. This is a no1.\n2.This is a no2."
        block_type = helper.block_to_block_type(block)
        self.assertNotEqual(block_type, helper.block_type_ordered_list)

    def test_block_to_block_type_paragraph(self):
        block = (
            "This is a paragraph of text.\n It has some things going on.  Like that."
        )
        block_type = helper.block_to_block_type(block)
        self.assertEqual(block_type, helper.block_type_paragraph)

    def test_markdown_to_html_node_heading(self):
        markdown = """
# This is a heading
"""
        node = helper.markdown_to_html_node(markdown)
        self.assertEqual(
            node,
            HtmlNode(
                tag="div", children=[HtmlNode(tag="h1", value="This is a heading")]
            ),
        )

    def test_markdown_to_html_node_quote(self):
        markdown = """
> This is a quote\nThis is the other line

## This is a heading but little bit smaller
"""
        node = helper.markdown_to_html_node(markdown)
        self.assertEqual(
            node,
            HtmlNode(
                tag="div",
                children=[
                    HtmlNode(
                        tag="blockquote",
                        value="This is a quote\nThis is the other line",
                    ),
                    HtmlNode(
                        tag="h2", value="This is a heading but little bit smaller"
                    ),
                ],
            ),
        )

    def test_markdown_to_html_node_code(self):
        markdown = """```
for i in something: print(i)
```

# This is a header


> This is a quote
"""
        node = helper.markdown_to_html_node(markdown)
        expected = HtmlNode(
            tag="div",
            children=[
                HtmlNode(
                    tag="pre",
                    children=[
                        HtmlNode(tag="code", value="\nfor i in something: print(i)\n"),
                    ],
                ),
                HtmlNode(tag="h1", value="This is a header"),
                HtmlNode(tag="blockquote", value="This is a quote"),
            ],
        )

        self.assertEqual(node, expected)

    def test_markdown_to_html_node_unordered_list(self):
        markdown = """
- This is a list item
- Another
- And Another
"""
        expected = HtmlNode(
            tag="div",
            children=[
                HtmlNode(
                    tag="ul",
                    children=[
                        HtmlNode(tag="li", value="This is a list item"),
                        HtmlNode(tag="li", value="Another"),
                        HtmlNode(tag="li", value="And Another"),
                    ],
                ),
            ],
        )

        node = helper.markdown_to_html_node(markdown)
        self.assertEqual(node, expected)

    def test_markdown_to_html_node_ordered_list(self):
        markdown = """
1. This is a list item
2. Another
3. And Another
"""
        expected = HtmlNode(
            tag="div",
            children=[
                HtmlNode(
                    tag="ol",
                    children=[
                        HtmlNode(tag="li", value="This is a list item"),
                        HtmlNode(tag="li", value="Another"),
                        HtmlNode(tag="li", value="And Another"),
                    ],
                ),
            ],
        )

        node = helper.markdown_to_html_node(markdown)
        self.assertEqual(node, expected)

    def test_markdown_to_html_node_mixed(self):
        markdown = """
# This is a heading

> Some quotes from someone

1. This is a list item
2. Another
3. And Another
"""
        expected = HtmlNode(
            tag="div",
            children=[
                HtmlNode(tag="h1", value="This is a heading"),
                HtmlNode(tag="blockquote", value="Some quotes from someone"),
                HtmlNode(
                    tag="ol",
                    children=[
                        HtmlNode(tag="li", value="This is a list item"),
                        HtmlNode(tag="li", value="Another"),
                        HtmlNode(tag="li", value="And Another"),
                    ],
                ),
            ],
        )

        node = helper.markdown_to_html_node(markdown)
        self.assertEqual(node, expected)
