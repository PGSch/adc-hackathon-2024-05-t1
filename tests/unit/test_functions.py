# imports
import pytest
import re

# function to test
from src.pig_latin import pig_latin

# unit tests
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("apple", "appleway"),
        ("hello", "ellohay"),
        ("Hello", "Ellohay"),
        ("world!", "orldway!"),
        ("123", "123"),
        ("", ""),
        ("hello world!", "ellohay orldway!"),
        ("xyz", "xyzay"),
        ("rhythm", "rhythmay"),
        ("hello123", "ellohay123"),
        ("supercalifragilisticexpialidocious", "upercalifragilisticexpialidocioussay"),
    ],
)
def test_pig_latin(input_text, expected_output):
    assert pig_latin(input_text) == expected_output