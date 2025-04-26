import io
import os
import pathlib
from typing import Generator

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
        ("\n\n        x=3\n\n", "\n\n        x = 3\n\n"),
        ("elif x==5:\n", "elif x == 5:\n"),
        ("'''\n'''\n", '""" """\n'),  # tokenize error handling
        ("    finally :\n", "    finally:\n"),
        ("    def f():\n        pass\n", "    def f():\n        pass\n"),
        ("    def f(a,\n          b):\n", "    def f(a, b):\n"),
    ],
)
def test_macchiato(input, expected):
    in_fp = io.StringIO(input)
    out_fp = io.StringIO()
    exit_code = macchiato.macchiato(in_fp, out_fp)
    assert exit_code == 0
    output = out_fp.getvalue()
    assert output == expected


class TestConfig:
    @pytest.fixture
    def working_dir(
        self, tmp_path: pathlib.Path
    ) -> Generator[pathlib.Path, None, None]:
        """Provide a temporary, current working directory."""

        orig_cwd = os.getcwd()

        working_dir = tmp_path / "project" / "component"
        working_dir.mkdir(parents=True)
        os.chdir(working_dir)
        yield working_dir

        os.chdir(orig_cwd)

    def test_detection(self, working_dir: pathlib.Path):
        """Make sure that black config is used if it is present."""

        orig = '["abcdefghijklm", "nopqrstuvwxyz"]\n'

        def do_format() -> str:
            in_fp = io.StringIO(orig)
            out_fp = io.StringIO()
            assert macchiato.macchiato(in_fp, out_fp) == 0
            return out_fp.getvalue()

        # No config, defaults should be used.
        assert do_format() == orig

        # Add config file to parent directory. Shorter line length setting should be used.
        with (working_dir.parent / "pyproject.toml").open("w") as fp:
            fp.write("[tool.black]\nline_length = 25\n")
        assert do_format() == """[\n    "abcdefghijklm",\n    "nopqrstuvwxyz",\n]\n"""

        # Fake a .git directory in current directory. Config file should be ignored.
        (working_dir / ".git").mkdir()
        assert do_format() == orig
