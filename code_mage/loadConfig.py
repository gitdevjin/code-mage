import os
import toml


def load_config():
	# Load config file from the project's root directory
	config_path = os.path.expanduser("~/.codemage-config.toml")  # Adjust path to project root
	if os.path.exists(config_path):
		config = toml.load(config_path)
	else:
		config = {}

	config["version"] = __get_version_from_pyproject()

	return config


def __get_version_from_pyproject():
	with open("pyproject.toml", "r") as f:
		pyproject_data = toml.load(f)
	return pyproject_data["tool"]["poetry"]["version"]
