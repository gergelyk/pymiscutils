arginfo
=======

When ``arginfo`` object is used as a decorator, it can be also used as
an interface providing information about the args of decorated function.
This includes current and default values of the arguments as well as
boolean flag to say which argument has been set by the caller.

For examples:

* Use arginfo to check which arguments have been set and which kwargs are specifed:

>>> @arginfo
... def foo(x=100, **kwargs):
...     if arginfo.x.isset:
...         print("'a' is set!")
...
...     if x == arginfo.x.defval:
...         print("'a' has default value!")
...
...     if 'y' in arginfo:
...         print("'y' is specified")
>>> foo()
'a' has default value!
>>> foo(x = 200)
'a' is set!
>>> foo(x = 100)
'a' is set!
'a' has default value!
>>> foo(y=123)
'a' has default value!
'y' is specified

* You can iterate & subscribe arginfo object:

>>> @arginfo
... def foo(a, b=123, *, c, d=456):
...     for argname in sorted(arginfo):
...         print(argname, arginfo[argname].isset)
>>> foo(1, c=2)
a True
b False
c True
d False
>>> foo(1, 2, c=3, d=4)
a True
b True
c True
d True
>>> foo(1, 123, c=3, d=456)
a True
b True
c True
d True

* Print details of the arguments:

>>> @arginfo
... def foo(a, b=123, *, c, d=456):
...     print(arginfo.a)
...     print(arginfo.b)
...     print(arginfo.c)
...     print(arginfo.d)
>>> foo(1,c=2)
Argument(isset=True, value=1)
Argument(defval=123, isset=False, value=123)
Argument(isset=True, value=2)
Argument(defval=456, isset=False, value=456)


