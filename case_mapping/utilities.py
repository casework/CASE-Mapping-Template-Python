import os


def is_valid_path(path: str) -> bool:
    """
    Determines if the provided path is a valid directory path or is a file path that is contained
    within a valid directory path.
    """
    return not os.path.isdir(path) and os.path.exists(os.path.dirname(path))
