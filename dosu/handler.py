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
    """
    Makes (creates) given subjects
    """
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

        copy_tree(subject_dir, root_dir + '/' + subject, preserve_symlinks=1)

    else:
        return True

    return False

@trackcalls
def delete(subjects):
    """
    Deletes given subjects
    """
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
    """
    Starts notetaking for a given subject
    """
    if subject not in config.subjects:
        print ("Subject %s does not exist" % subject)
        return False

    root_dir = config.get('general.root_dir')

    if not root_dir:
        print ("Root dir is not defined in config file")
        return False

    note_prefix = config.get('templates.note_prefix')
    today = datetime.today()
    subject_dir = root_dir + '/' + subject
    path = '%s/%s/%s%d/%s%02d' % (
        subject_dir,
        config.get('templates.notes_dir'),
        config.get('templates.year_dir_prefix'),
        today.year % 1000,
        config.get('templates.month_dir_prefix'),
        today.month
    )

    try:
        os.makedirs(path)
        note_number = 0
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        else:
            note_number = len(fnmatch.filter(os.listdir(path), note_prefix + '*.md'))

    note_number += 1

    meta = load_file(subject_dir + '/' + config.get('templates.meta_file')).format(
        config=config.get('templates.variables'),
        date=time.strftime('%d.%m.%Y'),
        subject=subject,
        note_number=note_number
    )

    path += '/%s%d.md' % (
        config.get('templates.note_prefix'),
        note_number
    )

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

@trackcalls
def compile(subjects, years, months):
    """
    Compile notes for given subjects with selected years and months
    """

    root_dir = config.get('general.root_dir')

    if not root_dir:
        print ("Root dir is not defined in config file")
        return False

    for subject in subjects:

        if subject not in config.subjects:
            print ("Subject %s does not exist" % subject)
            continue

        today = datetime.today()
        subject_dir = root_dir + '/' + subject
        compiled_path = '%s/%s/%s_%02d_%02d_%d.pdf' % (
            subject_dir,
            config.get('templates.compiled_dir'),
            subject.lower(),
            today.day,
            today.month,
            today.year % 1000
        )

        os.chdir(subject_dir)

        command = "pandoc"
        additional_args = config.get('compiling.additional_arguments')
        header_file = config.get('compiling.header_file')

        if additional_args != None:
            command += " %s " % additional_args

        command += " -o %s " % compiled_path

        if header_file != None:
            if os.path.isfile('%s/%s' % (subject_dir, header_file)):
                command += "%s " % header_file
            else:
                print ("Header file %s does not exist. Ignoring" % header_file)

        for year in years:

            year_dir = '%s/%s/%s%d' % (
                subject_dir,
                config.get('templates.notes_dir'),
                config.get('templates.year_dir_prefix'),
                year % 1000
            )

            if not os.path.isdir(year_dir):
                print ("Subject %s has no notes for year %d. Ignoring" % (subject, year))
                continue

            for month in months:

                month_dir = '%s/%s%02d' % (
                    year_dir,
                    config.get('templates.month_dir_prefix'),
                    month
                )

                if not os.path.isdir(month_dir):
                    print ("Subject %s has no notes for month %d in year %d. Ignoring" % (
                        subject,
                        month,
                        year
                    ))
                    continue

                command += '%s/%s*.md ' % (
                    month_dir,
                    config.get('templates.note_prefix')
                )

        # Call cannot be used here since we are using wildcards
        os.system(command)

        return True

@trackcalls
def list():
    """
    Lists subjects
    """

    for subject in config.subjects:
        print(subject)
    else:
        return True

    return False
