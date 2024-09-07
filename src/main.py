from src import iohelper
from src.nodes import nodehelper
import os


def main():
    public_path = iohelper.get_path_public()
    static_path = iohelper.get_path_static()

    file_path = os.path.dirname(os.path.abspath(__file__))

    from_path = "/../content/"
    from_path = file_path + from_path

    template_path = "/../template.html"
    template_path = file_path + template_path

    dest_path = "/../public/"
    dest_path = file_path + dest_path

    # iohelper.delete_all_under_directory(public_path)
    # iohelper.move(static_path, public_path)
    # nodehelper.generate_page(from_path, template_path, dest_path)
    nodehelper.generate_pages_recursive(from_path, template_path, dest_path)


# def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):


if __name__ == "__main__":
    main()
