Config
======

**Config** `()`

Class desired to store configuration data of your application.

This is what you put in ``config.py`` among the sources of your application::

    from miscutils.config import Config
    cfg = Config()
    # user parameters
    cfg.var1 = 123
    cfg.var2 = 456

Next, you import the file in your sources:

>>> from config import cfg

Now you can do the followind:

* Access selected value(s):

>>> cfg[1]
456
>>> cfg[0:2]
[123, 456]
>>> cfg['var1']
123
>>> cfg.var1
123
>>> d = list(map(lambda key: cfg[key], ['var1', 'var2']))
[123, 456]

* Access all values at once (in order):

>>> cfg[:]
[123, 345]

* Access all keys at once (in order):

>>> [x for x in cfg]
['var1', 'var2']
>>> list(cfg)
['var1', 'var2']
>>> tuple(cfg)
('var1', 'var2')
>>> set(cfg)
{'var1', 'var2'}

* Access items (pairs of keys and values, in order):

>>> {x: cfg[x] for x in cfg}
{'var1': 123, 'var2': 345}

* Access other properties:

>>> len(cfg)
2
>>> str(cfg)
"OrderedDict([('var1', 123), ('var2', 456)])"
>>> repr(cfg)
"OrderedDict([('var1', 123), ('var2', 456)])"

Note: :code:`dict(cfg)` is not supported.

