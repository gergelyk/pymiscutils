fs
==

File system related utilities.

copy_dir
--------

**copy_dir** `(src, dst)`

Copies src directory recursively on place of dst. If dst already exists, it will be removed first.

This function uses following commands of Unix shell: `rm`, `cp`

repl_in_paths
-------------

**repl_in_paths** `(text, repl, top_dir='.')`

Scans top_dir recursively to find given text in file/dir names. Then replaces this text by repl. Function is case sensitive.

This function uses following commands of Unix shell: `find`, `mv`

For example, if current directory has following structure::

    foo.txt
    README.txt
    my_foo_files\first.py
    my_foo_files\second.py
    my_foo_files\foo.py

invoking ``repl_in_paths('foo', 'bar', '.'):`` will process it as follows::

    bar.txt
    README.txt
    my_bar_files\first.py
    my_bar_files\second.py
    my_bar_files\bar.py

repl_in_files
-------------

**repl_in_files** `(text, repl, top_dir='.')`

Scans top_dir recursively to find given text in the content of files. Then replaces this text by repl. Function is case sensitive.

This function uses following commands of Unix shell: `grep`, `sed`


