from typing import List

# We move the cost value to be able to set them as config or to modify them easily
# in the future
COST_PARAMETERS_CENTS = {
    "BASE_COST": 100,
    "PALINDROME_MULTIPLIER": 2,
    "COST_PER_CHARACTER": 5,
    "LENGTH_PENALTY": 500,
    "UNIQUE_WORDS_BONUS": -200,
    "COST_PER_WORD": {"LESS_THEN_3": 10, "LESS_THEN_7": 20, "OTHER": 30},
}

# We compute all the component of the cost function as "cents"
# This is because float representations is not precise enough
# when dealing with credits/money. Here we choose a simple solution
# where the total "cents" is just divided at the end
#
# We can compute this _more_ efficiently but that would be as the detriment
# of maintainability/readability; We have room for improvement if we notice this is slow in-situ
def compute_message_cost(text: str):
    cost_in_cents = COST_PARAMETERS_CENTS["BASE_COST"]

    cost_in_cents += compute_cost_per_characters(text)
    cost_in_cents += compute_cost_third_vowels(text)
    cost_in_cents += compute_length_penalty(text)

    words = text.split()
    cost_in_cents += compute_cost_per_words(words)
    cost_in_cents += compute_unique_words(words)

    if is_palindrome(text):
        cost_in_cents *= COST_PARAMETERS_CENTS["PALINDROME_MULTIPLIER"]

    cost_in_cents = max(cost_in_cents, 100)
    return cost_in_cents / 100


def compute_cost_per_characters(text: str):
    return len(text) * COST_PARAMETERS_CENTS["COST_PER_CHARACTER"]


def compute_length_penalty(text: str):
    return COST_PARAMETERS_CENTS["LENGTH_PENALTY"] if len(text) > 100 else 0


def compute_unique_words(words: List[str]):
    words_set = {}
    duplicate_found = False

    for word in words:
        if word in words_set:
            duplicate_found = True
            break
        else:
            words_set[word] = True

    if duplicate_found:
        return 0
    else:
        return COST_PARAMETERS_CENTS["UNIQUE_WORDS_BONUS"]


def compute_cost_per_words(words: List[str]):
    total_cost = 0
    for word in words:
        word_length = len(word)
        match word_length:
            case length if length <= 3:
                total_cost += 10
            case length if length <= 7:
                total_cost += 20
            case _:
                total_cost += 30

    return total_cost


def compute_cost_third_vowels(text: str):
    text_lowercase = text.lower()
    vowels = {"a", "e", "i", "o", "u"}
    total_cost = 0
    for i, character in enumerate(text_lowercase):
        if i % 3 == 0:
            if character in vowels:
                total_cost += 30

    return total_cost


def is_palindrome(text):
    text_processed = text.lower()
    text_processed = "".join(char for char in text_processed if char.isalnum())
    return text_processed[::-1] == text_processed
