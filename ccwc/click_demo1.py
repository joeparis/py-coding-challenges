#!/usr/bin/env python3
"""From https://www.assemblyai.com/blog/the-definitive-guide-to-python-click/"""
import json
import pprint
import re
import string

import click


# @click.group(<name>) creates a command that instantiates a group class
# a group is intended to be a set of related commands
# @click.argument(<argument name>) tells us that we will be passing an argument
# and referring to that argument in the function by the name we pass it
# @click.pass_context tells the group command that we're going to be using
# the context, the context is not visible to the command unless we pass this
#
# In our example we'll name our group "cli"
@click.group("cli")
@click.version_option(version="0.1.0")
@click.pass_context
@click.argument("file")
def cli(ctx: click.Context, file: str):
    """An example CLI for interfacing with a document."""
    _stream = open(file)
    _dict = json.load(_stream)
    _stream.close()
    ctx.obj = _dict


# @click.command(<name>) creates a command that can be called with
# the name that we pass through
#
# Here we'll create an example command that prints out our context object,
# which we expect to be a json looking dictionary
@cli.command("check_context_object")
@click.pass_context
def check_context(ctx):
    pprint.pprint(type(ctx.obj))


# Here we'll make a pass decorator, which we can use to pass
# the last object stored of a type of our choosing in the context
# by using click.make_pass_decorator(<type>)
pass_dict = click.make_pass_decorator(dict)


# click.echo is click's version of the echo command
# click.style lets us style our output
# click.secho is a command that takes a message, and a style command,
# and is a combination of click.echo and click.style
#
# This command returns the keys to our dictionary object and
# demonstrates how to use click.echo, click.style, and click.secho


@cli.command("get_keys")
@pass_dict
def get_keys(_dict: dict):
    keys = list(_dict.keys())
    click.secho("The keys in our dictionary are:", fg="green")
    click.echo(click.style(keys, fg="blue"))


# This command gets a specific key from the context object
@cli.command("get_key")
@click.argument("key")
@click.pass_context
def get_key(ctx: click.Context, key: str):
    pprint.pprint(ctx.obj[key])


# click.invoke(<command>, <args>) is click's way of letting us
# arbitrarily nest commands. NOTE: this command can only be used
# when both the command being invoked AND the the command
# doing the invoking use @click.pass_context
#
# Since we already have a get_key command, we can just call that
# to print out a summary
@cli.command("get_summary")
@click.pass_context
def get_name(ctx: click.Context):
    ctx.invoke(get_key, key="summary")


# @click.option(<one dash usage>, <two dash usage>, is_flag (optional), help = <help>)
# is how we can pass options to our command
#
# We'll create a function that gets the "results" of our dictionary
# and we will pass it two optional arguments, one to specify that
# we want a specific key from the results, and a flag to indicate
# whether or not we want to save our results to a json file
@cli.command("get_results")
@click.option("-d", "--download", is_flag=True, help="Pass to download the result to a json file")
@click.option("-k", "--key", help="Pass a key to specify that key from the results")
@click.pass_context
def get_results(ctx: click.Context, download: bool, key: str):
    results = ctx.obj["results"]

    if key is not None:
        result = {}
        for entry in results:
            if key in entry:
                if key in result:
                    result[key] += entry[key]
                else:
                    result[key] = entry[key]
        results = result

    if download:
        if key is not None:
            filename = key + ".json"
        else:
            filename = "results.json"

        with open(filename, mode="w", encoding="utf-8") as w:
            w.write(json.dumps(results, indent=2))
        print(f"File saved to {filename}")
    else:
        pprint.pprint(results, indent=2)


# @click.pass_obj is similar to @click.pass_context, instead
# of passing the whole context, it only passes context.obj
#
# We'll do something fun with our text extractor, we'll include
# options to extract as either paragraphs or sentences, and
# default to returning one big block of text
@cli.command("get_text")
@click.option("-s", "--sentences", is_flag=True, help="Pass to return sentences")
@click.option("-p", "--paragraphs", is_flag=True, help="Pass to return paragraphs")
@click.option("-d", "--download", is_flag=True, help="Download as json file")
@click.pass_obj
def get_text(_dict, sentences, paragraphs, download):
    """Returns the text as sentences, paragraphs, or one block by default"""
    results = _dict["results"]
    text = {}
    for idx, entry in enumerate(results):
        if paragraphs:
            text[idx] = entry["text"]
        else:
            if "text" in text:
                text["text"] += entry["text"]
            else:
                text["text"] = entry["text"]

    if sentences:
        # sentences = text["text"].split(".")
        sentences = re.split("\.|\?|!", text["text"])
        # for i in range(len(sentences)):
        for i, _ in enumerate(sentences):
            if sentences[i]:
                text[i] = sentences[i].strip()
        del text["text"]
    pprint.pprint(text, indent=2)

    if download:
        if paragraphs:
            filename = "paragraphs.json"
        elif sentences:
            filename = "sentences.json"
        else:
            filename = "text.json"

        with open(filename, mode="w", encoding="utf-8") as w:
            w.write(json.dumps(results, indent=2))
        print(f"File saved to {filename}")


def main():
    cli(prog_name="cli")


if __name__ == "__main__":
    main()
