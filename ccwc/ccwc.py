#!/usr/bin/env python3
"""Recreating the GNU wc utility."""
import os
from pathlib import Path

import click


@click.command()
@click.argument("file")
@click.option("-c", "--bytes", is_flag=True, help="Print the byte counts.")
@click.option("-l", "--lines", is_flag=True, help="Print the byte counts.")
@click.option("-w", "--words", is_flag=True, help="Print the byte counts.")
@click.version_option(version="0.1.0")
def cli(file, bytes, lines, words):
    file_path = Path(file)

    if bytes:
        _bytes = file_path.read_bytes()
        click.echo(f"{len(_bytes)} {file_path.name}")

    if lines:
        with file_path.open(encoding="utf-8") as f:
            click.echo(f"{len(f.readlines())} {file_path.name}")

    if words:
        count = 0
        with file_path.open(encoding="utf-8") as f:
            _lines = f.readlines()
            for line in _lines:
                count += len(line.strip().split())

        click.echo(f"{count} {file_path.name}")


def main():
    # cli()
    cli(prog_name="ccwc")


if __name__ == "__main__":
    main()
