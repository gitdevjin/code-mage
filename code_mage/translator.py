import os
from openai import OpenAI
from dotenv import load_dotenv


def translate(source_file, target=None, output=None, num=""):
    load_dotenv()
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

    target_lang = target

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

    print("Source-file: " + original_file_name)

    with open(source_file, 'r') as src:
        code = src.read()
    
    print(code);


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
    print(result) # stdout

    output_file = f"translated_{original_file_name}{output_file_ext}"
    if output:
        output_file = output + str(num) + output_file_ext
        
    with open(output_file, 'w') as f:
        f.write(result)