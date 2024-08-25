from src.nodes.htmlnode import HtmlNode
from typing import Optional


class LeafNode(HtmlNode):
    def __init__(
        self,
        value: Optional[str],
        tag: Optional[str] = None,
        props: Optional[dict[str, str]] = None,
    ):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("all leaf nodes must have a value")

        html = ""
        if self.tag is None:
            html = self.value
        else:
            attributes = self.props_to_html()
            html = f"<{self.tag}{attributes}>{self.value}</{self.tag}>"

        return html
