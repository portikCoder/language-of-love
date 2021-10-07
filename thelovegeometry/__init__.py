import argparse
import logging
import pathlib

from thelovegeometry.utils.storage_operator import create_dir_if_needed, validate_input_file

PARSE_STORY_AT_ONCE = True


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s:%(levelname)s:%(message)s',
    )
    logging.info('Logger setup is done')


def get_input_file_from_cli() -> pathlib.Path:
    parser = argparse.ArgumentParser(
        description="The tool is able to parse LOVE stories full of drama, based on the PyPeg2 module",
        prog=f"python -m {__package__}"
    )

    parser.add_argument(
        "-f",
        "--file",
        type=pathlib.Path,
        help="path to the input file"
    )
    args = parser.parse_args()
    return args.file


def get_input_file_from_cli_and_validate() -> pathlib.Path:
    input_file = get_input_file_from_cli()
    validate_input_file(input_file)
    return input_file


# It is being used this way, so therefore the logger gets initialized implicitly, as I don't wanna care of it
setup_logging()
