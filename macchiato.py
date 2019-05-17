import itertools
import sys
import tempfile

import black


def main():

    # Read input.
    lines = sys.stdin.readlines()
    non_blank_lines = [line for line in lines if line.strip()]
    if not non_blank_lines:
        for line in lines:
            print(line, end="")
        return 0

    # Detect indentation.
    first_line = non_blank_lines[0]
    indent = len(first_line) - len(first_line.lstrip())
    n_fake_lines, remainder = divmod(indent, 4)
    if remainder:
        raise SystemExit("indent of first line must be a multiple of four")

    with tempfile.NamedTemporaryFile(suffix=".py", mode="wt+") as fp:

        # Write "if True:" lines to produce syntactically valid Python.
        for i in range(n_fake_lines):
            prefix = 4 * i * " "
            fp.write(f"{prefix}if True:\n")

        # Copy the input.
        for line in lines:
            fp.write(line)

        fp.flush()

        # Run black.
        args = sys.argv[1:]
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
            for line in formatted_lines[n_fake_lines:]:
                print(line, end="")

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


if __name__ == "__main__":
    sys.exit(main())
