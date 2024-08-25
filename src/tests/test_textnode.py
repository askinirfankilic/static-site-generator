import unittest

from src.nodes.textnode import TextNode


class TestTextNode(unittest.TestCase):
    # generate unit tests for the TextNode class but add arguments with names in node constructors
    def test_simple_text_node(self):
        node = TextNode(text="Hello, World!", text_type="text")
        self.assertEqual(node.text, "Hello, World!")
        self.assertEqual(node.text_type, "text")
        self.assertIsNone(node.url)

    def test_text_node_with_url(self):
        node = TextNode(
            text="Hello, World!", text_type="text", url="https://example.com"
        )
        self.assertEqual(node.text, "Hello, World!")
        self.assertEqual(node.text_type, "text")
        self.assertEqual(node.url, "https://example.com")

    def test_eq_method(self):
        node1 = TextNode(text="Hello, World!", text_type="text")
        node2 = TextNode(text="Hello, World!", text_type="text")
        self.assertEqual(node1, node2)

    def test_eq_method_not_equal(self):
        node1 = TextNode(text="Hello, World!", text_type="text")
        node2 = TextNode(text="Hello, World!", text_type="title")
        self.assertNotEqual(node1, node2)

    def test_repr_method(self):
        node = TextNode(text="Hello, World!", text_type="text")
        self.assertEqual(repr(node), "TextNode(Hello, World!, text, None)")


if __name__ == "__main__":
    unittest.main()
