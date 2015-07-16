# coding=utf8

from __future__ import absolute_import

import subprocess
import vim
import traceback
import Queue
import threading
import sys

_commands_queue = Queue.Queue()
_lock = threading.Lock()


def _run_expression(expression):
    process = subprocess.Popen(
        [
            'vim', '--remote-expr', expression,
            '--servername', vim.eval("v:servername")
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE
    )

    stdout, stderr = process.communicate()

    if process.returncode:
        raise Exception(
            'vim returned error:\n' + stderr
        )

    return stdout


def _run_task(task):
    if threading.current_thread().name == 'MainThread':
        task()
    else:
        _commands_queue.put(task)
        with _lock:
            _run_expression(
                "pyeval('"
                '__import__("ashium").editor.process_remote_queue()'
                "')"
            )


def command(command):
    if threading.current_thread().name == 'MainThread':
        vim.command(command)
    else:
        _run_task(lambda: vim.command(command))


def process_remote_queue():
    while not _commands_queue.empty():
        task = _commands_queue.get()
        try:
            task()
        except Exception as e:
            sys.stdout.write(
                'Remote execution failed. Traceback follows.\n' +
                traceback.format_exc(e)
            )


def write_message(message):
    if threading.current_thread().name == 'MainThread':
        sys.stdout.write(message)
    else:
        _run_task(lambda: sys.stdout.write(message))


def cd(directory):
    command("silent cd {}".format(directory))


def on_load_file_in_dir(base_dir, code):
    command("au BufEnter {}/* py {}".format(base_dir, code))


def on_idle(code):
    command("augroup ashium_cursor_hold")
    command("au!")
    command("au CursorHoldI <buffer> py {}".format(code))
    command("au CursorHold  <buffer> py {}".format(code))
    command("augroup end")


def save_current_file():
    command('silent write!')


def reopen_current_file():
    command('silent edit!')


def open_file(file_name):
    # reopen file in place of current buffer
    command('bw! | edit! {}'.format(file_name))
    command('filetype detect')


def on_file_close(code):
    command("au BufWinLeave <buffer> py {}".format(code))


def move_cursor(line, column, view_state=None):
    command('silent edit! +normal\ {}G{}\|'.format(line, column))
    command('call feedkeys("\<right>", "n")')
    if view_state:
        command(
            'call winrestview('
            '{{"topline": {}, "leftcol": {}, "skipcol": {}}}'
            ')'.format(
                view_state['topline'],
                view_state['leftcol'],
                view_state['skipcol'],
            )
        )


def get_cursor():
    return (
        int(vim.current.window.cursor[0]),
        int(vim.current.window.cursor[1])
    )


def get_window_view_state():
    return vim.eval('winsaveview()')


def run_in_foreground(task):
    _run_task(task)


def get_current_file_path():
    return vim.current.buffer.name
