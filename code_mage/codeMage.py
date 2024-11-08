#!/usr/bin/env python3

import sys
from .translator import Translator
from .loadConfig import load_config
from .argsParser import arg_parser


def main():
	# Load config file
	config = load_config()

	args = arg_parser(config)

	if not args.source_files:
		sys.exit(
			"Welcome To CodeMage!\nIf you need a Help, Type the fllowing command:\npoetry run codemage -h"
		)

	translator = Translator(args, config)

	for index, file in enumerate(args.source_files):
		print(file)
		translator.translate(file, index + 1)


if __name__ == "__main__":
	main()
