import io

import macchiato

import pytest


@pytest.mark.parametrize(
    "lines, before, after",
    [
        ([], 0, 0),
        ([""], 1, 0),
        ([" ", "", "foo"], 2, 0),
        (["foo", ""], 0, 1),
        ([" ", "", "foo", "  ", "bar", "baz", "", "", ""], 2, 3),
        ([" ", "", "foo", "  ", "bar", "baz", "", "", "quux"], 2, 0),
    ],
)
def test_count_surrounding_blank_lines(lines, before, after):
    actual = macchiato.count_surrounding_blank_lines(lines)
    assert (before, after) == actual
