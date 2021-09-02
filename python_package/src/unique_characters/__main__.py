from .util import find_unique_characters
import _io
import argparse


def _print_result(input_string: str):
    characters = find_unique_characters(input_string)
    characters_str = ", ".join(characters) if characters else "No characters"
    characters_str += " is" if len(characters) == 1 else " are"
    print(f'"{input_string}" => {len(characters)}\n{characters_str} present once.')


def main():
    parser = argparse.ArgumentParser(description="Show unique characters in the string and their number")
    parser.add_argument('--file', type=argparse.FileType('r'), help='Read input_sring string from given file')
    parser.add_argument('--string', help='proceed given string')
    args = parser.parse_args()
    if isinstance(args.file, _io.TextIOWrapper):
        _print_result(args.file.read())
    elif isinstance(args.string, str):
        _print_result(args.string)


if __name__ == '__main__':
    main()
