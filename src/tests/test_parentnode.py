import unittest
from src.nodes.leafnode import LeafNode
from src.nodes.parentnode import ParentNode


# create test class for parent node with arguments with names
class TestParentNode(unittest.TestCase):
    # generate unit tests for the ParentNode class but add arguments with names in node constructors
    def test_initialization_with_all_params(self):
        node = ParentNode(
            tag="div",
            children=[
                LeafNode(
                    value="Example Child",
                    tag="p",
                    props={"child_class": "text_child_something"},
                )
            ],
            props={"class": "container"},
        )
        self.assertEqual(node.tag, "div")
        self.assertEqual(
            node.children,
            [
                LeafNode(
                    value="Example Child",
                    tag="p",
                    props={"child_class": "text_child_something"},
                )
            ],
        )
        self.assertEqual(node.props, {"class": "container"})

    def test_to_html_method(self):
        node = ParentNode(
            tag="div",
            children=[
                LeafNode(
                    value="Example Child",
                    tag="p",
                )
            ],
            props={"class": "container"},
        )
        self.assertEqual(
            node.to_html(), '<div class="container"><p>Example Child</p></div>'
        )

    def test_to_html_method_with_multi_children(self):
        node = ParentNode(
            tag="div",
            children=[
                LeafNode(
                    value="Example Child",
                    tag="p",
                ),
                LeafNode(
                    value="Another Child",
                    tag="h",
                ),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><p>Example Child</p><h>Another Child</h></div>",
        )

    def test_to_html_method_with_nested_parents(self):
        node = ParentNode(
            tag="div",
            children=[
                ParentNode(
                    tag="p",
                    children=[
                        LeafNode(
                            value="double parent child",
                            tag="q",
                        ),
                    ],
                ),
                LeafNode(
                    value="Another Child",
                    tag="h",
                ),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><p><q>double parent child</q></p><h>Another Child</h></div>",
        )

    def test_to_html_method_with_multi_nested_parents(self):
        node = ParentNode(
            tag="div",
            children=[
                ParentNode(
                    tag="p",
                    children=[
                        ParentNode(
                            tag="q",
                            children=[
                                LeafNode(
                                    value="triple parent child",
                                    tag="r",
                                ),
                            ],
                        ),
                    ],
                ),
                LeafNode(
                    value="Another Child",
                    tag="h",
                ),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><p><q><r>triple parent child</r></q></p><h>Another Child</h></div>",
        )

    def test_to_html_method_no_children(self):
        node = ParentNode(
            tag="div",
            children=[],
            props={"class": "container"},
        )
        with self.assertRaises(ValueError):
            _ = node.to_html()

        # tag: str,
        # children: list[HtmlNode],
        # props: dict[str, str],

        # value: Optional[str],
        # tag: Optional[str] = None,
        # props: Optional[dict[str, str]] = None,
