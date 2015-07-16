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
