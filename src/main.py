from src import iohelper


def main():
    iohelper.move(iohelper.get_path_static(), iohelper.get_path_public())


if __name__ == "__main__":
    main()
