import os
import sys
from .api import Api


class Translator:
	def __init__(self, args, config):
		self.supported_lang = ["javascript", "python", "c++", "java"]
		self.target_lang = "python"
		self.source_lang = "none"
		self.config = config
		self.args = args

		# Decide and Validify Target language into which the source file is translated
		if self.args.language is not None:
			self.target_lang = self.args.language

		if self.target_lang not in self.supported_lang:
			sys.exit(f"{self.target_lang} is not supported target language")

	def translate(self, source_file, file_num=""):
		# Extracting Original file name and extension
		original_file_name = os.path.splitext(os.path.basename(source_file))[0]
		original_file_ext = os.path.splitext(os.path.basename(source_file))[1]

		# Decide and Validify Input File Language
		self.source_lang = self.__get_source_lang(original_file_ext)

		if self.source_lang == self.target_lang:
			sys.exit("the target language is the same with the source_file")
		elif self.source_lang == "none":
			sys.exit("the file is not written in a supported programming language")

		# Decide output file name
		output_file_name = self.__get_output_filename(original_file_name, file_num)

		# Read file
		with open(source_file, "r") as src:
			code = src.read()

		# Create Api Class
		llm_api = Api(self.args.model, self.config)

		# Stream out the result
		if self.args.stream:
			completion = llm_api.call_api(self.target_lang, code, self.args.stream)

			for chunk in completion:
				if chunk.choices[0].delta.content is not None:
					print(chunk.choices[0].delta.content, end="")

			sys.stdout.flush()

			if self.args.token_usage is not False:
				sys.stderr.write("\nStream Flag Doesn't Support Token-Usage Option")

			print("\n************ END ************\n")
		else:  # File Output
			completion = llm_api.call_api(self.target_lang, code, self.args.stream)

			result = completion.choices[0].message.content

			with open(output_file_name, "w") as f:
				f.write(result)

			# prints token usage info if --token-usage/-t flag is present
			if self.args.token_usage and self.args.model != "openrouter":
				prompt_tokens = completion.usage.prompt_tokens
				completion_tokens = completion.usage.completion_tokens
				total_tokens = completion.usage.total_tokens

				sys.stderr.write(f"prompt tokens: {prompt_tokens}\n")
				sys.stderr.write(f"completion tokens: {completion_tokens}\n")
				sys.stderr.write(f"total tokens: {total_tokens}\n")
			elif self.args.token_usage and self.args.model == "openrouter":
				sys.stderr.write("Sorry, this model doesn't provide token usage details\n")

	def __get_output_filename(self, origin_file_name, file_number):
		output_file_ext = self.__get_output_ext(self.target_lang)
		output_file_name = f"translated_{origin_file_name}{output_file_ext}"

		if self.args.output:
			output_file_name = self.args.output + str(file_number) + output_file_ext

		return output_file_name

	def __get_source_lang(self, extension):
		src_lang = "none"
		if extension == ".js":
			src_lang = "javascript"
		elif extension == ".py":
			src_lang = "python"
		elif extension == ".cpp":
			src_lang = "c++"
		elif extension == ".java":
			src_lang = "java"

		return src_lang

	def __get_output_ext(self, language):
		# Decide output file extension.
		if language == "javascript":
			output_ext = ".js"
		elif language == "python":
			output_ext = ".py"
		elif language == "c++":
			output_ext = ".cpp"
		elif language == "java":
			output_ext = ".java"

		return output_ext
