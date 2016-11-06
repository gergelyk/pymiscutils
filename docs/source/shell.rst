Shell
=====

This module includes tools for interacting with system shell. Most of the commands require underlying Unix enviroment or at least GNU utilities installed in your system. MSYS seems to be a good candidate for Windows users. This solution hasn't been tested though.

shell
-----

**shell** `(cmd, *args, **kwargs)`

This function has been inspired by ``%sx`` magic known from IPython. It executes given command in underlying shell. Returns array of strings that represent stdout of the command split in lines. If return code of the command doesn't equal 0, ``subprocess.CalledProcessError`` exception is raised. Second and following arguments are passed to ``format()`` function in order to preprocess the command itself.

>>> shell('ls -a {topdir}', topdir='~/pymiscutils')
['.',
 '..',
 'docs',
 'dodo.py',
 'examples',
 '.git',
 'miscutils',
 'README.cfg',
 'README.rst',
 'setup.py',
 'tests']

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


