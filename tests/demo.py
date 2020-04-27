#!/usr/bin/env python
import argsimple
from pathlib import Path

from argsimple.option import Option


import logging

# logging.getLogger().setLevel(logging.DEBUG)


if __name__ == "__main__":
    # argsimple has only one command: "add()"
    # the minimum number of values is one prefix (must start with "-")
    argsimple.add("--output")
    # but it also accepts a variety of keywords
    argsimple.add("-f", "--float", type=float, default=0.999, help="a float")
    argsimple.add("-i", "--input", type=Path, required=True, help="an input file")
    argsimple.add("-u", "--url", dest="bannana", help="a url")
    argsimple.add("-s", "--string", choices=["a", "b", "c"], help="a string")
    argsimple.add("--test", type=bool, group="extra arguments", help="is a test")

    # arguments are parsed when they are called, and referenced through the main module
    # arguments default to none if they were not given
    # print(Option._options_by_name)

    print(f"output -> {argsimple.output}")
    print(f"float -> {argsimple.float}")
    print(f"input -> {argsimple.input}")
    print(f"bannana -> {argsimple.bannana}")
    print(f"string -> {argsimple.string}")
    print(f"test -> {argsimple.test}")

    try:
        argsimple.spam
    except AttributeError:
        print("Caught attribute error")
