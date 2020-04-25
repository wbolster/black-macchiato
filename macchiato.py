import itertools
import sys
import tempfile
import tokenize
from typing import IO, Iterable, List, NamedTuple, Optional, Tuple, cast

import black


__version__ = "1.2.0"

_single_indent = " " * 4


class WrapInfo(NamedTuple):
    """Describes the changes made when wrapping text."""

    n_blank_before: int = 0
    n_blank_after: int = 0
    n_fake_before: int = 0
    n_fake_after: int = 0


def _indent_levels(line: str) -> int:
    """Determine how many levels the line is indented."""

    spaces = len(line) - len(line.lstrip())
    levels, remainder = divmod(spaces, 4)
    if remainder:
        raise ValueError("indent of first line must be a multiple of four")
    return levels


def _fake_before_lines(first_line: str) -> List[str]:
    """Construct the fake lines that should go before the text."""

    fake_lines = []
    indent_levels = _indent_levels(first_line)

    # Handle regular indent
    for i in range(indent_levels):
        prefix = _single_indent * i
        fake_lines.append(f"{prefix}if True:\n")

    # Handle else/elif/except/finally
    try:
        first_token: Optional[tokenize.TokenInfo] = next(
            tokenize.generate_tokens(iter([first_line.lstrip()]).__next__)
        )
    except tokenize.TokenError:
        first_token = None
    if first_token and first_token.type == tokenize.NAME:
        name = first_token.string
        prefix = _single_indent * indent_levels
        if name in {"else", "elif"}:
            fake_lines.append(f"{prefix}if True:\n")
            fake_lines.append(f"{prefix}{_single_indent}pass\n")
        elif name in {"except", "finally"}:
            fake_lines.append(f"{prefix}try:\n")
            fake_lines.append(f"{prefix}{_single_indent}pass\n")

    return fake_lines


def _fake_after_lines(last_line: str) -> List[str]:
    """Construct the fake lines that should go after the text."""

    lines = []

    # Detect an unclosed block at the end. Add a ‘pass’ line if needed for valid syntax.
    if last_line.rstrip().endswith(":"):
        indent_levels = _indent_levels(last_line)
        prefix = _single_indent * (indent_levels + 1)
        lines.append(f"{prefix}pass\n")

    return lines


def wrap_lines(lines: List[str]) -> Tuple[List[str], WrapInfo]:
    """Wrap the input lines with fake text, to fake a complete source document."""

    # Strip leading and trailing blank lines.
    n_blank_before, n_blank_after = count_surrounding_blank_lines(lines)
    until = len(lines) - n_blank_after
    lines = lines[n_blank_before:until]
    if not lines:
        wrap_info = WrapInfo(n_blank_before=n_blank_before, n_blank_after=n_blank_after)
        return lines, wrap_info

    # Construct fake lines that need to surround the text for valid syntax.
    first_line = lines[0]
    fake_before_lines = _fake_before_lines(first_line)

    last_line = lines[-1]
    fake_after_lines = _fake_after_lines(last_line)

    lines = fake_before_lines + lines + fake_after_lines

    wrap_info = WrapInfo(
        n_blank_before=n_blank_before,
        n_blank_after=n_blank_after,
        n_fake_before=len(fake_before_lines),
        n_fake_after=len(fake_after_lines),
    )
    return lines, wrap_info


def format_lines(lines: List[str], black_args=None) -> List[str]:
    if black_args is None:
        black_args = []

    with tempfile.NamedTemporaryFile(suffix=".py", mode="wt+", delete=False) as fp:
        # Copy the input.
        for line in lines:
            fp.write(line)
        fp.flush()

        # Run black.
        if "--quiet" not in black_args:
            black_args.append("--quiet")
        black_args.append(fp.name)

        try:
            exit_code = black.main(args=black_args)
        except SystemExit as exc:
            exit_code = exc.code

        if exit_code == 0:
            # Write output.
            fp.seek(0)
            return cast(List[str], fp.readlines())

        raise RuntimeError("black failed", exit_code)


def unwrap_lines(lines: List[str], wrap_info: WrapInfo) -> List[str]:
    """Unwrap previously-wrapped text."""

    until = len(lines) - wrap_info.n_fake_after
    lines = lines[wrap_info.n_fake_before : until]

    fmt_n_blank_before, _ = count_surrounding_blank_lines(lines)
    lines = lines[fmt_n_blank_before:]

    # Restore blank lines.
    blank_before = ["\n"] * wrap_info.n_blank_before
    blank_after = ["\n"] * wrap_info.n_blank_after

    return blank_before + lines + blank_after


def macchiato(in_fp: IO[str], out_fp: IO[str], args=None):
    # Read input.
    lines = in_fp.readlines()

    # Build syntactically valid text.
    lines, wrap_info = wrap_lines(lines)

    # Format.
    try:
        lines = format_lines(lines, black_args=args)
    except RuntimeError as e:
        exit_code = e.args[1]
        return exit_code

    # Unwrap text and write output.
    lines = unwrap_lines(lines, wrap_info)
    for line in lines:
        out_fp.write(line)

    return 0


def is_blank_string(s):
    return s.isspace() or not s


def count_surrounding_blank_lines(lines: Iterable[str]) -> Tuple[int, int]:
    before = 0
    after = 0
    grouper = itertools.groupby(lines, is_blank_string)
    try:
        is_blank, group = next(grouper)
    except StopIteration:
        pass
    else:
        if is_blank:
            before = len(list(group))

    for is_blank, group in grouper:
        after = len(list(group)) if is_blank else 0

    return before, after


def main():
    try:
        args = sys.argv[1:]
        exit_code = macchiato(sys.stdin, sys.stdout, args)
    except ValueError as exc:
        raise SystemExit(str(exc))
    else:
        raise SystemExit(exit_code)


if __name__ == "__main__":
    sys.exit(main())
