import unittest

from src.nodes.htmlnode import HtmlNode


class TestHtmlNode(unittest.TestCase):
    test_cases = {
        "eq_1": {
            "tag": "p",
            "value": "an example paragraph",
            "props": {"href": "www.google.com"},
        },
        "eq_2": {
            "tag": "q",
            "value": "an example paragraph",
            "props": {"href": "www.google.com"},
        },
        "props_to_html": {
            "from": {
                "tag": None,
                "value": None,
                "props": {"href": "www.google.com"},
            },
            "to": ' href="www.google.com"',
        },
    }
    # href="https://www.google.com" target="_blank"

    def test_eq(self):
        node1 = self.generate_node(self.test_cases["eq_1"])
        node2 = self.generate_node(self.test_cases["eq_2"])
        self.assertNotEqual(node1, node2)

    def test_props_to_html(self):
        node = self.generate_node(self.test_cases["props_to_html"]["from"])
        html = node.props_to_html()
        self.assertEqual(html, self.test_cases["props_to_html"]["to"])

    def generate_node(self, case: dict) -> HtmlNode:
        return HtmlNode(case["tag"], case["value"], None, case["props"])


if __name__ == "__main__":
    unittest.main()
