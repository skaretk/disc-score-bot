from pathlib import Path

def is_path_empty(path: Path):
    """Returns True if path does not exist or is empty, False if path is not empty"""
    if path.exists() and not path.is_file():
        if not path.iterdir():
            return True # Empty directory
        return False # Non empty directory
    return True # The path is either for a file or not valid
