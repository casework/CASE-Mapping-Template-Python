import hashlib
import os


def is_valid_path(path: str) -> bool:
    """
    Determines if the provided path is a valid directory path or is a file path that is contained
    within a valid directory path.
    """
    # TODO
    return True


def get_files_in_dir(path: str) -> list:
    """
    Retrieves the list of files contained within a directory.
    """
    if not is_valid_path(path):
        raise FileNotFoundError("Path does not exist: {path}")

    # list to store files
    files = []

    # Iterate directory
    for relative_path in os.listdir(path):
        # check if current path is a file
        if os.path.isfile(os.path.join(path, relative_path)):
            files.append(relative_path)

    return files


def hash_file(file_path, hash_algo=hashlib.sha256()):
    """
    Generates a hash of a file by chunking it and utilizing the Python hashlib library.
    """
    # Ensure the file path exists
    if not os.path.exists(file_path):
        raise IOError(
            "The file path {} is not valid, the file does not exist".format(file_path)
        )

    with open(file_path, "rb") as f:
        while True:
            # Reading is buffered, so we can read smaller chunks.
            chunk = f.read(hash_algo.block_size)
            if not chunk:
                break
            hash_algo.update(chunk)
    return hash_algo.hexdigest()
