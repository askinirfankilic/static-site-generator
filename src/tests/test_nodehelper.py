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
