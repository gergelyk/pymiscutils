import re
from itertools import chain

class ErrorBranchLocked(KeyError): pass
class ErrorAttributeDuplicated(Exception): pass

class Branch:
    """ Branch that is a component of the tree. See tree() function. Note that
        Branch implements idea of Extended Attributes. This means that attributes
        can be accessed in three ways:
            
        >>> obj.foo
        >>> obj['foo']
        >>> getattr(obj, 'foo')
        
        >>> obj.foo = 123
        >>> obj['foo'] = 123
        >>> setattr(obj, 'foo', 123)
        
        Attribute names can be not only textual, but also numerical (indices)
        or of any other type.
    """
    
    # Yes, we need these attributes here, even though they are overwritten in __init__
    _root = None
    _dict_ext = {}
    _leaves = {}
    _locked = False

    def __init__(self, root):
        self._root = root
        self._dict_ext = {}
        self._leaves = {}

    def __getattr__(self, name):
        # This method is called only if 'name' is not found in attribs of 'self'
        return getattr(self._root, self._leaves[name])

    def __setattr__(self, name, value):
        # This method is called, no matter if 'name' is an existing attribute
        # of 'self' or not
        if name in self._leaves:
            setattr(self._root, self._leaves[name], value)
        else:
            if self._locked:
                raise ErrorBranchLocked('This object is locked. You cannot add attributes.')
            else:
                super().__setattr__(name, value)

    def __dir__(self):
        """ Return list of:

        * regular attributes defined by textual names (including these which
          include spaces and other syntax-unfriendly characters)
        * private, protected and built-in attributes

        It will not include:

        * attributes defined by non-textual names
        * especially attributes defined by numerical names
        """
        cls = dir(type(self))
        obj = list(self.__dict__.keys())
        ext = [key for key in self._dict_ext.keys() if isinstance(key, str)]
        lvs = [key for key in self._leaves.keys() if isinstance(key, str)]
        return list(set(cls + obj + ext + lvs))

    def _keys(self, plain_only=False, visible_only=False, numeric_only=False, sort=False):
        """ Return list of all the attributes, including these which __dir__
        wouldn't return.
        Following filters can be enabled (and also combined):

        * plain_only - only attribs with textual names that are valid Python
            identifiers.
        * visible_only - only attribs with non-textual names and these with
            textual names that don't start with underscore.
        * numeric_only - only attribs with numeric names (indices)

        'sort' option can be used only when the resulting list is sortable.
        """
        cls = dir(type(self))
        obj = list(self.__dict__.keys())
        ext = list(self._dict_ext.keys())
        lvs = list(self._leaves.keys())
        keys = set(cls + obj + ext + lvs)

        def isplain(a):
            return isinstance(a, str) and re.match('^[a-zA-Z_][a-zA-Z0-9_]*$', a)

        def isvisible(a):
            return not isinstance(a, str) or not a.startswith('_')

        def isnumeric(a):
            return isinstance(a, int)

        if plain_only:
            keys = filter(isplain, keys)

        if visible_only:
            keys = filter(isvisible, keys)

        if numeric_only:
            keys = filter(isnumeric, keys)

        if sort:
            keys = sorted(keys)

        return list(keys)

    def _values(self, plain_only=False, visible_only=False, numeric_only=False, sort=False):
        """ Return values of the attributes. Sort can be used to sort values by keys.
        """
        keys = self._keys(plain_only, visible_only, numeric_only, sort)
        return (self[key] for key in keys)

    def _items(self, plain_only=False, visible_only=False, numeric_only=False, sort=False):
        """ Return (key, value) pairs that connect names and values of the attributes. Sort can be used to sort items by keys.
        """
        keys = self._keys(plain_only, visible_only, numeric_only, sort)
        return ( (key, self[key]) for key in keys)

    def __iter__(self):
        """ Iterate through numerical attributes. Sorting not guaranteed.
        """
        return self._values(numeric_only=True)

    def __len__(self):
        """ Say how many numerical attributes we have.
        """
        return len(self._keys(numeric_only=True))

    def __getitem__(self, name):
        if isinstance(name, str):
            return getattr(self, name)
        else:
            if name in self._leaves:
                return getattr(self._root, self._leaves[name])
            else:
                return self._dict_ext[name]

    def __setitem__(self, name, value):
        if isinstance(name, str):
            setattr(self, name, value)
        else:
            if name in self._leaves:
                setattr(self._root, self._leaves[name], value)
            else:
                self._dict_ext[name] = value

    def __str__(self):
        """ Recursively displays all the values. Results are sorted.
        """
        def disp(lines, value, level=0):
            indent = ' '*2
            keys = value._keys(visible_only=True)
            names = [(k, k) if isinstance(k, str)
                     else (k, '[' + str(k) + ']') for k in keys]

            names.sort(key=lambda x: x[1])
            for key, name in names:
                data = value[key]
                if isinstance(data, Branch):
                    lines.append('{}{}'.format(indent*level, name))
                    disp(lines, data, level+1)
                else:
                    lines.append('{}{} = {}'.format(indent*level, name, data))

        lines = []
        disp(lines, self)
        return '\n'.join(lines)

def add_sub_branch(root, parent, orig, split):
    attr = split[0]
    if len(split) == 1:
        if attr in parent._keys():
            raise ErrorAttributeDuplicated('Attribute {} duplicated'.format(attr))
        else:
            # Add leaf
            parent._leaves[attr] = orig
    else:
        if attr in parent._keys():
            # Add to existing branch
            if not isinstance(parent[attr], Branch):
                raise ErrorAttributeDuplicated('Attribute {} duplicated'.format(attr))
            add_sub_branch(root, parent[attr], orig, split[1:])
        else:
            # Add to new branch
            child = Branch(root)
            add_sub_branch(root, child, orig, split[1:])
            parent[attr] = child

def split_attr_default(attr):

    def split_segment(segment):

        # Segment is expected to be NN..NII..I
        # where N (name) is any character and I (index) is a digit
        m = re.search(r'^(\d*)(.*)$', segment[::-1])
        name = m.groups()[1][::-1].strip()
        index = m.groups()[0][::-1]

        # Replace any uncommon character (e.g. space or dash) with underscore
        name = re.sub('[^a-zA-Z0-9_]', '_', name)

        name_a = [name] if name else []
        index_a = [int(index)] if index else []
        return name_a + index_a

    segments = [p.strip() for p in re.split(r'[\.]', attr)]
    parts = chain(*map(split_segment, segments))
    return list(parts)

def lock(branch):
    branch._locked = True
    for b in branch._values():
        if isinstance(b, Branch):
            lock(b)

def tree(obj, split_attr=split_attr_default):
    """ Create a structure of Branch objects that is described by names of the
    attributes of 'obj'. For instance:
        
    >>> class C: pass
    >>> c = C()
    >>> setattr(c, 'foo.x', 123)
    >>> setattr(c, 'foo.y', 234)
    >>> setattr(c, 'bar.x', 345)
    >>> setattr(c, 'bar.y', 456)
    >>> t = tree(c)
    >>> t.foo.x
    123
    >>> t.foo.y
    234
    >>> t.bar.x
    345
    >>> t.bar.y
    456
     
    'split_attr' is a function that takes attribute name as parameter and splits
    it into list of components that build path to the attribute. By default 
    'split_attr_default' function is in use. For example:
        
    >>> split_attr_default('foo.x')
    ['foo', 'x']
        
    List of components can include also integers. Later they turn into indices.
    For example:
        
    >>> split_attr_default('foo.x0.val')
    ['foo', 'x', 0, 'val']
    
    >>> class C: pass
    >>> c = C()
    >>> setattr(c, 'foo.x0', 123)
    >>> setattr(c, 'foo.x1', 234)
    >>> setattr(c, 'foo.x02', 345)
    >>> t = tree(c)
    >>> t.x[0]
    123
    >>> t.x[1]
    234
    >>> t.x[2]
    345
    
    Names and indices can be mixed.
    
    """ 
    
    def isvisible(a):
        return not isinstance(a, str) or not a.startswith('_')

    attrs = filter(isvisible, dir(obj))
    branch = Branch(obj)
    splits = {orig: split_attr(orig) for orig in attrs}

    for orig in splits:
        add_sub_branch(obj, branch, orig, splits[orig])

    lock(branch)
    return branch

