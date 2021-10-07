import logging
from unittest import mock

import pytest
from pypeg2 import parse

from thelovegeometry import get_input_file_from_cli_and_validate
from thelovegeometry.love_story_language_parser_template import LoveStoryLanguageParserTemplate


def test_one_feels_love_for_one():
    story = parse("A loves B.", LoveStoryLanguageParserTemplate)

    result = [{"A": {"loves": ["B"]}}]

    assert story.__dict__() == result


def test_one_feels_love_and_hatred_for_one():
    story = parse("A loves B but A hates B.", LoveStoryLanguageParserTemplate)

    result = [{"A": {"loves": ["B"], "hates": ["B"]}}]

    assert story.__dict__() == result


def test_multiple_feels_love_for_one_or_multiple_separated_by_comma():
    story = parse("A loves B, B loves A and B loves D.", LoveStoryLanguageParserTemplate)

    result = [{"A": {"loves": ["B"]},
               "B": {"loves": ["A", "D"]}}]

    assert story.__dict__() == result


def test_multiple_feels_love_for_multiple_duplicated_and_itself_separated_by_comma():
    story = parse("A loves B, A loves B and A loves A.", LoveStoryLanguageParserTemplate)

    result = [{"A": {"loves": ["B", "B", "A"]}}]

    assert story.__dict__() == result


def test_multiple_feels_love_and_hatred_for_one():
    story = parse("A hates B, A loves D while B loves C and D hates A.", LoveStoryLanguageParserTemplate)

    result = [{"A": {"hates": ["B"], "loves": ["D"]},
               "B": {"loves": ["C"]},
               "D": {"hates": ["A"]}}]

    assert story.__dict__() == result


def test_multiple_feels_love_or_hatred_for_multiple():
    story = parse("A loves B but B hates A and B hates D and A loves D.", LoveStoryLanguageParserTemplate)

    result = [{"A": {"loves": ["B", "D"]},
               "B": {"hates": ["A", "D"]}}]

    assert story.__dict__() == result


def test_multiple_feels_love_or_hatred_for_one_separated_by_newline():
    story = parse("A loves B but B hates A\nD loves B and C loves A.", LoveStoryLanguageParserTemplate)

    result = [{"A": {"loves": ["B"]},
               "B": {"hates": ["A"]},
               "D": {"loves": ["B"]},
               "C": {"loves": ["A"]}
               }]

    assert story.__dict__() == result


def test_fail_if_no_sentence_separator():
    with pytest.raises(SyntaxError) as e:
        parse("A loves B", LoveStoryLanguageParserTemplate)

    assert "expecting '.' (line 1)" in str(e.value)


def test_fail_if_unknown_conjunction():
    with pytest.raises(SyntaxError) as e:
        parse("A loves B haha B hates A.", LoveStoryLanguageParserTemplate)

    assert "expecting '.' (line 1)" in str(e.value)


def test_parse_love_story_from_cli_input():
    with mock.patch("sys.argv", [__file__, "-f", "input/thelovegeometry.input"]):
        input_file = get_input_file_from_cli_and_validate()

    with open(input_file, "r") as f:
        story = parse(f.read(), LoveStoryLanguageParserTemplate)
        for element in story:
            logging.debug(f"parsed line: {element}")

            assert element is not None

        assert story is not None
