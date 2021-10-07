import collections
import typing

from pypeg2 import Keyword, K, List, Enum, attr, maybe_some, csl, Namespace, optional, name


class Name(str):
    grammar = name()


class Feeling(Keyword):
    grammar = Enum(K("loves"), K("hates"))


class LoveState:
    grammar = attr("who", Name), attr("feeling", Feeling), attr("whom", Name)

    # persist dynamic attributes from above
    who: attr
    feeling: attr
    whom: attr

    def __str__(self) -> str:
        return f"{self.who.name} {self.feeling.name} {self.whom.name}"

    def __dict__(self) -> dict:
        return {
            self.who.name: {self.feeling.name: self.whom.name}
        }


class LoveStateConjunctive(Keyword):
    grammar = Enum(K("and"), K("but"), K("while"))


class LoveStates(Namespace):
    grammar = maybe_some(csl(LoveState), optional(LoveStateConjunctive)),

    def __str__(self):
        return " | ".join([str(x) for x in self.data.values()])

    def __dict__(self) -> dict:
        """Merge multiple love statements into one by using 'for' loop for being convenient"""

        love_states = [x.__dict__() for x in self.values() if isinstance(x, LoveState)]

        result = collections.defaultdict(lambda: collections.defaultdict(list))
        for love_state in love_states:
            for who, loves_whom in love_state.items():
                for loves, whom in loves_whom.items():
                    result[who][loves].append(whom)

        return result
        # return {k: v for elem_dict in [x.__dict__() for x in self.values() if isinstance(x, LoveStatement)] for k, v in
        #         elem_dict.items()}


class LoveStatesSeparator:
    grammar = "."


class LoveStoryLanguageParserTemplate(List):
    grammar = maybe_some(LoveStates, ".")

    def __str__(self) -> str:
        """ As because the f-string does not allow backslashes:
        >>> chr(10)
        \n"""
        return f"{chr(10).join([str(x) for x in self])}"

    def __dict__(self) -> typing.List[dict]:
        return [x.__dict__() for x in self]
