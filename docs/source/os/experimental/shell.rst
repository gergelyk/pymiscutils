shell
=====

Shell related utilities

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
