#!/usr/bin/env python3
"""Recreating the GNU wc utility."""
import os
from pathlib import Path

import click


# @click.group("cli")
@click.command()
# @click.pass_context
@click.argument("file")
# @click.argument("file", type=click.Path(exists=True), nargs=-1)
@click.option("-c", "--bytes", is_flag=True, help="Print the byte counts.")
@click.version_option(version="0.1.0")
def cli(file, bytes):
    file_path = Path(file)

    if bytes:
        click.echo(f"{os.stat(str(file_path)).st_size} {file_path.name}")

        bytes = file_path.read_bytes()
        click.echo(f"{len(bytes)} {file_path.name}")


def main():
    # cli()
    cli(prog_name="ccwc")


if __name__ == "__main__":
    main()
