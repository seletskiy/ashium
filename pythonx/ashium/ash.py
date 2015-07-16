# coding=utf8

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
        ]
    )


def get_review_files_list(review_url):
    result = []

    rawFilesList = subprocess.check_output(
        [
            'ash', '--no-color',
            review_url, 'ls'
        ]
    )

    for rawFileEntry in rawFilesList.strip().split('\n'):
        matches = re.match("\s*(\w+)\s+(.*?)\s*(?:(\s+[-+]x))?$", rawFileEntry)
        if not matches:
            raise Exception(
                "unexpected entry from ash ls: <{}>".format(rawFileEntry)
            )

        result.append(matches.group(2))

    return result


def upload_review(review_url, input_file, review_file_name):
    command = [
        'ash', '--no-color',
        '--input', input_file,
        review_url, 'review'
    ]

    if review_file_name is not None:
        command.append(review_file_name)

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout, stderr = process.communicate()

    if process.returncode > 0 and process.returncode != 2:
        raise Exception(
            'ash returned error:' +
            '\nSTDERR\n' + stderr +
            '\nSTDOUT\n' + stdout
        )
