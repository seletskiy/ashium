# coding=utf8

import editor
import subprocess
import re

import utils


def get_review_into_file(review_url, review_file_name, target_name):
    utils.create_file_directories(target_name)
    subprocess.check_output(
        [
            'ash', '--no-color',
            review_url, 'review',
            review_file_name,
            '--output', target_name
        ],
        stderr=subprocess.STDOUT
    )


def get_review_files_list(review_url):
    result = []

    rawFilesList = subprocess.check_output(
        [
            'ash', '--no-color',
            review_url, 'ls'
        ],
        stderr=subprocess.STDOUT
    )

    for rawFileEntry in rawFilesList.strip().split('\n'):
        matches = re.match("\s*(\w+)\s+(.*?)\s*(?:(\s+[-+]x))?$", rawFileEntry)
        if not matches:
            raise Exception(
                "unexpected entry from ash ls: <{}>".format(rawFileEntry)
            )

        result.append(matches.group(2))

    return result


def upload_review(review_url, input_file, review_file_name, origin_file):
    command = [
        'ash', '-i', '--no-color',
        '--input', input_file,
        '--origin', origin_file,
        review_url, 'review'
    ]

    if review_file_name is not None:
        command.append(review_file_name)

    editor.command("silent! !" + " ".join(command))
