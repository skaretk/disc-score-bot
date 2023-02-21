import os
from pathlib import Path

def is_path_empty(path: Path):
    if os.path.exists(path) and not os.path.isfile(path):
        if not os.listdir(path):
            # Empty directory
            return True
        else:
            # Not empty directory
            return False
    else:
        # The path is either for a file or not valid
        return True
