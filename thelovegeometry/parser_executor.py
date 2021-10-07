import logging
import pathlib
from typing import TextIO

from pypeg2 import parse

from thelovegeometry import PARSE_STORY_AT_ONCE
from thelovegeometry.love_story_language_parser_template import LoveStoryLanguageParserTemplate, LoveStatesSeparator


def parse_input(input_file: pathlib.Path) -> LoveStoryLanguageParserTemplate:
    with open(input_file, "r") as f:
        if PARSE_STORY_AT_ONCE:
            parsed = parse_input_by(f)
        else:
            parse_input_preseparated_by_sentence(f)

    logging.info("Parse of the input is ready")
    return parsed


def parse_input_by(file: TextIO):
    text = file.read()
    return parse_input_text(text)


def parse_input_text(input_text) -> LoveStoryLanguageParserTemplate:
    story = parse(input_text, LoveStoryLanguageParserTemplate)
    return story


###################
# Parse by sentence

def parse_sentence(sentence: str):
    logging.debug(f"Sentenece to be parsed: {sentence}")
    story = parse(sentence, LoveStoryLanguageParserTemplate)
    for element in story:
        logging.debug(f"parsed line: {element}")


def parse_input_preseparated_by_sentence(f):
    """
    For this function I think as the long-term solution.
    The why is easy: while reading the whole file is cool and stuff, could happen that is too huge to be parsed at once in real world scenarios.

    :param f: IO file
    :return:
    """
    sentence = ''
    for line in f:
        if LoveStatesSeparator.grammar in line[-2:]:
            sentence += line
            parse_sentence(sentence)
            sentence = ''
        else:
            sentence += line
