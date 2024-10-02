import os
import toml

def load_config():
    # Load config file from the project's root directory
    project_root = os.path.dirname(os.path.abspath(__file__))  # Get the current file's directory
    config_path = os.path.join(project_root, "../.code-mage-config.toml")  # Adjust path to project root
    if os.path.exists(config_path):
        config = toml.load(config_path)
    else:
        config = {}

    return config