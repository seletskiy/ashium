# coding=utf8

import editor
import review
import utils
import shutil


def load_from_current_file():
    with open(editor.get_current_file_path(), 'r') as buffer:
        for line in buffer.readlines():
            modeline = utils.parse_modeline(line)
            if modeline:
                break

    file_name = None
    if 'overview' in modeline:
        file_name = review.OVERVIEW
    if 'file' in modeline:
        file_name = modeline['file']

    return load_from_url(modeline['review-url'], file_name)


def load_from_url(url, file_name=None):
    active_review = review.Review(url, autoupdate=True)
    if file_name is not None:
        entry = active_review._add_loaded_file(file_name)

        shutil.copy(editor.get_current_file_path(), entry.get_file_path())

    active_review.load()

    if file_name is not None:
        editor.open_file(entry.get_file_path())

    return active_review
