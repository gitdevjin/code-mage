import pytest
from unittest.mock import patch, MagicMock
import os
from code_mage.api import Api


class TestApiConstructor:
	@pytest.fixture
	def mock_config(self):
		return {"OPENROUTER_API_KEY": "fake_api_key_from_toml"}

	def test_constructor_with_openrouter_and_config(self, mock_config, monkeypatch):
		# This overwirtes only the specified key-value pair.
		monkeypatch.setenv("OPENROUTER_API_KEY", "")

		api = Api(model="openrouter", config=mock_config)

		assert api.model == "openrouter"
		assert api.api_model == "sao10k/l3-euryale-70b"
		assert api.api_url == "https://openrouter.ai/api/v1"
		assert api.api_key == "fake_api_key_from_toml"
		assert api.supported_model == ["groq", "openrouter"]

	def test_constructor_with_groq_and_env(self, mock_config, monkeypatch):
		# Mock the environment variable for OPENROUTER_API_KEY
		monkeypatch.setenv("GROQ_API_KEY", "fake_api_key_from_env")

		api = Api(model="groq", config=mock_config)

		assert api.model == "groq"
		assert api.api_model == "llama3-8b-8192"
		assert api.api_url == "https://api.groq.com/openai/v1"
		assert api.api_key == "fake_api_key_from_env"
		assert api.supported_model == ["groq", "openrouter"]

	def test_constructor_with_unsupported_model(self, mock_config, monkeypatch):
		monkeypatch.setenv("GROQ_API_KEY", "fake_api_key_from_env")

		with pytest.raises(SystemExit) as exc_info:
			api = Api(model="unsupported_model", config=mock_config)  # noqa

		assert (
			str(exc_info.value)
			== "unsupported_model is not suppored. Model Supported: ['groq', 'openrouter']"
		)


class TestApiWithEnv:
	@pytest.fixture
	def mock_config(self):
		return {
			"OPENROUTER_API_KEY": "fake_openrouter_api_key_from_toml",
			"GROQ_API_KEY": "fake_groq_api_key",
		}

	# Mock OpenAI response
	def mock_api_call(self, *args, **kwargs):
		# Return a mock response object with a `choices` attribute
		mock_response = MagicMock()
		mock_response.choices = [{"message": {"content": "Translated code"}}]
		return mock_response

	# Test when model is supported
	@patch.dict(
		os.environ,
		{
			"OPENROUTER_API_KEY": "fake_api_key_from_env",
			"GROQ_API_KEY": "fake_groq_api_key_from_env",
		},
	)
	@patch("code_mage.api.OpenAI")
	def test_api_with_openrouter(self, mock_openai_class):
		# Mock the OpenAI client and its methods
		mock_client = MagicMock()

		# When the code create OpenAI class inside call_api(), it's replaced by mock_openai_class
		mock_openai_class.return_value = mock_client
		mock_client.chat.completions.create = MagicMock(return_value=self.mock_api_call())

		# Create an instance of the Api with a supported model
		api = Api(model="openrouter", config={})

		# Simulate an API call
		response = api.call_api(target_lang="python", code="some_code")

		# Check if the API call was made with the expected arguments
		mock_client.chat.completions.create.assert_called_once_with(
			extra_headers={},
			model="sao10k/l3-euryale-70b",
			messages=[
				{"role": "system", "content": "only display the code without any explanation"},
				{"role": "user", "content": "translate this to python language: some_code"},
			],
			stream=False,
		)

		# Assert the response content
		assert response.choices[0]["message"]["content"] == "Translated code"

	@patch.dict(
		os.environ,
		{
			"OPENROUTER_API_KEY": "fake_api_key_from_env",
			"GROQ_API_KEY": "fake_groq_api_key_from_env",
		},
	)
	@patch("code_mage.api.OpenAI")
	def test_api_with_groq(self, mock_openai_class):
		# Mock the OpenAI client and its methods
		mock_client = MagicMock()

		# When the code create OpenAI class inside call_api(), it's replaced by mock_openai_class
		mock_openai_class.return_value = mock_client
		mock_client.chat.completions.create = MagicMock(return_value=self.mock_api_call())

		# Create an instance of the Api with a supported model
		api = Api(model="groq", config={})

		# Simulate an API call
		response = api.call_api(target_lang="python", code="some_code")

		# Check if the API call was made with the expected arguments
		mock_client.chat.completions.create.assert_called_once_with(
			extra_headers={},
			model="llama3-8b-8192",
			messages=[
				{"role": "system", "content": "only display the code without any explanation"},
				{"role": "user", "content": "translate this to python language: some_code"},
			],
			stream=False,
		)

		assert api.api_url == "https://api.groq.com/openai/v1"
		assert api.api_key == "fake_groq_api_key_from_env"

		# Assert the response content
		assert response.choices[0]["message"]["content"] == "Translated code"
