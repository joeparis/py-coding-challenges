#!/usr/bin/env python3
"""Recreating the GNU wc utility."""
import sys
from pathlib import Path

import click


@click.command()
@click.argument("file")
@click.option("-c", "--bytes", is_flag=True, help="Print the byte counts.")
@click.option("-l", "--lines", is_flag=True, help="Print the newline counts.")
@click.option("-w", "--words", is_flag=True, help="Print the word counts.")
@click.option("-m", "--chars", is_flag=True, help="Print the character counts.")
@click.version_option(version="0.1.0")
def cli(file, bytes, lines, words, chars):
    file_path = Path(file)

    byte_count = len(file_path.read_bytes())
    word_count = 0
    char_count = 0

    with file_path.open(encoding="utf-8") as f:
        lines_ = f.readlines()
        line_count = len(lines_)

        for line in lines_:
            word_count += len(line.strip().split())
            char_count += len(line)

    assert byte_count == 341836
    assert line_count == 7137
    assert word_count == 58159
    # assert char_count == 339120

    if bytes:
        click.echo(f"{byte_count} {file_path.name}")
        return 0
    if lines:
        click.echo(f"{line_count} {file_path.name}")
        return 0
    if words:
        click.echo(f"{word_count} {file_path.name}")
        return 0
    if chars:
        click.echo(f"{char_count} {file_path.name}")
        return 0

    click.echo(f"{line_count:>8}{word_count:>8}{byte_count:>8} {file_path.name}")


def main():
    return cli(prog_name="ccwc")


if __name__ == "__main__":
    sys.exit(main())
