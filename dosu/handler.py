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


import os
import sys
import shutil
import errno
import time
import fnmatch
import subprocess
import shlex
from datetime import datetime
from distutils.dir_util import copy_tree


from . import config
from .utils import load_file
from .decorators import trackcalls


@trackcalls
def make(subjects):
    subject_dir = config.get('templates.subject_dir')
    root_dir = config.get('general.root_dir')

    if not root_dir:
        print ("Root dir is not defined in config file")
        return False

    if not subject_dir:
        print ("Subject template dir is not defined in config file")
        return False

    for subject in subjects:

        if subject in config.subjects:
            print ("Subject %s already exists" % subject)
            continue

        copy_tree(subject_dir, root_dir + '/' + subject)

    else:
        return True

    return False

@trackcalls
def delete(subjects):
    root_dir = config.get('general.root_dir')

    if not root_dir:
        print ("Root dir is not defined in config file")
        return False

    for subject in subjects:

        if subject not in config.subjects:
            print ("Subject %s does not exist" % subject)
            continue

        shutil.rmtree(root_dir + '/' + subject)

    else:
        return True

    return False

@trackcalls
def write(subject):
    if subject not in config.subjects:
        print ("Subject %s does not exist" % subject)

    root_dir = config.get('general.root_dir')

    if not root_dir:
        print ("Root dir is not defined in config file")
        return False

    today = datetime.today()
    subject_dir = root_dir + '/' + subject
    path = '%s/notes/year_%d/month_%02d' % (
        subject_dir,
        today.year % 1000,
        today.month
    )

    try:
        os.makedirs(path)
        note_number = 0
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        else:
            note_number = len(fnmatch.filter(os.listdir(path), 'note_*.md'))

    note_number += 1

    meta = load_file(subject_dir + '/meta.md') % {
        'name': config.get('author.name'),
        'email': config.get('author.email'),
        'date': time.strftime('%d.%m.%Y'),
        'subject': subject,
        'number': note_number
    }

    path += '/note_%d.md' % note_number

    with open(path, 'w') as f:
        f.write(meta)

    os.chdir(subject_dir)
    if config.get('writing.open_reader'):

        tmp_pdf_path = subject_dir + '/' + '.tmp.pdf'
        subprocess.Popen(['pandoc', path, '-o', tmp_pdf_path]).wait()

        cmd = shlex.split(config.get('writing.reader'))
        cmd.append(tmp_pdf_path)
        subprocess.Popen(cmd)

    if config.get('writing.open_editor'):
        cmd = shlex.split(config.get('writing.editor'))
        cmd.append(path)
        subprocess.Popen(cmd)

    sys.exit(0)

    return True
