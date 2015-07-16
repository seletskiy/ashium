# coding=utf8

import threading
import os.path

import ash
import parallel
import review


class Entry(object):

    def __init__(self, review, name_in_review):
        self._review = review
        self._name_in_review = name_in_review
        self._updating = False
        self._update_lock = threading.Lock()

    def get_name_in_review(self):
        return self._name_in_review

    def get_file_path(self):
        if self._name_in_review == review.OVERVIEW:
            return os.path.join(
                self._review.get_local_path(),
                'overview'
            ) + '.diff'
        else:
            return os.path.join(
                self._review.get_files_path(),
                self._name_in_review
            ) + '.diff'

    def update(self, force=False):
        if not os.path.exists(self.get_file_path()) or force:
            self._download_file()
        else:
            self._update_file()

    def get_origin_path(self):
        if self._name_in_review == review.OVERVIEW:
            return os.path.join(
                self._review.get_origin_path(),
                'overview'
            ) + '.diff'
        else:
            return os.path.join(
                self._review.get_origin_files_path(),
                self._name_in_review
            ) + '.diff'

    def _download_file(self):
        parallel.run(lambda: ash.get_review_into_file(
            self._review.get_id(),
            self._name_in_review,
            self.get_file_path()
            )
        )

    def _update_file(self):
        if self._updating:
            return

        with self._update_lock:
            self._updating = True

        def download_and_compare():
            new_file_name = self.get_file_path() + '.new'

            try:
                ash.get_review_into_file(
                    self._review.get_id(),
                    self._name_in_review,
                    new_file_name,
                )

                self._review._diff_with_remote(
                    self.get_file_path(),
                    new_file_name,
                )
            finally:
                with self._update_lock:
                    self._updating = False

        parallel.run(download_and_compare)
