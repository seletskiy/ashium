# coding=utf8

import os
import re
import errno
import uuid


def create_file_directories(filename):
    dirname = os.path.dirname(filename)
    if dirname:
        try:
            os.makedirs(dirname)
        except OSError as exception:
            if exception.errno == errno.EEXIST and os.path.isdir(dirname):
                pass
            else:
                raise


def write_placeholder(file_name, line_number):
    placeholder = '### {}{}'.format(
        uuid.uuid4(),
        os.linesep
    )

    with open(file_name, 'r+') as file:
        contents = file.readlines()
        contents.insert(line_number, placeholder)
        file.truncate(0)
        file.seek(0, 0)
        file.writelines(contents)

    return placeholder


def extract_placeholder(file_name, placeholder):
    placeholder_line_number = 0

    with open(file_name, 'r+') as file:
        contents = file.readlines()
        for (line_number, line) in enumerate(contents):
            if line == placeholder:
                placeholder_line_number = line_number
                del contents[line_number]
                break
        file.truncate(0)
        file.seek(0, 0)
        file.writelines(contents)

    return placeholder_line_number


def parse_modeline(line):
    matches = re.match(r'### ash: (.*)', line)
    if not matches:
        return None

    modeline = {}

    for rawItem in matches.group(1).split(' '):
        splitted = rawItem.split('=')
        if len(splitted) == 1:
            modeline[splitted[0]] = True
        else:
            modeline[splitted[0]] = splitted[1]

    return modeline
