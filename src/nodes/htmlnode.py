from typing import Optional


class HtmlNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[list["HtmlNode"]] = None,
        props: Optional[dict[str, str]] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        props = self.props
        if props is None:
            return ""

        attributes: list[str] = []
        for key, value in props.items():
            attributes.append(f' {key}="{value}"')

        html = "".join(attributes)
        return html

    def __eq__(self, value):
        return (
            self.tag == value.tag
            and self.value == value.value
            and self.children == value.children
            and self.props == value.props
        )

    def __repr__(self) -> str:
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"
