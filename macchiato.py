import itertools
import sys
import tempfile
import tokenize

import black


__version__ = "1.2.0"


def macchiato(in_fp, out_fp, args=None):
    if args is None:
        args = []

    # Read input.
    lines = in_fp.readlines()

    # Detect blank lines and deal with completely blank input.
    n_blank_before, n_blank_after = count_surrounding_blank_lines(lines)
    until = len(lines) - n_blank_after
    lines = lines[n_blank_before:until]
    if not lines:
        out_fp.write("\n" * n_blank_before)
        return 0

    # Detect indentation. Add "if True:" lines if needed for valid syntax.
    first_line = lines[0]
    indent = len(first_line) - len(first_line.lstrip())
    n_fake_before, remainder = divmod(indent, 4)
    if remainder:
        raise ValueError("indent of first line must be a multiple of four")
    for i in range(n_fake_before):
        prefix = 4 * i * " "
        lines.insert(i, f"{prefix}if True:\n")

    # Handle else/elif/except/finally
    try:
        first_token = next(
            tokenize.generate_tokens(iter([first_line.lstrip()]).__next__)
        )
    except tokenize.TokenError:
        first_token = None
    if first_token and first_token.type == tokenize.NAME:
        name = first_token.string
        if name in {"else", "elif"}:
            lines.insert(n_fake_before, f"{indent * ' '}if True:\n")
            lines.insert(n_fake_before + 1, f"{indent * ' '}    pass\n")
            n_fake_before += 2
        elif name in {"except", "finally"}:
            lines.insert(n_fake_before, f"{indent * ' '}try:\n")
            lines.insert(n_fake_before + 1, f"{indent * ' '}    pass\n")
            n_fake_before += 2

    # Detect an unclosed block at the end. Add ‘pass’ at the end of the line if
    # needed for valid syntax.
    last_line = lines[-1]
    n_fake_after = 0
    if last_line.rstrip().endswith(":"):
        lines[-1] = last_line.rstrip() + "pass\n"
        n_fake_after = 1

    with tempfile.NamedTemporaryFile(suffix=".py", mode="wt+", delete=False) as fp:

        # Copy the input.
        for line in lines:
            fp.write(line)

        fp.flush()

        # Run black.
        if "--quiet" not in args:
            args.append("--quiet")
        args.append(fp.name)
        try:
            exit_code = black.main(args=args)
        except SystemExit as exc:
            exit_code = exc.code

        if exit_code == 0:
            # Write output.
            fp.seek(0)
            formatted_lines = fp.readlines()
            until = len(formatted_lines) - n_fake_after
            formatted_lines = formatted_lines[n_fake_before:until]
            fmt_n_blank_before, _ = count_surrounding_blank_lines(formatted_lines)
            formatted_lines = formatted_lines[fmt_n_blank_before:]
            out_fp.write("\n" * n_blank_before)
            for line in formatted_lines:
                out_fp.write(line)
            out_fp.write("\n" * n_blank_after)

    return exit_code


def is_blank_string(s):
    return s.isspace() or not s


def count_surrounding_blank_lines(lines):
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
