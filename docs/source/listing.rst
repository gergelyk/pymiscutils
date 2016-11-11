Listing
=======

This module helps with preparing listings of Python code like the one below:

>>> 123 + 345
468
>>> def foo(text):
...     print(text.upper())
>>> foo('Hello World!')
HELLO WORLD!

Usage
-----

The easiest way of getting a listing as above is by preparing the following script:

.. code-block:: python

    123 + 345
    def foo(text):
        print(text.upper())

    foo('Hello World!')

and running it as follows:

.. code-block:: bash

    python -m pylisting filename [first_line=1 [cell_width=80 [cell_height=10 [compact=True]]]]

or simply:

.. code-block:: bash

    pylisting filename [first_line=1 [cell_width=80 [cell_height=10 [compact=True]]]]

Note that square brackets denote arguments which are optional.

The other option requires of adding one extra line in the script:

.. code-block:: python

    from miscutils import listing_here

    123 + 345
    def foo(text):
        print(text.upper())

    foo('Hello World!')

and running it in python, as usually:

.. code-block:: bash

    python myscript.py

Whenever you would like to exclude some code from the listing, you should place it above the line which imports ``listing_here`` module. For instance:

.. code-block:: python

    def foo(text):
        print(text.upper())

    from miscutils import listing_here

    123 + 345
    foo('Hello World!')

will result in:

.. code-block:: python

    >>> 123 + 345
    468
    >>> foo('Hello World!')
    HELLO WORLD!

It is also possible to customize the look of the listing:

.. code-block:: python

    from miscutils.listing import listing_here

    def bar(n):
        return list(range(n))

    listing_here(cell_width=20, cell_height=5)

    bar(1000)

will produce:

.. code-block:: python

    >>> bar(1000)
    [0, 1, 2, 3, 4, 5,
     6, 7, 8, 9, 10, 11,
     12, 13, 14, 15, 16,
     ...
     997, 998, 999]

Finally, code from external file or from variables can be listed by using ``listing_file`` and ``listing`` functions. For more details see `Reference`_.

Reference
---------

**listing_here** `(cell_width=80, cell_height=10, compact=True)`

    Print listing considering everything before the line where this function is called as silent code and everything after the line where this function is called as verbose code.


**listing_file** `(filename, firstline=1, cell_width=80, cell_height=10, compact=True)`

    Print listing of the code in the file specified by ``filename``. firstline defines the first line of verbose code. Everything above is considered as silent code.


**listing** `(silent_code, verbose_code, cell_width=80, cell_height=10, compact=True)`

    First silently executes code provided in ``silent_code``. Then executes code provided in ``verbose_code`` printing listing at the same time.

