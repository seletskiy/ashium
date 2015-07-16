# coding=utf8

import subprocess

FORMAT_ED_SCRIPT = '-e'
FORMAT_MERGED = '-m'


def diff3(my_file, origin_file, theirs_file, format=FORMAT_MERGED):
    options = [
        format,
        my_file, origin_file, theirs_file
    ]

    if format == FORMAT_MERGED:
        options = [
            '-L', 'OURS',
            '-L', 'ORIGIN',
            '-L', 'REMOTE',
        ] + options

    process = subprocess.Popen(
        ['diff3'] + options,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout, stderr = process.communicate()
    if process.returncode > 1:
        raise Exception(
            'diff3 returned error:' +
            '\nSTDERR\n' + stderr +
            '\nSTDOUT\n' + stdout
        )

    return stdout


def differs(my_file, origin_file, theirs_file):
    return "" != diff3(
        my_file, origin_file, theirs_file,
        format=FORMAT_ED_SCRIPT
    )
