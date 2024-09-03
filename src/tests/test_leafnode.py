import unittest

from src.nodes.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_simple_leaf_node(self):
        leaf = LeafNode(value="Hello, World!")
        self.assertEqual(leaf.to_html(), "Hello, World!")

    def test_leaf_node_with_tag(self):
        leaf = LeafNode(value="Hello, World!", tag="p")
        self.assertEqual(leaf.to_html(), "<p>Hello, World!</p>")

    def test_leaf_node_with_props(self):
        leaf = LeafNode(value="Hello, World!", tag="p", props={"class": "text"})
        self.assertEqual(leaf.to_html(), '<p class="text">Hello, World!</p>')

    def test_leaf_node_with_none_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode(value=None)
            _ = node.to_html()


if __name__ == "__main__":
    unittest.main()
