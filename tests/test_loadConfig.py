import os
from unittest.mock import patch
from code_mage.loadConfig import load_config  # Adjust the import path accordingly


class TestLoadConfig:
	@patch("os.path.exists")
	@patch("toml.load")
	def test_load_config_file_exists(self, mock_toml_load, mock_os_exists):
		# Simulate that the file exists
		mock_os_exists.return_value = True

		# Simulate the contents of the file
		mock_toml_load.return_value = {
			"language": "Python",
			"OPENROUTER_API_KEY": "mock_openrouter_api_key",
		}

		# Call load_config function
		config = load_config()

		# Assertions
		mock_os_exists.assert_called_once_with(os.path.expanduser("~/.codemage-config.toml"))
		mock_toml_load.assert_called_once_with(os.path.expanduser("~/.codemage-config.toml"))
		assert config == {"language": "Python", "OPENROUTER_API_KEY": "mock_openrouter_api_key"}

	@patch("os.path.exists")
	def test_load_config_file_not_exists(self, mock_os_exists):
		# Simulate that the file does not exist
		mock_os_exists.return_value = False

		# Call the function under test
		config = load_config()

		# Assertions
		mock_os_exists.assert_called_once_with(os.path.expanduser("~/.codemage-config.toml"))
		assert config == {}
