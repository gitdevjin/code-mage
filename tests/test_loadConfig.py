import os
from unittest.mock import patch, mock_open
from code_mage.loadConfig import load_config  # Adjust the import path accordingly


class TestLoadConfig:
	@patch("os.path.exists")
	@patch("toml.load")
	@patch("builtins.open", new_callable=mock_open)
	def test_load_config_file_exists(self, mock_file, mock_toml_load, mock_os_exists):
		# Simulate that the config file exists
		mock_os_exists.return_value = True

		# Simulate the contents of the config file
		mock_toml_load.side_effect = [
			{
				"language": "Python",
				"OPENROUTER_API_KEY": "mock_openrouter_api_key",
			},  # First call (config file)
			{"tool": {"poetry": {"version": "0.9.0"}}},  # Second call (pyproject.toml)
		]

		# Call load_config function
		config = load_config()

		# Assertions
		mock_os_exists.assert_called_once_with(os.path.expanduser("~/.codemage-config.toml"))
		mock_file.assert_called_once_with("pyproject.toml", "r")
		assert config == {
			"language": "Python",
			"OPENROUTER_API_KEY": "mock_openrouter_api_key",
			"version": "0.9.0",
		}

	@patch("os.path.exists")
	@patch("toml.load")
	@patch("builtins.open", new_callable=mock_open)
	def test_load_config_file_with_no_content(self, mock_file, mock_toml_load, mock_os_exists):
		# Simulate that the file does not exist
		mock_os_exists.return_value = True

		# Call the function under test

		mock_toml_load.side_effect = [
			{},
			{"tool": {"poetry": {"version": "0.9.0"}}},  # Second call (pyproject.toml)
		]

		config = load_config()

		# Assertions
		mock_os_exists.assert_called_once_with(os.path.expanduser("~/.codemage-config.toml"))
		mock_file.assert_called_once_with("pyproject.toml", "r")

		# Assert the default config with version added
		assert config == {"version": "0.9.0"}

	@patch("os.path.exists")  # Third argument
	@patch("builtins.open")  # Second argument
	@patch("toml.load")  # First argument
	def test_load_config_file_not_exists(self, mock_toml_load, mock_file, mock_os_exists):
		# Simulate that the config file does not exist
		mock_os_exists.return_value = False

		# Simulate the content of the pyproject.toml file
		mock_toml_load.return_value = {"tool": {"poetry": {"version": "0.9.0"}}}

		# Call the function under test
		config = load_config()

		# Assertions
		mock_os_exists.assert_called_once_with(os.path.expanduser("~/.codemage-config.toml"))
		mock_file.assert_called_once_with("pyproject.toml", "r")
		assert config == {"version": "0.9.0"}
