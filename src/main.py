from src.nodes import nodehelper
import os


def main():
    file_path = os.path.dirname(os.path.abspath(__file__))

    from_path = "/../content/"
    from_path = file_path + from_path

    template_path = "/../template.html"
    template_path = file_path + template_path

    dest_path = "/../public/"
    dest_path = file_path + dest_path

    nodehelper.generate_pages_recursive(from_path, template_path, dest_path)


if __name__ == "__main__":
    main()
