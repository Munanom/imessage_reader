#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
cli.py
Entrypoint to the command line interface.
Python 3.8+
Date created: October 15th, 2020
Date modified: May 30th, 2023
"""

import argparse
import os
import sys

from os.path import expanduser

from imessage_reader import fetch_data
from imessage_reader import info


# Path to the chat.db file on macOS
MACOS_DB_PATH = expanduser("~") + "/Library/Messages/chat.db"


def get_parser() -> argparse.ArgumentParser:
    """Create the argument parser

    Returns:
        argparse.ArgumentParser: parser
    """

    parser = argparse.ArgumentParser(
        description="A tool to fetch messages from the chat.db file."
    )

    parser.add_argument(
        "-p",
        "--path",
        type=str,
        nargs="?",
        const=MACOS_DB_PATH,
        default=MACOS_DB_PATH,
        help="Path to the database file"
    )

    parser.add_argument(
        "-o",
        "--output",
        nargs="?",
        default="nothing",
        help="e = Excel, s = SQLite, r = Show recipients"
    )

    parser.add_argument(
        "-v",
        "--version",
        help="Show the current version.",
        action="store_true"
    )

    return parser


def check_path_to_database(args):
    """
    Parse arguments from sys.argv and perform the appropriate actions.
    :param args: The user's input
    """
    if args.path == MACOS_DB_PATH:
        evaluate(MACOS_DB_PATH, args.output, args.version)
    elif os.path.isdir(args.path):
        db_path = args.path + "/chat.db"
        evaluate(db_path, args.output, args.version)
    else:
        sys.exit("Path doesn't exist! Exit program.")


def evaluate(path: str, output: str, version: bool):
    data = fetch_data.FetchData(path, output)
    print(f"{path}, {output}")

    if version:
        info.app_info()

    if output == "e" or output == "excel":
        data.show_user_txt("excel")
    elif output == "s" or output == "sqlite" or output == "sqlite3":
        data.show_user_txt("sqlite")
    elif output == "r" or output == "recipients":
        data.show_user_txt("recipients")
    else:
        data.show_user_txt("nothing")


def main():
    """
    Entrypoint to the command-line interface (CLI).
    """
    parser = get_parser()
    args = parser.parse_args()
    check_path_to_database(args)


if __name__ == "__main__":
    main()
