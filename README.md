Ever seen AJAX implemented in vim? Here we go!

**Warning**: ashium still in beta. Also, ashium is a multithreaded application,
and it can result into crash. However, most of the exceptions should be catched
and if you notice, that something is wrong, try to open `:mess` and looking for
traceback.

# Ashium

Ashium is a way of reviewing pull-requests in Atlassian Stash using you
favorite editor (vim, obviously).

Ashium works on top of the [ash](https://github.com/seletskiy/ash), which do
all the magic.

Ashium implements sophisticated algorithms to update PR directly in the editor
as soon as it gets changed on the remote side. In most cases it is unobtrusive
and others comments and changes will just magically appears while you reviewing
code or typing your comments.

# Installation

```
Plug 'seletskiy/ashium'
```

# Usage

Just use `ash` for opening review you are interested in.  Ashium will take care
of downloading entire review and handling all updates.

Also, it will save all changes when you leaving review file, but you can commit
changes as soon as you want:

```
map <silent> <leader>c :py ashium.commit()<CR>
map <silent> <leader>o :py ashium.drop_changes()<CR>
```

# Integration to other editor

There is currently no multi-editor support in the ashium, but architecture is
fine enough to make it possible.

New source file should be created under pythonx/editor/<editor>.py with
following methods declared:

* `cd(<dirname>)` -- editor should change current directory to the specified;
* `get_current_file_path()` -- returns full path to the currently opened file;
* `reopen_current_file()` -- editor should reopen currently opened file
  discarding all changes;
* `run_in_foreground(<python_function>)` -- editor should block and run
  specified function in the foreground;
* `save_current_file()` -- editor should store currently opened file on the
  storage;
* `<view_state> = get_window_view_state()` -- python dict with following fields
  should be returned:
  ** `topline` -- number of the first line of the file shown in editor window;
  ** `leftcol` -- number of the first column, that is visible in editor window;
  ** `skipcol` -- should be equal to 0 (vim specific);
* `move_cursor(<line>, <column>, <view_state>)` -- editor should move cursor
  to the specified `<line>` and `<column>`, possibly keeping view state
  described by `<view_state>` (can be `None`, in that case no view state should
  be preserved);
* `(<line>, <column>) = get_cursor()` -- editor should return current cursor
 position, denoted in the tuple `(<line>, <column>)`;
* `on_load_file_in_dir(<dirname>, <python_expression>)` -- editor should bind
  specified `<python_expression>` on opening file in the `<dirname>`;
* `on_idle(<python_expression>)` -- editor should bind specified python
  expression and run it if user do not do any actions for some period of time
  (editor specific);
* `on_file_close(<python_expression>) -- editor should bind specified
  expression and run it **before** current file is closed;

Then, you should instruct your editor to run following code after reading
file, which full path is matches mask `/tmp*/ash.*/*`:

```
ashium.try_to_load_from_current_file()
```

Until ashium is not ready for multi-editor support, manual intervention
required to the file pythonx/ashium/editor/__init__.py. Just alter `from ...`
line in that file to load your editor module instead of `vim`.
