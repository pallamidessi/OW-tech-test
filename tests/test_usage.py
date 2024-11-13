import pytest
from usage import (  # Replace 'app' with the actual module name if needed
    compute_message_cost,
    compute_cost_per_characters,
    compute_length_penalty,
    compute_unique_words,
    compute_cost_per_words,
    compute_cost_third_vowels,
    is_palindrome,
)

## Those test cases are VERY incomplete but show that our code is easy to test !

# Test the full cost functions
def test_compute_message_cost():
    assert compute_message_cost("racecar") == 1  # Palindrome
    assert compute_message_cost("hello world") == 1  # Unique words
    assert compute_message_cost("hello hello") == 1.95  # Simple test

# Test the different cost components
def test_compute_cost_per_characters():
    assert compute_cost_per_characters("hello") == 25


def test_compute_length_penalty():
    assert compute_length_penalty("a" * 101) == 500  # Exceeds 100 characters
    assert compute_length_penalty("short text") == 0


def test_compute_unique_words():
    assert compute_unique_words(["hello", "world"]) == -200  # Unique words
    assert compute_unique_words(["hello", "hello"]) == 0  # Duplicate found


def test_compute_cost_per_words():
    assert compute_cost_per_words(["hi", "hello", "worlds"]) == 50
    assert compute_cost_per_words(["veryverylongword"]) == 30


def test_compute_cost_third_vowels():
    assert compute_cost_third_vowels("amazing") == 30  # 'a' at index 0
    assert compute_cost_third_vowels("hello") == 0


def test_is_palindrome():
    assert is_palindrome("racecar") is True
    assert is_palindrome("hello") is False
