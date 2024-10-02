#!/usr/bin/env python3

import argparse
import sys
from .translator import translate
from .loadConfig import load_config

def main():
    VERSION = "release 0.1"

    # Load config file
    config = load_config()

    parser = argparse.ArgumentParser(description="This Tool translates a source file into another programming language.")
    
    # Arguments
    parser.add_argument('source_files', nargs='*', help="The path to the source file to translate.")

    # Options
    parser.add_argument('--language', '-l', help='The language to translate the source files into', default=config.get('language'))
    parser.add_argument('--output', '-o', help="Specify the output file name(without extension)", default=config.get('output'))
    parser.add_argument('--version', '-v', action='version', version=f'CodeMage {VERSION}', help="Show program's version number and exit")
    parser.add_argument('--token-usage', '-t', action='store_true', help='Get information about token usage for the prompt and response', default=config.get('token_usage', False))
    parser.add_argument('--model', '-m', help="Specify the LLM API model name", default=config.get('model'))
    parser.add_argument('--stream', '-s', action='store_true', help='Stream out the output into stdout', default=config.get('stream', False))
    
    args = parser.parse_args()

    if not args.source_files:
        sys.exit("Welcome To CodeMage!\nIf you need a Help, Type the fllowing command:\npoetry run codemage -h")

    for index, file in enumerate(args.source_files):
        translate(file, args, index + 1)


if __name__ == "__main__":
    main()
