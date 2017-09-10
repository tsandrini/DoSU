"""
__/\\\\\\\\\\\\______________________/\\\\\\\\\\\____/\\\________/\\\_
 _\/\\\////////\\\__________________/\\\/////////\\\_\/\\\_______\/\\\_
  _\/\\\______\//\\\________________\//\\\______\///__\/\\\_______\/\\\_
   _\/\\\_______\/\\\_____/\\\\\______\////\\\_________\/\\\_______\/\\\_
    _\/\\\_______\/\\\___/\\\///\\\_______\////\\\______\/\\\_______\/\\\_
     _\/\\\_______\/\\\__/\\\__\//\\\_________\////\\\___\/\\\_______\/\\\_
      _\/\\\_______/\\\__\//\\\__/\\\___/\\\______\//\\\__\//\\\______/\\\__
       _\/\\\\\\\\\\\\/____\///\\\\\/___\///\\\\\\\\\\\/____\///\\\\\\\\\/___
        _\////////////________\/////_______\///////////________\/////////_____

Created by Tomáš Sandrini
"""

from . import __version__

import argparse
import os
import shutil
import sys

from . import handler


def get_args(args):
    """
    Get the script arguments.
    """
    description = "DoSU - pandoc note writing utility"
    arg = argparse.ArgumentParser(description=description)

    arg.add_argument(
        '-m',
        metavar='make',
        nargs='+',
        help="Make subject"
    )

    arg.add_argument(
        '-c',
        metavar='compile',
        help="Compile notes for a given subject"
    )

    arg.add_argument(
        '-w',
        metavar='write',
        help="Start writing notes for a given subject"
    )

    arg.add_argument(
        '-v',
        action='store_true',
        help="Print current dosu version"
    )

    arg.add_argument(
        '-d',
        metavar='delete',
        nargs='+',
        help="Deletes a subject"
    )

    arg.add_argument(
        '-q',
        action='store_true',
        help="Quiet mode, don't print anything and \
            don't display notifications."
    )


    return arg.parse_args(args)


def process_args(args):
    """
    Process args.
    """
    if not len(sys.argv) > 1 and False:
        print("error: dosu needs to be given arguments to run.\n"
              "       Refer to \"dosu -h\" for more info.")
        sys.exit(1)

    if args.v:
        print("dosu", __version__)
        sys.exit(0)

    if args.m:
        handler.make(args.m)

    if args.d:
        handler.delete(args.d)

    if args.w:
        handler.write(args.w)

    if args.q:
        sys.stdout = sys.stderr = open(os.devnull, 'w')


def main():
    """
    Main script function
    """
    args = get_args(sys.argv[1:])
    process_args(args)


if __name__ == "__main__":
    main()
