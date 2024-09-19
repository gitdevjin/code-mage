import os
import sys
from openai import OpenAI
from dotenv import load_dotenv


def translate(source_file, args, num=""):
    load_dotenv()

    # Get arguments
    language = args.language
    output = args.output
    token_flag = args.token_usage
    
    original_file_name = os.path.splitext(os.path.basename(source_file))[0]
    original_file_ext = os.path.splitext(os.path.basename(source_file))[1]

    output_file_ext = ".py"
    
    source_lang = "none"

    if original_file_ext == ".js":
        source_lang = "javascript"
    elif original_file_ext == ".py":
        source_lang = "python"
    elif original_file_ext == ".cpp":
        source_lang = "c++"
    elif original_file_ext == ".java":
        source_lang = "java"

    supported_lang = ["javascript", "python", "c++", "java"]

    target_lang = language

    if target_lang is None:
        target_lang = "python"
    elif target_lang not in supported_lang:
        sys.exit("the target language is not supported")
        
    if source_lang == target_lang:
        sys.exit("the target language is the same with the source_file")
    elif source_lang == "none":
        sys.exit("the file is not a supported programming language")

    if target_lang == "javascript":
        output_file_ext = ".js"
    elif target_lang == "python":
        output_file_ext = ".py"
    elif target_lang == "c++":
        output_file_ext = ".cpp"
    elif target_lang == "java":
        output_file_ext = ".java"


    with open(source_file, 'r') as src:
        code = src.read()

    # gets API Key from environment variable OPENAI_API_KEY
    api_key = os.getenv("OPENROUTER_API_KEY")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    completion = client.chat.completions.create(
        extra_headers={
        },
        model="sao10k/l3-euryale-70b",
        messages=[
            {"role": "system", "content": "only display the code without any explanation"},
            {"role": "user", "content": f"translate this to {target_lang} language: {code}"},
        ],
    )

    result = completion.choices[0].message.content

    output_file = f"translated_{original_file_name}{output_file_ext}"
    if output:
        output_file = output + str(num) + output_file_ext
        
    with open(output_file, 'w') as f:
        f.write(result)


    # prints token usage information if --token-usage/-t flag is present
    if token_flag:
        if completion.usage.completion_tokens_details:
            prompt_tokens = completion.usage.prompt_tokens
            completion_tokens = completion.usage.completion_tokens
            total_tokens = completion.usage.total_tokens

            print(f"prompt tokens: {prompt_tokens}", file=sys.stderr)
            print(f"completion tokens: {completion_tokens}", file=sys.stderr)
            print(f"total tokens: {total_tokens}", file=sys.stderr)
        else:
            print("Sorry, this model doesn't give token usage details", file=sys.stderr)
        
