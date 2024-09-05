from src import iohelper
from src.nodes import nodehelper
import os


def main():
    # iohelper.move("", iohelper.get_path_public())

    from_path = "/../content/index.md"
    from_path = os.path.dirname(os.path.abspath(__file__)) + from_path

    template_path = "/../template.html"
    template_path = os.path.dirname(os.path.abspath(__file__)) + template_path
    nodehelper.generate_page(from_path, template_path, None)


if __name__ == "__main__":
    main()
