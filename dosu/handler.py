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


import sys
import shutil
from distutils.dir_util import copy_tree


from . import config
from .decorators import trackcalls


@trackcalls
def make(subject):
    if subject in config.subjects:
        print ("Subject already exists")
        return False

    subject_dir = config.get('templates.subject_dir')
    root_dir = config.get('general.root_dir')

    if not root_dir:
        print ("Root dir is not defined in config file")
        return False

    if not subject_dir:
        print ("Subject template dir is not defined in config file")
        return False


    copy_tree(subject_dir, root_dir + '/' + subject)
    return True

@trackcalls
def delete(subject):
    if subject not in config.subjects:
        print ("Cannot delete subject that does not exist")
        return False

    root_dir = config.get('general.root_dir')

    if not root_dir:
        print ("Root dir is not defined in config file")
        return False

    shutil.rmtree(root_dir + '/' + subject)
    return True
