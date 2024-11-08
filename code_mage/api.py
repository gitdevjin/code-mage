import os
import sys
from openai import OpenAI


class Api:
	def __init__(self, model, config):
		self.supported_model = ["groq", "openrouter"]
		self.model = model if model is not None else "openrouter"

		if self.model not in self.supported_model:
			sys.exit(f"{self.model} is not suppored. Model Supported: {self.supported_model}")

		# default api_url and api_model
		self.api_url = "https://openrouter.ai/api/v1"
		self.api_model = "sao10k/l3-euryale-70b"
		self.api_key = os.getenv("OPENROUTER_API_KEY") or config.get("OPENROUTER_API_KEY")

		# api_url and api_model when the provider is groq
		if self.model == "groq":
			self.api_url = "https://api.groq.com/openai/v1"
			self.api_model = "llama3-8b-8192"
			self.api_key = os.getenv("GROQ_API_KEY") or config.get("GROQ_API_KEY")

	def call_api(self, target_lang, code, stream_flag=False):
		client = OpenAI(
			base_url=self.api_url,
			api_key=self.api_key,
		)

		completion = client.chat.completions.create(
			extra_headers={},
			model=self.api_model,
			messages=[
				{
					"role": "system",
					"content": "only display the code without any explanation",
				},
				{
					"role": "user",
					"content": f"translate this to {target_lang} language: {code}",
				},
			],
			stream=stream_flag,
		)

		return completion
