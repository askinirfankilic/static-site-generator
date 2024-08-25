from src.nodes.htmlnode import HtmlNode
from typing import Optional


class ParentNode(HtmlNode):
    # add constructor arguments with names
    def __init__(
        self,
        tag: str,
        children: list[HtmlNode],
        props: Optional[dict[str, str]] = None,
    ):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("all parent nodes must have a tag")

        if self.children is None or len(self.children) == 0:
            raise ValueError("all parent nodes must at least have one child")

        html: list[str] = []
        for child in self.children:
            html.append(child.to_html())

        attributes = self.props_to_html()
        return f"<{self.tag}{attributes}>{"".join(html)}</{self.tag}>"
