from typing import Optional


class TextNode:
    def __init__(self, text: str, text_type: str, url: Optional[str] = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        return (
            self.text_type == value.text_type
            and self.url == value.url
            and self.text == value.text
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
