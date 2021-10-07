import logging

from thelovegeometry import get_input_file_from_cli_and_validate
from thelovegeometry.love_story_semantic_validator import LoveStorySemanticValidator
from thelovegeometry.parser_executor import parse_input
from thelovegeometry.love_story_language_parser_template import LoveStoryLanguageParserTemplate


def debug_prints(parsed_story: LoveStoryLanguageParserTemplate):
    # DEBUG only >
    logging.debug(f"Parsed text dict: {parsed_story.__dict__()}")
    logging.debug(f"Parsed text: {parsed_story}")
    for element in parsed_story:
        logging.debug(f"parsed line: {element}")
    # <


def main():
    input_file = get_input_file_from_cli_and_validate()

    logging.info("Init done of the application")
    logging.debug(input_file)
    parsed_story = parse_input(input_file)
    
    logging.info("Validate Story of Love")
    validate_and_print_error_messages_of_love_statements(parsed_story)
    logging.info("Validation is done")
    
    # debug_prints(parsed_story)

    logging.info("Exit from the application")


def validate_and_print_error_messages_of_love_statements(parsed_story):
    for broken_love_states in LoveStorySemanticValidator(parsed_story).validate_and_get_brokens():
        love_states = broken_love_states[0]
        messages = broken_love_states[1]
        logging.info("*" * 50)
        logging.info(f"Love of States: {love_states.__str__()}")
        logging.info("*" * 50)
        logging.info("Error messages:")
        for message in messages:
            logging.info(f"{message}")
        logging.info("*" * 50 + "\n")


if __name__ == "__main__":
    main()
