import pytest
from unittest.mock import patch
from code_mage.argsParser import arg_parser  # Adjust the import path as needed


@pytest.fixture
def mock_config():
	# A mock configuration that mimics the structure of the actual config dictionary.
	return {
		"language": "python",
		"output": "result",
		"token_usage": False,
		"model": "groq",
		"stream": False,
	}


# Test with no arguments
def test_arg_parser_no_args(mock_config):
	with patch("sys.argv", ["code_mage.py"]):
		args = arg_parser(mock_config)
		assert args.source_files == []
		assert args.language == "python"  # default from mock_config
		assert args.output == "result"  # default from mock_config
		assert args.token_usage is False
		assert args.model == "groq"
		assert args.stream is False


# Test with source file
def test_arg_parser_with_source_file(mock_config):
	with patch("sys.argv", ["code_mage.py", "example.js"]):
		args = arg_parser(mock_config)
		assert args.source_files == ["example.js"]
		assert args.language == "python"
		assert args.output == "result"


# Test with source file
def test_arg_parser_with_more_than_two_source_files(mock_config):
	with patch("sys.argv", ["code_mage.py", "example.js", "sample.js"]):
		args = arg_parser(mock_config)
		assert args.source_files == ["example.js", "sample.js"]
		assert args.language == "python"
		assert args.output == "result"


# Test with --language option
def test_arg_parser_with_language_option(mock_config):
	with patch("sys.argv", ["code_mage.py", "--language", "java"]):
		args = arg_parser(mock_config)
		assert args.language == "java"  # Overriding the config with the argument
		assert args.output == "result"  # Default from mock_config


def test_arg_parser_with_language_option_short(mock_config):
	with patch("sys.argv", ["code_mage.py", "-l", "java"]):
		args = arg_parser(mock_config)
		assert args.language == "java"  # Overriding the config with the argument
		assert args.output == "result"  # Default from mock_config


# Test with multiple options
def test_arg_parser_multiple_options(mock_config):
	with patch("sys.argv", ["code_mage.py", "--language", "java", "--output", "output_file"]):
		args = arg_parser(mock_config)
		assert args.language == "java"
		assert args.output == "output_file"


# Test --version (requires special handling since it exits the program)
def test_arg_parser_version(mock_config):
	with patch("sys.argv", ["code_mage.py", "--version"]):
		with pytest.raises(SystemExit) as excinfo:
			arg_parser(mock_config)
		assert excinfo.type is SystemExit
		assert excinfo.value.code == 0  # Should exit with code 0 for --version


def test_arg_parser_version_short(mock_config):
	with patch("sys.argv", ["code_mage.py", "-v"]):
		with pytest.raises(SystemExit) as excinfo:
			arg_parser(mock_config)
		assert excinfo.type is SystemExit
		assert excinfo.value.code == 0  # Should exit with code 0 for --version


# Test --stream option
def test_arg_parser_stream_option(mock_config):
	with patch("sys.argv", ["code_mage.py", "--stream"]):
		args = arg_parser(mock_config)
		assert args.stream is True

		# Test --stream option


def test_arg_parser_stream_option_short(mock_config):
	with patch("sys.argv", ["code_mage.py", "-s"]):
		args = arg_parser(mock_config)
		assert args.stream is True


# Test --token-usage option
def test_arg_parser_token_usage_option(mock_config):
	with patch("sys.argv", ["code_mage.py", "--token-usage"]):
		args = arg_parser(mock_config)
		assert args.token_usage is True

		# Test --token-usage option


def test_arg_parser_token_usage_option_short(mock_config):
	with patch("sys.argv", ["code_mage.py", "-t"]):
		args = arg_parser(mock_config)
		assert args.token_usage is True
