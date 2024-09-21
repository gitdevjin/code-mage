#!/usr/bin/env python3

import argparse
import os
import sys
from dotenv import load_dotenv
from .translator import translate

def main():
    VERSION = "release 0.1"

    parser = argparse.ArgumentParser(description="This Tool translates a source file into another programming language.")
    
    # Arguments
    parser.add_argument('source_files', nargs='*', help="The path to the source file to translate.")

    # Options
    parser.add_argument('--language', '-l', help='The language to translate the source files into')
    parser.add_argument('--output', '-o', help="Specify the output file name(without extension)")
    parser.add_argument('--version', '-v', action='version', version=f'CodeMage {VERSION}', help="Show program's version number and exit")
    parser.add_argument('--token-usage', '-t', action='store_true', help='Get information about token usage for the prompt and response')
    parser.add_argument('--model', '-m', help="Specify the LLM API model name")
    
    args = parser.parse_args()

    if not args.source_files:
        sys.exit("Welcome To CodeMage!\nIf you need a Help? Type the fllowing:\npoetry run codemage -h")

    for index, file in enumerate(args.source_files):
        translate(file, args, index + 1)


if __name__ == "__main__":
    main()
