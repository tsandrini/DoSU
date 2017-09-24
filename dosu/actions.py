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


import argparse


class ValidateMonths(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        months = [int(month) for month in args]
        setattr(args, self.dest, months)


class ValidateYears(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        years = [int(year) for years in args]
        setattr(args, self.dest, years)
