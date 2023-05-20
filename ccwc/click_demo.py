#!/usr/bin/env python3
import click


@click.group()
def greet():
    pass


@click.command()
def hello(**kwargs):
    pass


@click.command()
def goodbye(**kwargs):
    pass


if __name__ == "__main__":
    greet()
