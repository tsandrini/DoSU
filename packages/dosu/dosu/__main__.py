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

from dosu import __version__

import argparse
import os
import shutil
import sys
from datetime import datetime

from dosu import handler
from dosu.utils import parse_semester_from_datetime
from dosu.actions import ValidateMonths, ValidateYears


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
        help="Makes (creates) given subjects"
    )

    arg.add_argument(
        '-C',
        metavar='compile',
        nargs='+',
        help="Compiles notes for a given subjects"
    )

    arg.add_argument(
        '-W',
        metavar='write',
        help="Starts note taking for a subject"
    )

    arg.add_argument(
        '-D',
        metavar='delete',
        nargs='+',
        help="Deletes subjects"
    )

    arg.add_argument(
        '-s',
        metavar='semester',
        # action=ValidateMonths,
        help="Semester specification - default will be the current one"
    )

    arg.add_argument(
        '-v',
        action='store_true',
        help="Print current dosu version"
    )

    arg.add_argument(
        '-l',
        action='store_true',
        help="List all subjects"
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
    if not len(sys.argv) > 1:
        print("error: dosu needs to be given arguments to run.\n"
              "       Refer to \"dosu -h\" for more info.")
        raise SystemExit

    if args.q:
        sys.stdout = sys.stderr = open(os.devnull, 'w')

    semester = args.s if args.s is not None \
                else parse_semester_from_datetime(datetime.today())

    if args.M:
        handler.make(args.M, semester)

    if args.D:
        handler.delete(args.D, semester)

    if args.W:
        handler.write(args.W, semester)

    if args.C:
        handler.compile(args.C, semester)

    if args.l:
        handler.list(semester)

    if args.v:
        print("DoSU ", __version__)
        sys.exit(0)


def main():
    """
    Main script function
    """
    args = get_args(sys.argv[1:])
    process_args(args)


if __name__ == "__main__":
    main()
