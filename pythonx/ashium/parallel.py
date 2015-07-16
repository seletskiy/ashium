# coding=utf8

import threading
import traceback
import editor


def run(task):
    def task_wrapper(task):
        try:
            task()
        except Exception as exception:
            editor.write_message(
                'Exception occured while execution threaded command. '
                'Traceback follows.\n' +
                traceback.format_exc(exception)
            )

    threading.Thread(target=lambda: task_wrapper(task)).start()
