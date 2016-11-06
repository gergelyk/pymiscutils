Magic Context Manager
=====================

Using context managers in IPython requires the user to use ``with`` statement. Common drawback is that inside of the ``with`` statement user cannot take advantages of interactive nature of IPython prompt. Magic Context Manager module provides magic functions for IPython that solve this issue.

Additionally let's consider one more common example:

>>> with MyClass() as obj:
>>>     obj.foo()

This is how context managers are used in Python. It is worth to mention that ``obj`` what is available inside of ``with`` statement is what ``__enter__`` method of MyClass returns. The actual instance of MyClass is unavailable though. This is another thing which Magic Context Manager helps to overcome.

Yet another thing - nested contexts. With Magic Context Manager you can exit outer context without exiting the inner one. This has only limited practical meaning, but can be used for experimenting and debugging.

Finally one must be avare that using Magic Context Manager, whole responsibility of entering and exiting contexts is on the user. This is why Magic Context Manager should be used wiht special caution.

Installation
------------

This module should be imported in one of the startup scripts of IPython. For example ``~/.ipython/profile_default/startup/magic_with.ipy`` can contain following line:

.. code-block:: python

    from miscutils import magic_with

More information on startup scripts can be found `here <https://ipython.org/ipython-doc/1/config/overview.html#startup-files>`_.

Usage
-----

Let's have a look on the example:

>>> fh = %with_enter open('somefile', 'w+')
Item appended. Current stack:
0: open('somefile', 'w+')
>>> fh.write('blah')
4
>>> %with_exit
Item popped. Current stack:
(empty)

This would correspond to the regular Python code:

>>> with open('somefile', 'w+') as fh:
>>>     fh.write('blah')

Reference
---------

**%with_enter** `object`

Open context.
      
Calls ``__enter__`` on the object given as an argument. Returns value returned by ``__enter__``. Object is put on stack.


**%with_exit** `[index=-1, [type=None, [value=None, [tb=None]]]]`

Close context.
    
Calls ``__exit__(type, value, tb)`` on the object from the stack. Object is removed from the stack. Index on the stack can be provided. Default is -1 which corresponds the the last item on the stack. ``type``, ``value``, ``tb`` are arguments that are passed to ``__exit__``.
    

**%with_show**

Disply stack of Magic Context Manager.


**%with_clear**
    
Clears stack of Magic Context Manager commands


**%with_get** `[index=-1]`

Returns object from stack of Magic Context Manager.

Index on the stack can be provided. Default is -1 which corresponds the the last item on the stack.


