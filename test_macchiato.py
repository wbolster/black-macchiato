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


@pytest.mark.parametrize(
    "input, expected",
    [
        ("foo\n", "foo\n"),
        ("    foo\n", "    foo\n"),
        ("    if True:\n", "    if True:\n"),
        ("\n\n        x=3\n\n", "\n\n        x = 3\n\n")
    ],
)
def test_macchiato(input, expected):
    in_fp = io.StringIO(input)
    out_fp = io.StringIO()
    exit_code = macchiato.macchiato(in_fp, out_fp)
    assert exit_code == 0
    output = out_fp.getvalue()
    assert output == expected
