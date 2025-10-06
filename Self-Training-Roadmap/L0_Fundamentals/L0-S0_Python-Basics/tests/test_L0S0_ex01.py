import pytest
from exercises.L0S0_ex01_str import (
    sentences,
    clean_text,
    ascii_only,
    to_uppercase,
    check_start_end,
    replace_digits,
    join_sentences,
)

ORIGINAL = [
    "  Hello World!  ",
    "Python 3.12.1 is out.",
    "سلام دنیا",
    "    DATA, 2025!!   ",
    "   \tclean Me\t\n",
]


def test_clean_text_strips_whitespace():
    expected = ["Hello World!", "Python 3.12.1 is out.", "سلام دنیا", "DATA, 2025!!", "clean Me"]
    assert clean_text(ORIGINAL) == expected


def test_ascii_only_filters_non_ascii():
    expected = [
        "  Hello World!  ",
        "Python 3.12.1 is out.",
        "    DATA, 2025!!   ",
        "   \tclean Me\t\n",
    ]
    assert ascii_only(ORIGINAL) == expected


def test_to_uppercase_preserves_non_latin_and_uppercases_ascii():
    expected = [
        "  HELLO WORLD!  ",
        "PYTHON 3.12.1 IS OUT.",
        "سلام دنیا",
        "    DATA, 2025!!   ",
        "   \tCLEAN ME\t\n",
    ]
    assert to_uppercase(ORIGINAL) == expected


def test_check_start_end_behavior_on_original_input():
    # Given the implementation uses the raw strings (including leading/trailing whitespace),
    # none of the original sentences start exactly with "DATA" nor end with a digit,
    # so the result should equal the original list.
    assert check_start_end(ORIGINAL) == ORIGINAL


def test_replace_digits_masks_all_digits_with_X():
    expected = [
        "  Hello World!  ",
        "Python X.XX.X is out.",
        "سلام دنیا",
        "    DATA, XXXX!!   ",
        "   \tclean Me\t\n",
    ]
    assert replace_digits(ORIGINAL) == expected


def test_join_sentences_returns_hash_joined_string():
    expected = "#".join(ORIGINAL)
    assert join_sentences(ORIGINAL) == expected


def test_integration_main_side_effects_are_safe(monkeypatch, capsys):
    # Ensure calling main doesn't raise and it prints something (the original main prints results).
    # We run main once and capture stdout.
    from text_processor import main

    # Run main (it prints then returns)
    main()
    captured = capsys.readouterr()
    assert captured.out  # something was printed