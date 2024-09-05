from typing import Optional


class HtmlNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[list["HtmlNode"]] = None,
        props: Optional[dict[str, Optional[str]]] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        html = ""
        if self.tag is not None:
            attributes = self.props_to_html()
            if self.value is None:
                html = f"<{self.tag}{attributes}>{"".join([child.to_html() for child in self.children])}</{self.tag}>"
            else:
                html = f"<{self.tag}{attributes}>{self.value}{"".join([child.to_html() for child in self.children])}</{self.tag}>"

            return html

        raise ValueError("all html nodes should have a tag")

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
        return f"HtmlNode(tag={self.tag},\nvalue={self.value},\nchildren={self.children},\nprops={self.props})"
