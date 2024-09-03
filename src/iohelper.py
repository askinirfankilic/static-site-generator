import os
import shutil


def delete_all_under_directory(directory_path: str | None) -> None:
    try:
        if directory_path is None or not os.path.isdir(directory_path):
            print(f"E: the path {directory_path} is not a valid directory")
            return

        for name in os.listdir(directory_path):
            path = os.path.join(directory_path, name)

            if os.path.isfile(path):
                try:
                    os.remove(path)
                    print(f"deleted file {path}")
                except Exception as e:
                    print(f"E: could not delete {path}. {e}")
            elif os.path.isdir(path):
                try:
                    shutil.rmtree(path)
                    print(f"deleted directory with its contents: {path}")
                except Exception as e:
                    print(f"E: could not delete directory {path}. {e}")

    except Exception as e:
        print(f"E: an error occurred: {e}")


def move(from_path: str, to_path: str) -> None:
    try:
        if not is_valid_dir(from_path) or not is_valid_dir(to_path):
            print(f"E: all paths not valid from: {from_path} to: {to_path}")
            return

        contents = get_contents_recursive(from_path, _func_recursive_content)
        if contents is None:
            print(f"could not get contents from {from_path}. aborting...")
            return
        for content in contents:
            to_content = get_to_path(content)
            ensure_dir_exists(to_content)
            to_content = os.path.dirname(to_content)
            shutil.copy(content, to_content)

            print(f"copied {content} to {to_content}")

    except Exception as e:
        print(f"E: an error occurred: {e}")


def get_path_public() -> str:
    path = get_path("../public/")
    if path is None:
        raise Exception("path is not valid")
    return path


def get_path_static() -> str:
    path = get_path("../static/")
    if path is None:
        raise Exception("path is not valid")
    return path


def get_path(ext: str) -> str | None:
    dir_path = os.path.dirname(__file__)
    path = os.path.join(dir_path, ext)
    if not os.path.isdir(path):
        print(f"E: the path {path} is not a valid directory")
        return

    return path


def is_valid_dir(path: str) -> bool:
    return os.path.isdir(path)


def ensure_dir_exists(file_path):
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)


def get_contents_recursive(path: str, recursive_func) -> list[str] | None:
    try:
        if not os.path.isdir(path):
            raise Exception("path is not a valid dir")

        return recursive_func(path, [])

    except Exception as e:
        print(f"E: an error occurred: {e}")


def get_to_path(from_path: str) -> str:
    li = from_path.rsplit("static", maxsplit=1)
    return "public".join(li)


def _func_recursive_content(path, contents):
    for name in os.listdir(path):
        new_path = os.path.join(path, name)
        if is_valid_dir(new_path):
            _func_recursive_content(new_path, contents)
        else:
            contents.append(new_path)

    return contents
