#!/usr/bin/env python3

import argparse
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def main():

    parser = argparse.ArgumentParser(description="Translate a source file into another programming language.")
    
    # Arguments
    parser.add_argument('source_file', help="The path to the source file to translate.")

    # Options
    parser.add_argument('--target', '-t', help='The language to translate the source files into', required=True)
    parser.add_argument('--output', '-o', help="Specify the output file name(without extension)")
    
    args = parser.parse_args()
    
    print("Source-file: " + args.source_file)
    print("Target Option: " + args.target)
    #print("Output Option: " + args.output)

    with open(args.source_file, 'r') as src:
        code = src.read()
    
    print("Print: ")
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
            {"role": "system", "content": "only display the code"},
            {"role": "user", "content": f"translate this to python language: {code}"},
        ],
    )
    output = completion.choices[0].message.content
    
    print(output) # for check the content

    default_output_file = f"translated_{os.path.basename(args.source_file)}"
    
    output_file = f"translated_{os.path.basename(args.source_file)}"
    with open(output_file, 'w') as f:
        f.write(output)

if __name__ == "__main__":
    main()
