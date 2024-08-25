from nodes.htmlnode import HtmlNode
from nodes.textnode import TextNode


def main():
    node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    html_node = HtmlNode("This is a html node", "value of that")
    print(node)
    print(html_node)


if __name__ == "__main__":
    main()
