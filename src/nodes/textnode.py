from typing import Optional

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


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
