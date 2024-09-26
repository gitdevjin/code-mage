import os
import sys
from openai import OpenAI
from dotenv import load_dotenv
from groq import Groq


def translate(source_file, args, num=""):
    load_dotenv()

    supported_lang = ["javascript", "python", "c++", "java"]

    # Get arguments
    target_lang = args.language
    output = args.output
    token_flag = args.token_usage
    source_lang = "none"
    
    # Extracting Original file name and extension
    original_file_name = os.path.splitext(os.path.basename(source_file))[0]
    original_file_ext = os.path.splitext(os.path.basename(source_file))[1]

    # Validify and Set Default traget_lang
    if target_lang is None:
        target_lang = "python"
    elif target_lang not in supported_lang:
        sys.exit("the target language is not supported")

    # Default target_lang and extension is python
    output_file_ext = ".py"

    # Decide output file extension.
    if target_lang == "javascript":
        output_file_ext = ".js"
    elif target_lang == "python":
        output_file_ext = ".py"
    elif target_lang == "c++":
        output_file_ext = ".cpp"
    elif target_lang == "java":
        output_file_ext = ".java"
    
    # Check source_lang
    if original_file_ext == ".js":
        source_lang = "javascript"
    elif original_file_ext == ".py":
        source_lang = "python"
    elif original_file_ext == ".cpp":
        source_lang = "c++"
    elif original_file_ext == ".java":
        source_lang = "java"

    # Validify source_lang
    if source_lang == target_lang:
        sys.exit("the target language is the same with the source_file")
    elif source_lang == "none":
        sys.exit("the file is not a supported programming language")

    
    output_file_name = f"translated_{original_file_name}{output_file_ext}"
    if output:
        output_file_name = output + str(num) + output_file_ext

    with open(source_file, 'r') as src:
        code = src.read()


    completion = None
    #******************** Stream out the result ******************** #
    if args.stream:
        if args.model == "groq":
            client = Groq(
                api_key=os.getenv("GROQ_API_KEY"),
            )
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "only display the code without any explanation"},
                    {"role": "user", "content": f"translate this to {target_lang} language: {code}"},
                ],
                model="llama3-8b-8192",
                stream=True,
            )
        elif args.model == "openrouter" or args.model is None:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPENROUTER_API_KEY"),
            )

            completion = client.chat.completions.create(
                extra_headers={
                    },
                model="sao10k/l3-euryale-70b",
                messages=[
                    {"role": "system", "content": "only display the code without any explanation"},
                    {"role": "user", "content": f"translate this to {target_lang} language: {code}"},
                ],
                stream=True,
            )
        else:
            sys.stderr.write("Not Supported Model")
            sys.stderr.write("Supported Model: openrouter, groq")

        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")

        sys.exit(0) # EXIT with success status
    # ******************** *************** **************************** #

    if args.model == "groq":
        print("groq")
        client = Groq(
            api_key=os.getenv("GROQ_API_KEY"),
        )

        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "only display the code without any explanation"},
                {"role": "user", "content": f"translate this to {target_lang} language: {code}"},
            ],
            model="llama3-8b-8192",
        )
    elif args.model == "openrouter" or args.model is None:
        print("openrouter")
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
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
    else:
        sys.stderr.write("Not Supported Model")
        sys.stderr.write("Supported Model: openrouter, groq")
    
    result = completion.choices[0].message.content
        
    with open(output_file_name, 'w') as f:
        f.write(result)


    # prints token usage information if --token-usage/-t flag is present
    if token_flag and args.model != "openrouter":
        prompt_tokens = completion.usage.prompt_tokens
        completion_tokens = completion.usage.completion_tokens
        total_tokens = completion.usage.total_tokens

        sys.stderr.write(f"prompt tokens: {prompt_tokens}\n")
        sys.stderr.write(f"completion tokens: {completion_tokens}\n")
        sys.stderr.write(f"total tokens: {total_tokens}\n")
    else:
        sys.stderr.write("Sorry, this model doesn't provide token usage details\n")
        
