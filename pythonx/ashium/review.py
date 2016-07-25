# coding=utf8

import tempfile
import shutil
import os.path

import ash
import diff
import utils
import editor
import review_entry

OVERVIEW = ''


class Review(object):

    def __init__(self, review_url, autoupdate=False):
        self._temp_dir = tempfile.mkdtemp(".ashium")
        self._review_url = review_url
        self._entries = {}
        self._autoupdate = autoupdate

        os.makedirs(self.get_files_path())
        os.makedirs(self.get_origin_files_path())

    def stop(self):
        shutil.rmtree(self._temp_dir)

    def get_id(self):
        return self._review_url

    def load(self):
        editor.cd(self.get_local_path())

        editor.on_load_file_in_dir(
            self.get_local_path(),
            "ashium._active_review._setup_buffer()"
        )

        files_list = ash.get_review_files_list(self._review_url)
        files_list.insert(0, OVERVIEW)
        for file_name in files_list:
            entry = review_entry.Entry(self, file_name)
            entry.update()

            self._entries[entry.get_file_path()] = entry

    def update_file(self, filename, force=False):
        self.get_entry(filename).update(force)

    def get_entry(self, filename):
        if filename not in self._entries:
            raise Exception(
                'requested file is not found: {}'.format(filename)
            )

        return self._entries[filename]

    def update_current_buffer(self):
        self.update_file(editor.get_current_file_path())

    def load_current_buffer_from_remote(self):
        self.update_file(editor.get_current_file_path(), force=True)
        editor.reopen_current_file()

    def _save_origin(self, source=None):
        entry = self.get_entry(editor.get_current_file_path())

        origin_path = entry.get_origin_path()
        if not source and os.path.exists(origin_path):
            return

        if source is None:
            source = entry.get_file_path()

        utils.create_file_directories(origin_path)

        shutil.copyfile(source, origin_path)

    def _diff_with_remote(self, file_path, theirs_file):
        entry = self.get_entry(file_path)

        my_file = entry.get_file_path()
        origin_file = entry.get_origin_path()

        if not diff.differs(my_file, origin_file, theirs_file):
            os.unlink(theirs_file)
            return

        editor.run_in_foreground(
            lambda: self._apply_patch(file_path, theirs_file)
        )

    def _apply_patch(self, file_path, theirs_file):
        entry = self.get_entry(file_path)

        my_file = entry.get_file_path()
        origin_file = entry.get_origin_path()

        editor.save_current_file()

        view_state = editor.get_window_view_state()

        placeholder = utils.write_placeholder(
            my_file,
            editor.get_cursor()[0]
        )

        merged_contents = diff.diff3(my_file, origin_file, theirs_file)
        with open(my_file, 'w') as file:
            file.write(merged_contents)

        line_number = utils.extract_placeholder(
            my_file,
            placeholder,
        )

        editor.move_cursor(line_number, editor.get_cursor()[1], view_state)

        self._save_origin(theirs_file)

        os.unlink(theirs_file)

    def commit(self):
        if not editor.is_current_file_modified():
            return

        editor.save_current_file()

        entry = self.get_entry(editor.get_current_file_path())

        ash.upload_review(
            self._review_url,
            editor.get_current_file_path(),
            entry.get_name_in_review(),
            entry.get_origin_path()
        )

        ash.get_review_into_file(
            self._review_url,
            entry.get_name_in_review(),
            entry.get_file_path(),
        )

        self._save_origin(entry.get_file_path())

        editor.reopen_current_file()
        editor.redraw()

    def get_files_path(self):
        return os.path.join(self.get_local_path(), 'files')

    def get_local_path(self):
        return os.path.join(self._temp_dir, 'local')

    def get_origin_path(self):
        return os.path.join(self._temp_dir, 'origin')

    def get_origin_files_path(self):
        return os.path.join(self.get_origin_path(), 'files')

    def _setup_buffer(self):
        self._save_origin()

        if self._autoupdate:
            editor.on_idle("ashium._active_review.update_current_buffer()")

        editor.on_file_close("ashium._active_review.commit()")
        editor.on_file_changed("ashium._active_review._on_file_changed()")

    def _add_loaded_file(self, file_name):
        entry = review_entry.Entry(self, file_name)

        self._entries[entry.get_file_path()] = entry

        return entry

    def _on_file_changed(self):
        editor.set_file_modified()
