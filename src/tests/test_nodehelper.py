# write some unit tests for the nodehelper module
import unittest

import src.nodes.nodehelper as helper
from src.nodes.leafnode import LeafNode
from src.nodes.textnode import TextNode


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

    # add test for split

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
