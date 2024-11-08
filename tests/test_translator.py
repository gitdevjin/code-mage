import pytest
from unittest.mock import patch, Mock, MagicMock
from code_mage.translator import Translator


class TestTranslatorConstructor:
	@pytest.fixture
	def mock_args(self):
		"""Fixture for simulating command-line arguments."""
		return Mock(
			language=None,  # Example language
			model=None,
			stream=False,
			token_usage=False,
			output=None,
		)

	@pytest.fixture
	def mock_config(self):
		"""Fixture for simulating a configuration."""
		return Mock()

	def test_constructor_initialization(self, mock_args, mock_config):
		"""Test the constructor of the Translator class."""
		# Create the Translator object using the constructor
		translator = Translator(mock_args, mock_config)

		# Verify that the object is created successfully
		assert isinstance(translator, Translator)

		# Verify that attributes are set correctly
		assert translator.args == mock_args  # Ensure 'args' is set correctly
		assert translator.config == mock_config  # Ensure 'config' is set correctly

		# Check if the default language is correctly set
		assert translator.target_lang == "python"

	def test_constructor_with_wrong_args(self, mock_args, mock_config):
		mock_args.language = "html"
		# Create the Translator object using the constructor
		with pytest.raises(SystemExit):
			translator = Translator(mock_args, mock_config)  # noqa


class TestTranslatorPrivateMethods:
	@pytest.fixture
	def mock_args(self):
		"""Fixture for simulating command-line arguments."""
		return Mock(language=None, model=None, stream=False, token_usage=False, output=None)

	@pytest.fixture
	def mock_config(self):
		"""Fixture for simulating a configuration."""
		return Mock()

	@pytest.fixture
	def translator(self, mock_args, mock_config):
		"""Fixture for creating a Translator instance."""
		return Translator(mock_args, mock_config)

	def test_get_source_lang(self, translator):
		# Directly accessing the private __get_source_lang method
		assert translator._Translator__get_source_lang(".js") == "javascript"
		assert translator._Translator__get_source_lang(".py") == "python"
		assert translator._Translator__get_source_lang(".cpp") == "c++"
		assert translator._Translator__get_source_lang(".java") == "java"

	def test_get_output_ext(self, translator):
		# Testing the private __get_output_ext method
		assert translator._Translator__get_output_ext("javascript") == ".js"
		assert translator._Translator__get_output_ext("python") == ".py"
		assert translator._Translator__get_output_ext("c++") == ".cpp"
		assert translator._Translator__get_output_ext("java") == ".java"


class TestTranslatorWithWrongArgs:
	@pytest.fixture
	def mock_args(self):
		"""Fixture for simulating command-line arguments."""
		return Mock(language=None, model=None, stream=False, token_usage=False, output=None)

	@pytest.fixture
	def mock_config(self):
		"""Fixture for simulating a configuration."""
		return Mock()

	@pytest.fixture
	def translator(self, mock_args, mock_config):
		"""Fixture for creating a Translator instance."""
		return Translator(mock_args, mock_config)

	def test_target_lang_source_lang_same(self, translator, mock_args):
		with pytest.raises(SystemExit) as exc_info:
			translator.translate("./example/test.py")

		assert str(exc_info.value) == "the target language is the same with the source_file"

	def test_unsupported_src_lang(self, translator, mock_args):
		with pytest.raises(SystemExit) as exc_info:
			translator.translate("./example/test.c")

		assert str(exc_info.value) == "the file is not written in a supported programming language"


class TestTranslator:
	@pytest.fixture
	def mock_args(self):
		"""Fixture for simulating command-line arguments."""
		return Mock(language=None, model=None, stream=False, token_usage=False, output=None)

	def mock_api_call(self, *args, **kwargs):
		mock_response = MagicMock()
		mock_response.choices = [{"message": {"content": "Translated code"}}]
		return mock_response

	@patch("builtins.open", new_callable=MagicMock)  # Mock open
	@patch("code_mage.translator.Api")  # Mock Api class
	@patch.object(Translator, "_Translator__get_output_filename", return_value="translated_test.py")
	def test_translate(self, mock_get_output_filename, mock_api, mock_open, mock_args):
		mock_config = {"api_key": "fake_api_key"}

		# Initialize Translator instance
		translator = Translator(mock_args, mock_config)

		mock_file = MagicMock()
		mock_open.return_value = mock_file

		# Mock the Api's call_api method
		mock_api_instance = MagicMock()
		mock_api.return_value = mock_api_instance
		mock_api_instance.chat.completions.create = MagicMock(return_value=self.mock_api_call())

		translator.translate("./example/test.js")

		assert mock_api_instance.chat.completions.create.return_value.choices == [
			{"message": {"content": "Translated code"}}
		]

		mock_open.assert_any_call("./example/test.js", "r")
		mock_open.assert_any_call("translated_test.py", "w")


class TestTranslatorWithStreamFlagAndTokenUsage:
	@pytest.fixture
	def mock_args(self):
		"""Fixture for simulating command-line arguments."""
		return Mock(language=None, model=None, stream=True, token_usage=True, output=None)

	def mock_api_call(self, *args, **kwargs):
		mock_response = MagicMock()
		mock_response.choices = [{"message": {"content": "Translated code"}}]
		return mock_response

	@patch("builtins.open", new_callable=MagicMock)  # Mock open
	@patch("code_mage.translator.Api")  # Mock Api class
	@patch.object(Translator, "_Translator__get_output_filename", return_value="translated_test.py")
	def test_translate(self, mock_get_output_filename, MockApi, mock_open, mock_args, capsys):
		mock_config = {"api_key": "fake_api_key"}

		# Initialize Translator instance
		translator = Translator(mock_args, mock_config)

		mock_file = MagicMock()
		mock_open.return_value = mock_file

		# Mock the Api's call_api method
		mock_api_instance = MagicMock()
		MockApi.return_value = mock_api_instance
		mock_api_instance.chat.completions.create = MagicMock(return_value=self.mock_api_call())

		translator.translate("./example/test.js")

		assert mock_api_instance.chat.completions.create.return_value.choices == [
			{"message": {"content": "Translated code"}}
		]

		captured = capsys.readouterr()
		assert "\nStream Flag Doesn't Support Token-Usage Option" in captured


class TestTranslatorWithResult:
	@pytest.fixture
	def mock_args(self):
		"""Fixture for simulating command-line arguments."""
		return Mock(language=None, model=None, stream=True, token_usage=False, output=None)

	def mock_api_call(self, *args, **kwargs):
		mock_response = MagicMock()
		mock_response.choices = [{"message": {"content": "Translated code"}}]
		return mock_response

	@patch("builtins.open", new_callable=MagicMock)  # Mock open
	@patch("code_mage.translator.Api")  # Mock Api class
	@patch.object(Translator, "_Translator__get_output_filename", return_value="translated_test.py")
	def test_translate(self, mock_get_output_filename, MockApi, mock_open, mock_args, capsys):
		mock_config = {"api_key": "fake_api_key"}

		# Initialize Translator instance
		translator = Translator(mock_args, mock_config)

		mock_file = MagicMock()
		mock_open.return_value = mock_file

		# Mock the Api's call_api method
		mock_api_instance = MagicMock()
		MockApi.return_value = mock_api_instance
		mock_api_instance.chat.completions.create = MagicMock(return_value=self.mock_api_call())

		translator.translate("./example/test.js")

		assert mock_api_instance.chat.completions.create.return_value.choices == [
			{"message": {"content": "Translated code"}}
		]

		captured = capsys.readouterr().out
		assert "\n************ END ************\n" in captured
