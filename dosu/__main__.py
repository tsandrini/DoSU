"""
__/\\\\\\\\\\\\______________________/\\\\\\\\\\\____/\\\________/\\\_
 _\/\\\////////\\\__________________/\\\/////////\\\_\/\\\_______\/\\\_
  _\/\\\______\//\\\________________\//\\\______\///__\/\\\_______\/\\\_
   _\/\\\_______\/\\\_____/\\\\\______\////\\\_________\/\\\_______\/\\\_
    _\/\\\_______\/\\\___/\\\///\\\_______\////\\\______\/\\\_______\/\\\_
       _\/\\\\\\\\\\\\/____\///\\\\\/___\///\\\\\\\\\\\/____\///\\\\\\\\\/___
        _\////////////________\/////_______\///////////________\/////////_____

Created by Tomáš Sandrini
"""

from . import __version__

import argparse
import os
import shutil
import sys
from datetime import datetime

from . import handler


def get_args(args):
    """
    Get the script arguments.
    """
    description = "DoSU - pandoc note writing utility"
    arg = argparse.ArgumentParser(description=description)

    arg.add_argument(
        '-M',
        metavar='make',
        nargs='+',
        help="Make (create) given subjects"
    )

    arg.add_argument(
        '-C',
        metavar='compile',
        nargs='+',
        help="Compile notes for a given subjects"
    )

    arg.add_argument(
        '-W',
        metavar='write',
        help="Start note taking for a subject"
    )

    arg.add_argument(
        '-D',
        metavar='delete',
        nargs='+',
        help="Delete subjects"
    )

    arg.add_argument(
        '-m',
        metavar='month',
        nargs='+',
        type=int,
        help="months"
    )

    arg.add_argument(
        '-y',
        metavar='year',
        nargs='+',
        type=int,
        help="years"
    )

    arg.add_argument(
        '-v',
        action='store_true',
        help="Print current dosu version"
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

    if args.M:
        handler.make(args.M)

    if args.D:
        handler.delete(args.D)

    if args.W:
        handler.write(args.W)

    if args.C:
        today = datetime.today()

        years = args.y if args.y != None else [today.year]
        months = args.m if args.m != None else [today.month]

        if args.y:
            months = args.m if args.m else [i for i in range(13)][1:]
        else:
            months = args.m if args.m else [today.month]

        handler.compile(subjects=args.C, years=years, months=months)

    if args.q:
        sys.stdout = sys.stderr = open(os.devnull, 'w')

    if args.v:
        print("dosu", __version__)
        sys.exit(0)


def main():
    """
    Main script function
    """
    args = get_args(sys.argv[1:])
    process_args(args)


if __name__ == "__main__":
    main()
