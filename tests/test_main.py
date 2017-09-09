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


import unittest
import unittest.mock

import os
import random

from dosu import __main__
from dosu import handler
from dosu.utils import str_random
from dosu import config


class TestMain(unittest.TestCase):

    def test_args_w(self):
        subject = 'TestSubject' + str_random(5)
        args = __main__.get_args(['-w', subject])
        __main__.process_args(args)
        self.assertTrue(handler.make.has_been_called)

    def test_args_d(self):
        subject = random.choice(config.subjects)
        args = __main__.get_args(['-d', subject])
        __main__.process_args(args)
        self.assertTrue(handler.delete.has_been_called)


if __name__ == "__main__":
    unittest.main()
