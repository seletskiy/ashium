# coding=utf8

import loader

_active_review = None


def start_review(review_url=None):
    global _active_review

    if _active_review:
        raise Exception("review already started")

    if not review_url:
        _active_review = loader.load_from_current_file()
    else:
        _active_review = loader.load_from_url(review_url)


def stop_review():
    global _active_review

    if not _active_review:
        return

    _active_review.stop()
    _active_review = None


def commit():
    if not _active_review:
        raise Exception("no review is loaded")

    _active_review.commit()


def drop_changes():
    if not _active_review:
        raise Exception("no review is loaded")

    _active_review.load_current_buffer_from_remote()


def try_to_load_from_current_file():
    global _active_review

    _active_review = loader.load_from_current_file()
