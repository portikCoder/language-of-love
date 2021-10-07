from unittest import mock

from thelovegeometry import get_input_file_from_cli_and_validate
from thelovegeometry.parser_executor import parse_input


def test_parser_executor_love_story_from_cli_input():
    with mock.patch("sys.argv", [__file__, "-f", "input/thelovegeometry.input"]):
        input_file = get_input_file_from_cli_and_validate()

    story = parse_input(input_file)

    assert story is not None
    assert story[0] is not None
    assert list(story[0].values())[0].who.name == "A"
    assert list(story[0].values())[0].feeling == "loves"
    assert list(story[0].values())[0].whom.name == "B"
