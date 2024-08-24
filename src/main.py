from nodes.htmlnode import HtmlNode
from nodes.textnode import TextNode


def main():
    node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    html_node = HtmlNode("This is a html node", "value of that")
    print(node)
    print(html_node)

    # tag: Optional[str],
    # value: Optional[str],
    # children: Optional[list["HtmlNode"]],
    # props=Optional[dict[str, str]],


if __name__ == "__main__":
    main()
