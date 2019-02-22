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


from dosu import config
from dosu.utils import load_file
from dosu.decorators import trackcalls


@trackcalls
def make(subjects: list, semester: str) -> bool:
    """
    Makes (creates) given subjects
    """
    subject_dir = config.get('templates.subject_dir')
    root_dir = config.get('general.root_dir')

    if not root_dir:
        print("Root dir is not defined in config file")
        return False

    if not subject_dir:
        print("Subject template dir is not defined in config file")
        return False

    for subject in subjects:

        target = '%s/%s/%s' % (root_dir, semester, subject)

        if os.path.exists(target):
            print("Subject %s already exists" % subject)
            continue

        copy_tree(subject_dir, target, preserve_symlinks=1)

    else:
        return True

    return False


@trackcalls
def delete(subjects: list, semester: str) -> bool:
    """
    Deletes given subjects
    """
    root_dir = config.get('general.root_dir')

    if not root_dir:
        print("Root dir is not defined in config file")
        return False

    for subject in subjects:

        target = '%s/%s/%s' % (root_dir, semester, subject)
        if not os.path.exists(target):
            print("Subject %s does not exist" % subject)
            continue

        shutil.rmtree(root_dir + '/' + subject)

    else:
        return True

    return False


@trackcalls
def write(subject: str, semester: str) -> bool:
    """
    Starts notetaking for a given subject
    """
    root_dir = config.get('general.root_dir')

    if not root_dir:
        print("Root dir is not defined in config file")
        return False

    note_prefix = config.get('templates.note_prefix')
    subject_dir = '%s/%s/%s' % (root_dir, semester, subject)

    if not os.path.exists(subject_dir):
        print("Subject %s does not exist" % subject)
        return False

    path = '%s/%s' % (subject_dir, config.get('templates.notes_dir'))

    try:
        os.makedirs(path)
        note_number = 0
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        else:
            note_number = len(fnmatch.filter(
                os.listdir(path), note_prefix + '*.md'))

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
        cmd = config.get('writing.reader')

        if '{}' in cmd:
            cmd = cmd.replace('{}', tmp_pdf_path)
        else:
            cmd += ' {}'.format(tmp_pdf_path)

        cmd = shlex.split(cmd)
        subprocess.Popen(cmd)

    if config.get('writing.open_editor'):
        cmd = config.get('writing.editor')

        if '{}' in cmd:
            cmd = cmd.replace('{}', path)
        else:
            cmd += ' {}'.format(path)

        cmd = shlex.split(cmd)
        subprocess.Popen(cmd)

    onmodify_cmd = 'onmodify {} pandoc {} {} -o {}'.format(
        path,
        path,
        config.get('compiling.additional_arguments'),
        tmp_pdf_path
    )
    onmodify_cmd = shlex.split(onmodify_cmd)
    subprocess.Popen(onmodify_cmd)

    sys.exit(0)

    return True


@trackcalls
def compile(subjects: list, semester: str) -> bool:
    """
    Compile notes for given subjects with selected years and months
    """

    root_dir = config.get('general.root_dir')

    if not root_dir:
        print("Root dir is not defined in config file")
        return False

    for subject in subjects:

        subject_dir = '%s/%s/%s' % (root_dir, semester, subject)

        if os.path.exists(subject_dir):
            print("Subject %s does not exist" % subject)
            continue

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
                print("Header file %s does not exist. Ignoring" % header_file)

        command += '%s/%s*.md ' % (
            month_dir,
            config.get('templates.note_prefix')
        )

        command += '%s/%s/%s*.md' % (
            subject_dir,
            config.get('templates.notes_dir'),
            config.get('templates.note_prefix')
        )

        # Call cannot be used here since we are using wildcards
        os.system(command)

        return True


@trackcalls
def list(semester: str):
    """
    Lists subjects
    """

    root_dir = config.get('general.root_dir')

    if not root_dir:
        print("Root dir is not defined in config file")
        return False

    path = '%s/%s/' % (root_dir, semester)

    for subject in os.listdir(path):
        print(subject)
    else:
        return True

    return False
