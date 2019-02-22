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


import yaml
import os
from datetime import datetime


from dosu.settings import HOME


class Config:

    config_paths = (
        HOME + '/.config/dosu/config.yml',
        HOME + '/.dosu.yml',
    )

    def __init__(self):
        self.config = self.load_raw_config()

    def load_raw_config(self):
        for config_path in self.config_paths:
            try:
                with open(config_path, 'r') as ymlfile:
                    return yaml.load(ymlfile)
            except IOError as e:
                continue
        else:
            return None

    def get(self, key, fallback=None):
        """
        Gets a cached value by its key using dotted notation
        """
        try:
            tmp = self.config
            for fragment in key.split('.'):
                tmp = tmp[fragment]
            return tmp
        except KeyError as e:
            return fallback if fallback != None else key


def load_file(path):
    with open(path, 'r') as f:
        data = f.read()

    return data


def parse_semester_from_datetime(d: datetime) -> str:
    y = d.year - 1 if (d.month < 10) else d.year
    S_start = datetime(y, 10, 1)
    S_end = datetime(y + 1, 2, 17)

    s = 'S' if (d >= S_start and d <= S_end) else 'W'
    return '{}{}{}'.format(s, y % 100, (y + 1) % 100)


config = Config()
