dbg
===

Debugging utilities.

attrch
------
Register an action to take on attribute change.

Examples:

.. code-block:: python

    def example1():

        # capture any attribute change
        @attrch()
        class Foo:
            pass

        foo = Foo()
        foo.x = 123
        foo.xy = 123
        foo.xyz = 10

    def example2():

        # capture any attribute change to 10
        # and changes of attributes of the name with two letters
        @attrch(value=10)
        @attrch('..')
        class Foo:
            pass

        foo = Foo()
        foo.x = 123
        foo.xy = 123
        foo.xyz = 10

    def example3():

        class M(type): pass

        @attrch('..', meta=True)
        class Foo(metaclass=M):
            pass

        Foo.x = 123
        Foo.xy = 123
        Foo.xyz = 123
        print(Foo)

    def example4():

        @attrch('..', meta=True)
        class Foo:
            pass

        Foo.x = 123
        Foo.xy = 123
        Foo.xyz = 123
        print(Foo)

