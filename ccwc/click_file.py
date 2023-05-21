#!/usr/bin/env python3
import click


@click.command()
@click.argument("file", type=click.File("rb"))
def inout(file):
    text = file.read()
    o = click.open_file("spam.txt", mode="wb")
    o.write(text)

    file.close()
    o.close()


if __name__ == "__main__":
    inout()
