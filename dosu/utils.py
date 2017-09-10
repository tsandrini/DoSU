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


from .settings import HOME


class Config:

    config_paths = (
        HOME + '/.config/dosu/config.yaml',
        HOME + '/.dosu.yaml',
        HOME + '/Projekty/DoSU/htdocs/dosu/config/example.yaml',
    )

    def __init__(self):
        self.config = self.load_raw_config()
        self.subjects = self.load_subjects()

    def load_raw_config(self):
        for config_path in self.config_paths:
            try:
                with open(config_path, 'r') as ymlfile:
                    return yaml.load(ymlfile)
            except IOError as e:
                continue
        else:
            return None

    def load_subjects(self):

        if not self.config:
            return None

        base = self.get('general.root_dir')

        if not base:
            print ("DoSU root dir is not defined in config file")
            sys.exit(2)

        return set([name for name in os.listdir(base) if os.path.isdir(base + '/' + name)])

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

config = Config()
