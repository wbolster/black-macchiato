import itertools
import sys
import tempfile

import black


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
        raise SystemExit("indent of first line must be a multiple of four")
    for i in range(n_fake_before):
        prefix = 4 * i * " "
        lines.insert(i, f"{prefix}if True:\n")

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
            out_fp.write("\n" * n_blank_before)
            until = len(formatted_lines) - n_fake_after
            for line in formatted_lines[n_fake_before:until]:
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
