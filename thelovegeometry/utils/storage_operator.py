import logging
import pathlib


def create_dir_if_needed(directory_path: pathlib.Path):
    if not directory_path:
        raise ValueError(f"The input for the directory creation should not be empty!")

    pathlib.Path(directory_path).mkdir(parents=True, exist_ok=True)  # avoid errors if the path does exist


def validate_input_file(input_file: pathlib.Path):
    if not input_file or not pathlib.Path(input_file).is_file():
        raise ValueError(f"There is no such input file like '{input_file}'!")
    try:
        open(input_file, 'r')
    except Exception as e:
        raise ValueError(f"Could not open input file: '{input_file}'. Reason: {e}")

    logging.info("Input file validation is done successfully, and there were no errors")