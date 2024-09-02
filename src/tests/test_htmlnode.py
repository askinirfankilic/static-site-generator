import unittest

from src.nodes.htmlnode import HtmlNode


class TestHtmlNode(unittest.TestCase):
    def test_initialization_with_all_params(self):
        node = HtmlNode(
            tag="div",
            value="Content",
            children=[HtmlNode(tag="p", value="Child")],
            props={"class": "container"},
        )
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Content")
        self.assertEqual(node.children, [HtmlNode(tag="p", value="Child")])
        self.assertEqual(node.props, {"class": "container"})

    def test_initialization_with_no_params(self):
        node = HtmlNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_props_to_html_with_props(self):
        node = HtmlNode(props={"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), ' class="container" id="main"')

    def test_props_to_html_with_no_props(self):
        node = HtmlNode()
        self.assertEqual(node.props_to_html(), "")

    def test_eq_method(self):
        node1 = HtmlNode(tag="div", value="Content", props={"class": "container"})
        node2 = HtmlNode(tag="div", value="Content", props={"class": "container"})
        self.assertEqual(node1, node2)

    def test_eq_method_not_equal(self):
        node1 = HtmlNode(tag="div", value="Content", props={"class": "container"})
        node2 = HtmlNode(tag="p", value="Different", props={"class": "text"})
        self.assertNotEqual(node1, node2)

    def test_repr_method(self):
        node = HtmlNode(tag="div", value="Content", props={"class": "container"})
        self.assertEqual(
            repr(node), "HtmlNode(div,\nContent,\nNone,\n{'class': 'container'})"
        )


if __name__ == "__main__":
    unittest.main()
