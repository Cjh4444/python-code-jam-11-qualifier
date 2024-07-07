command = 'quote uwu "Hello, it is I"'

quote_command, quote, empty = command.split('"')

variant = quote_command[:4]
print(variant)


def piglatinify_word(word: str):
    vowels = ["a", "e", "i", "o", "u"]
    if word[0] in vowels:
        return f"{word}way"
    else:
        consonant_cluster_end = 0
        for idx, letter in enumerate(word):
            if letter in vowels:
                consonant_cluster_end = idx
                break

        return (
            f"{word[consonant_cluster_end:]}{word[:consonant_cluster_end]}ay"
        )


def uwuify_Ls_and_Rs(quote: str) -> str:
    output_string = (
        quote.replace("L", "W")
        .replace("l", "w")
        .replace("R", "W")
        .replace("r", "w")
    )
    return output_string


def uwuify_U_stutter(quote: str) -> str:
    def stutter(word):
        if word.startswith(("u", "U")):
            return word[0] + "-" + word
        return word

    words = quote.split()

    words = quote.split()
    stuttered_words = [stutter(word) for word in words]
    return " ".join(stuttered_words)


assert piglatinify_word("pig") == "igpay"
assert piglatinify_word("latin") == "atinlay"
assert piglatinify_word("friends") == "iendsfray"
assert piglatinify_word("eat") == "eatway"

quote = "You have no right to call yourself creative until you look at a trowel and think that it would make a great lockpick."
halfway = uwuify_Ls_and_Rs(quote)
assert (
    uwuify_U_stutter(halfway)
    == "You have no wight to caww youwsewf cweative u-untiw you wook at a twowew and think that it wouwd make a gweat wockpick."
)

quote_test = '"hello, my name is blah blah"'
print(quote_test[1 : len(quote_test) - 1])
