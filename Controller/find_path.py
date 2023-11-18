import os


def get_project_root(current_dir:str)->str:
    """
    Traverse up until a marker indicating the root directory is found.
    Replace '.project_root' with the name of your marker file.
    """
    while not os.path.exists(os.path.join(current_dir, 'Dockerfile')):
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            # Root directory not found
            raise FileNotFoundError("Project root marker not found.")
        current_dir = parent_dir
    return current_dir

# Load configurations from config.json
project_root = get_project_root(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(project_root, 'config.json')

