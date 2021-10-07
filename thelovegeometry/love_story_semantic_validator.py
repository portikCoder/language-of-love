from collections import Counter
from enum import Enum
from typing import List, Tuple

from thelovegeometry.love_story_language_parser_template import LoveStoryLanguageParserTemplate, LoveState

# should come from the templates
FEELS_LOVE = 'loves'
FEELS_HATRED = 'hates'

BrokenLoveStates = List[Tuple[LoveState, str]]


class LoveStorySemanticValidator:
    def __init__(self, parsed_love_story: LoveStoryLanguageParserTemplate):
        self.parsed_love_story = parsed_love_story

    def validate_and_get_brokens(self) -> List[BrokenLoveStates]:
        broken_love_states = []
        for love_states in self.parsed_love_story:
            error_messages = self._get_broken_love_states_messages(love_states)
            if error_messages:
                broken_love_states.append((love_states, error_messages))
        return broken_love_states

    def _get_broken_love_states_messages(self, love_states):
        """Good candidate to be a plugin-like method/class, to be extendable easily without modification of the actual code..."""

        if not love_states:
            return False

        broken_love_states: List[str] = []
        only_love_states = love_states.__dict__()
        for who, feels_what_to_whom in only_love_states.items():
            set_of_feels_LOVE_to_whom = set(feels_what_to_whom.get(FEELS_LOVE, ()))
            set_of_feels_HATRED_to_whom = set(feels_what_to_whom.get(FEELS_HATRED, ()))

            # 1. check for loving and hating at once the same person(s)
            result = self._check_for_loving_and_hating_at_once_the_same(set_of_feels_HATRED_to_whom,
                                                                        set_of_feels_LOVE_to_whom, who)
            if result:
                broken_love_states.append(result)

            # 2. check for loving (and|or) hating itself the person
            result = self._check_for_loving_hating_itself(feels_what_to_whom, set_of_feels_HATRED_to_whom,
                                                          set_of_feels_LOVE_to_whom, who)
            if result:
                broken_love_states.append(result)

            # 3. check for loving and/or hating somebody (even itself) multiple times
            result = self._check_for_loving_hating_multiple_times(feels_what_to_whom, who)
            if result:
                broken_love_states.append(result)

        return broken_love_states

    def _check_for_loving_hating_multiple_times(self, feels_what_to_whom, who):
        multiple_occurence_of_the_same_person = list(
            x[0].name for x in filter(lambda x: x[1] > 1, Counter(feels_what_to_whom.get(FEELS_LOVE, ())).items()))
        multiple_occurence_of_the_same_person.extend(
            list(
                x[0].name for x in
                filter(lambda x: x[1] > 1, Counter(feels_what_to_whom.get(FEELS_HATRED, ())).items()))
        )
        loves_or_hates_the_same_multiple_times = True if multiple_occurence_of_the_same_person else False
        if loves_or_hates_the_same_multiple_times:
            return f"[FEELING REPETITION] C'mon, you're better than this! Do not repeat yourself '{who}', we are getting bored of '{multiple_occurence_of_the_same_person}' and we do KNOW if you say it just once."

    def _check_for_loving_hating_itself(self, feels_what_to_whom, set_of_feels_HATRED_to_whom,
                                        set_of_feels_LOVE_to_whom, who):
        loves_or_hates_itself = set_of_feels_LOVE_to_whom.union(
            set_of_feels_HATRED_to_whom)
        if who in loves_or_hates_itself:
            feeling_felt = ''
            if who in feels_what_to_whom.get(FEELS_LOVE, ()):
                feeling_felt = FEELS_LOVE

            if who in feels_what_to_whom.get(FEELS_HATRED, ()):
                feeling_felt += " & " + FEELS_HATRED

            return f"[REFLEXIVE-FEELING] '{who}' {feeling_felt} itself, DON'T be that selfish! At the current situation one cannot do that with itself, anyhow and much it wants. :("

    def _check_for_loving_and_hating_at_once_the_same(self, set_of_feels_HATRED_to_whom,
                                                      set_of_feels_LOVE_to_whom, who):
        loves_and_hates_at_once = set_of_feels_LOVE_to_whom.intersection(
            set_of_feels_HATRED_to_whom)
        if loves_and_hates_at_once:
            return f"[LOVE&HATE THE SAME TIME] '{who}' {FEELS_LOVE} & {FEELS_HATRED} at the same time for the same person(s) '{[x.name for x in loves_and_hates_at_once]}', which is not possible in this implementation!"
