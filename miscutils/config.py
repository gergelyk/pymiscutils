from collections import OrderedDict

class Config:
    """
    Assigning values
    >>> cfg = Config()
    >>> cfg.var1 = 123
    >>> cfg.var2 = 456
    
    Accessing selected value(s)
    >>> cfg[1]
    456
    >>> cfg[0:2]
    [123, 456]
    >>> cfg['var1']
    123
    >>> cfg.var1
    123
    >>> d = list(map(lambda key: cfg[key], ['var1', 'var2']))
    []

    >>> accessing all values (in order)
    >>> cfg[:]
    [123, 345]

    >>> accessing all keys (in order)
    >>> [x for x in cfg]
    ['var1', 'var2']
    >>> list(cfg)
    ('var1', 'var2')
    >>> set(cfg)
    {'var1', 'var2'}

    >>> accessing other properties
    >>> len(cfg)
    2
    >>> str(cfg)
    "{'var1': 123, 'var2': 345}"
    >>> repr(cfg)
    "{'var1': 123, 'var2': 345}"

    >>> accessing items (in order)
    >>> {x: cfg[x] for x in cfg}
    {'var1': 123, 'var2': 345}

    Note: dict(cfg) is not supported.

    """

    _attribs = OrderedDict()

    def __setattr__(self, name, value):
        if name in dir(self):
            super().__setattr__(name, value)
        else:
            self._attribs[name] = value
    
    def __getattr__(self, name):
        return self._attribs[name]
    
    def __getitem__(self, descriptor):
        if isinstance(descriptor, slice):
            names = list(self._attribs.keys())[descriptor]
            return [getattr(self, name) for name in names]
        elif isinstance(descriptor, int):
            index = descriptor
            name = list(self._attribs.keys())[index]
            return getattr(self, name)
        else:
            name = descriptor
            return getattr(self, name)

    def __iter__(self):
        return (attr for attr in self._attribs)
        
    def __len__(self):
        return len(self._attribs)
        
    def __str__(self):
        return str(self._attribs)
        
    def __repr__(self):
        return str(self._attribs)
 
# this would need to be enabled in order to support dict(Config())
# but we don't want to mess in the user's namespace

#    def keys(self):
#        return self._attribs.keys()



