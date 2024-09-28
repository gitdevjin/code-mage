import os
import sys
from dotenv import load_dotenv
from .api import call_api


def translate(source_file, args, num=""):
    load_dotenv()

    supported_lang = ["javascript", "python", "c++", "java"]

     # Extracting Original file name and extension
    original_file_name = os.path.splitext(os.path.basename(source_file))[0]
    original_file_ext = os.path.splitext(os.path.basename(source_file))[1]


    # Decide and Validify Target language into which the source file is translated
    target_lang = args.language if args.language is not None else "python"
    if target_lang not in supported_lang:
        sys.exit("the target language is not supported")


    # Decide and Validify Input File Language
    source_lang = get_source_lang(original_file_ext)
    if source_lang == target_lang:
        sys.exit("the target language is the same with the source_file")
    elif source_lang == "none":
        sys.exit("the file is not a supported programming language")
    

    # Decide output file name
    output_file_ext = get_output_ext(target_lang)
    output_file_name = f"translated_{original_file_name}{output_file_ext}"
    
    if args.output:
        output_file_name = args.output + str(num) + output_file_ext

    # Read file
    with open(source_file, 'r') as src:
        code = src.read()


    # Stream out the result
    if args.stream:
        completion = call_api(args.model, target_lang, code, args.stream)

        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")

        sys.stdout.flush()

        if args.token_usage is not False:
            sys.stderr.write("\nStream Flag Doesn't Support Token-Usage Option")
        
        print("\n************ END ************\n");
    else: # File Output
    
        completion = call_api(args.model, target_lang, code, args.stream)

        result = completion.choices[0].message.content

        with open(output_file_name, 'w') as f:
            f.write(result)

        # prints token usage info if --token-usage/-t flag is present
        if args.token_usage and args.model != "openrouter":
            prompt_tokens = completion.usage.prompt_tokens
            completion_tokens = completion.usage.completion_tokens
            total_tokens = completion.usage.total_tokens

            sys.stderr.write(f"prompt tokens: {prompt_tokens}\n")
            sys.stderr.write(f"completion tokens: {completion_tokens}\n")
            sys.stderr.write(f"total tokens: {total_tokens}\n")
        elif args.token_usage and args.model == "openrouter":
            sys.stderr.write("Sorry, this model doesn't provide token usage details\n")
        

def get_source_lang(extension):
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


def get_output_ext(language):
     # Default target_lang and extension is python
    output_ext = ".py"

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


    
        
