from enum import auto, StrEnum
from warnings import warn

MAX_QUOTE_LENGTH = 50


# The two classes below are available for you to use
# You do not need to implement them
class VariantMode(StrEnum):
    NORMAL = auto()
    UWU = auto()
    PIGLATIN = auto()


class DuplicateError(Exception):
    """Error raised when there is an attempt to add a duplicate entry to a database"""


# Implement the class and function below
class Quote:
    def __init__(self, quote: str, mode: "VariantMode") -> None:
        if len(quote) > MAX_QUOTE_LENGTH:
            ValueError("Quote is too long")
        self.quote = quote
        self.mode = mode
        self._create_variant()

    def __str__(self) -> str:
        return self.quote

    def _create_variant(self) -> str:
        """
        Transforms the quote to the appropriate variant indicated by `self.mode` and returns the result
        """

        """
        Converts a given word into the pig latin equivalent
        """

        def piglatinify_word(word: str) -> str:
            vowels = ["a", "e", "i", "o", "u"]
            if word[0] in vowels:
                return f"{word}way"
            else:
                consonant_cluster_end = 0
                for idx, letter in enumerate(word):
                    if letter in vowels:
                        consonant_cluster_end = idx
                        break

                return f"{word[consonant_cluster_end:].lower}{word[:consonant_cluster_end].lower}ay"

        """
        Halfway converts a given quote into the uwu equivalent (just L/l and R/r to W/w)
        """

        def uwuify_Ls_and_Rs(quote: str) -> str:
            output_string = (
                quote.replace("L", "W")
                .replace("l", "w")
                .replace("R", "W")
                .replace("r", "w")
            )
            return output_string

        """
        Stutters all words in a quote that start with U/u to U/u-U/u
        """

        def uwuify_U_stutter(quote: str) -> str:
            def stutter(word):
                if word.startswith(("u", "U")):
                    return word[0] + "-" + word
                return word

            words = quote.split()
            stuttered_words = [stutter(word) for word in words]
            return " ".join(stuttered_words)

        match self.mode:
            case VariantMode.NORMAL:
                pass
            case VariantMode.UWU:
                Rs_and_Ls = uwuify_Ls_and_Rs(self.quote)
                if len(Rs_and_Ls) > MAX_QUOTE_LENGTH:
                    raise ValueError("Quote is too long")

                result = uwuify_U_stutter(Rs_and_Ls)
                if len(result) > MAX_QUOTE_LENGTH:
                    warn("Quote too long, only partially transformed")
                    self.quote = Rs_and_Ls
                else:
                    self.quote = result
            case VariantMode.PIGLATIN:
                result = " ".join(
                    piglatinify_word(word) for word in self.quote.split()
                )

                result = result[0].upper() + result[1:]

                if len(result) > MAX_QUOTE_LENGTH:
                    raise ValueError("Quote was not modified")
                else:
                    self.quote = result

        return str(self)


def run_command(command: str) -> None:
    """
    Will be given a command from a user. The command will be parsed and executed appropriately.

    Current supported commands:
        - `quote` - creates and adds a new quote
        - `quote uwu` - uwu-ifys the new quote and then adds it
        - `quote piglatin` - piglatin-ifys the new quote and then adds it
        - `quote list` - print a formatted string that lists the current
           quotes to be displayed in discord flavored markdown
    """

    command = command.replace("“", '"').replace("”", '"')

    if command == "quote list":
        for quote in Database.quotes:
            print(f"- {str(quote)}")
        return

    # separates quote from rest of command
    command_and_quote = command.split('"')

    if len(command_and_quote) < 2:
        raise ValueError("Invalid command")

    quote = command_and_quote[1].strip()

    split_command = command_and_quote[0].split()
    num_tokens = len(split_command)

    if num_tokens == 1:
        variant = ""
    elif num_tokens == 2:
        variant = split_command[1].strip()
    else:
        raise ValueError("Invalid command")

    action_string = split_command[0].strip()

    if action_string != "quote":
        raise ValueError("Invalid command")

    print(len(quote))
    if len(quote) >= MAX_QUOTE_LENGTH:
        ValueError("Quote is too long")

    match variant:
        case "":
            quote_object = Quote(quote, VariantMode.NORMAL)
        case "uwu":
            quote_object = Quote(quote, VariantMode.UWU)
        case "piglatin":
            quote_object = Quote(quote, VariantMode.PIGLATIN)
        case _:
            raise ValueError("Invalid command")

    try:
        Database.add_quote(quote_object)
    except DuplicateError:
        print("Quote has already been added previously")


# The code below is available for you to use
# You do not need to implement it, you can assume it will work as specified
class Database:
    quotes: list["Quote"] = []

    @classmethod
    def get_quotes(cls) -> list[str]:
        "Returns current quotes in a list"
        return [str(quote) for quote in cls.quotes]

    @classmethod
    def add_quote(cls, quote: "Quote") -> None:
        "Adds a quote. Will raise a `DuplicateError` if an error occurs."
        if str(quote) in [str(quote) for quote in cls.quotes]:
            raise DuplicateError
        cls.quotes.append(quote)
